#!/usr/bin/env python3
"""Arşivdeki eski sayfalardan src/content/pages/ dosyalarını üretir.

Bir kez çalıştırılır; var olan dosyanın üzerine yazmaz (elle yapılan
düzeltmeler korunsun). Yeniden üretmek için dosyayı silin.

  - Makaleler ve KVKK metni: gövde, eski sayfanın HTML'i olarak HARFİYEN
    taşınır. Yalnızca biçim temizlenir (style/class, boş paragraf, resim);
    tek bir harf değişmez. Başlığın aynısı olan ilk paragraf, sayfanın H1'i
    olduğu için çıkarılır.
  - Konu sayfaları: Markdown'a çevrilir; hekim dışı (kurum) metinleri
    olduğu için ayrıca elle gözden geçirilir (migration/content-changes.md).

Kullanım (repo kökünden):
    .venv-archive/bin/python migration/make_content.py
"""

import csv
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Comment, NavigableString
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "src" / "content" / "pages"
sys.path.insert(0, str(ROOT))
import inventory  # noqa: E402  (TOPICS, ARTICLES eşleri)

INV = {r["eski_adres"]: r for r in csv.DictReader(open(ROOT / "inventory.csv", encoding="utf-8"))}

# Makalelerin başlık, yazar ve yayın bilgisi (yeni sitenin makale
# listesiyle aynı; yazarlar kaynaktaki imzalardan doğrulandı).
ARTICLE_META = {
    "tr/bir-olgu-nedeniyle-bebek-bezi-fetisizmi": {
        "title": "Bir Olgu Nedeniyle Bebek Bezi Fetişizmi",
        "authors": "Dr. Nihan Oğuz, Dr. Niyazi Uygur",
        "publication": "Türk Psikiyatri Dergisi 2005; 16(2):133–138",
        "description": "Bebek bezi fetişizmi olan bir olgunun hastalık öyküsü ve özgeçmişi çerçevesinde adli ve dinamik açıdan tartışıldığı olgu sunumu.",
    },
    "en/diaper-fetishism-due-to-a-case": {
        "title": "Diaper Fetishism: A Case Report",
        "authors": "Dr. Nihan Oğuz, Dr. Niyazi Uygur",
        "publication": "Turkish Journal of Psychiatry 2005; 16(2):133–138",
        "description": "A case report of diaper fetishism, discussed from forensic and psychodynamic perspectives in the light of the patient’s history.",
    },
    "tr/viral-ensefalite-bagli-deliryum-bir-olgu-sunumu": {
        "title": "Viral Ensefalite Bağlı Deliryum: Bir Olgu Sunumu",
        "authors": "Nihan Oğuz, Cem İlnem, Ferhan Yener",
        "publication": "Düşünen Adam 2005; 18(4):217–223",
        "description": "Davranış değişiklikleri ve deliryumun ön planda olduğu, bu yüzden tanısı kolayca atlanabilen bir viral ensefalit olgusu.",
    },
    "en/delirium-due-to-viral-encephalitis-a-case-report": {
        "title": "Delirium Due to Viral Encephalitis: A Case Report",
        "authors": "Nihan Oğuz, Cem İlnem, Ferhan Yener",
        "publication": "Düşünen Adam 2005; 18(4):217–223",
        "description": "A case of viral encephalitis presenting mainly with behavioural changes and delirium, a picture in which the diagnosis is easily missed.",
    },
    "tr/beyin-tumorlerin-neden-oldugu-psikiyatrik-tablolar-iki-olgu-sunumu": {
        "title": "Beyin Tümörlerinin Neden Olduğu Psikiyatrik Tablolar: İki Olgu Sunumu",
        "authors": "Nihan Oğuz, Cem İlnem, Ferhan Yener",
        "description": "Beyin tümörlerinin yol açabildiği psikiyatrik belirtilerin iki olgu üzerinden ele alındığı olgu sunumu.",
    },
    "en/caused-by-brain-tumors-psychiatric-tables-two-case-reports": {
        "title": "Psychiatric Presentations Caused by Brain Tumours: Two Case Reports",
        "authors": "Nihan Oğuz, Cem İlnem, Ferhan Yener",
        "description": "Two case reports on the psychiatric symptoms that brain tumours can cause.",
    },
    "tr/covid-19-ve-ruhsal-degisim-olmak-ya-da-olmamak": {
        "title": "Covid-19 ve Ruhsal Değişim: Olmak ya da Olmamak!",
        "authors": "Uzm. Dr. Mehmet Oğuz",
        "description": "Pandeminin yarattığı psikolojik baskı ve belirsizlik üzerine, Uzm. Dr. Mehmet Oğuz'un yazısı.",
    },
    "en/covid-19-and-mental-change-to-be-or-not-to-be-": {
        "title": "Covid-19 and Mental Change: To Be or Not To Be!",
        "authors": "Dr Mehmet Oğuz, MD",
        "description": "An essay by Dr Mehmet Oğuz on the psychological pressure and uncertainty created by the pandemic.",
    },
    "tr/hayata-baslangic-bos-bir-tahta-midir": {
        "title": "Hayata Başlangıç Boş Bir Tahta mıdır?",
        "authors": "Uzm. Dr. Nihan Oğuz",
        "description": "Aile, kültür ve kuşaklar arası aktarımın bireyselliğimizi nasıl şekillendirdiği üzerine, Uzm. Dr. Nihan Oğuz'un yazısı.",
    },
}


def old_url(path):
    return "https://www.emdrizmir.com" + path


def link_target(href):
    """Eski sitedeki bir bağlantının yeni sitedeki karşılığı."""
    u = urlsplit(href)
    if u.hostname not in (None, "www.emdrizmir.com", "emdrizmir.com"):
        return href
    row = INV.get(u.path) or INV.get(u.path.rstrip("/"))
    return row["hedef"] if row else href


def content_node(path):
    raw = (ROOT / "live" / (path.lstrip("/") + ".html")).read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "lxml")
    content = soup.select_one("#content-wrap #content")
    first = content.find("div", class_="col-md-12", recursive=False)
    return soup, first if first is not None else content


def clean_html(node, h1):
    """Biçimi temizler, metne dokunmaz."""
    for t in node.select(".col-md-4, script, style, img, #fb-root, .fb-like, .fb-share-button"):
        t.decompose()
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for tag in node.find_all(True):
        keep = {"href"} if tag.name == "a" else set()
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in keep}
        if tag.name == "a" and "href" in tag.attrs:
            tag["href"] = link_target(tag["href"])
        if tag.name in ("span", "font", "div"):
            tag.unwrap()
    blocks = []
    for child in node.children:
        if isinstance(child, NavigableString):
            if child.strip():
                blocks.append(f"<p>{html.escape(str(child).strip())}</p>")
            continue
        text = child.get_text().replace("\u00a0", " ").strip()
        if not text:
            continue  # boş paragraf (&nbsp;)
        blocks.append(str(child))
    # Başlığın aynısı olan ilk blok, sayfada H1 olarak duruyor.
    norm = lambda s: re.sub(r"\s+", " ", BeautifulSoup(s, "lxml").get_text()).strip().casefold()
    if blocks and norm(blocks[0]).rstrip(" .") == h1.casefold().rstrip(" ."):
        blocks = blocks[1:]
    # Word'den gelen art arda boşluklar (liste numarası hizası) tek boşluk olur.
    blocks = [re.sub(r"(?:\u00a0[ \t]*){2,}", " ", b) for b in blocks]
    out = "\n\n".join(b.replace("\u00a0", "&nbsp;") for b in blocks)
    return out


def frontmatter(**kw):
    lines = ["---"]
    for k, v in kw.items():
        if v is None:
            continue
        lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def write(rel, text):
    dest = OUT / (rel + ".md")
    if dest.exists():
        print(f"  = {rel} (var, dokunulmadı)")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    print(f"  + {rel}")


def group_of(lang, slug, pairs):
    for tr, en in pairs:
        if (lang == "tr" and slug == tr) or (lang == "en" and slug == en):
            return tr or en
    raise KeyError((lang, slug))


def old_title(path):
    d = json.loads((ROOT / "live" / (path.lstrip("/") + ".json")).read_text(encoding="utf-8"))
    return re.sub(r"\s+", " ", d["h1"][0]).strip()


def first_sentences(text, limit=155):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def main():
    # Makaleler — HARFİYEN.
    for tr, en in inventory.ARTICLES:
        for lang, slug in (("tr", tr), ("en", en)):
            if not slug:
                continue
            rel = f"{lang}/{slug}"
            meta = ARTICLE_META[rel]
            _, node = content_node("/" + rel)
            body = clean_html(node, meta["title"])
            write(rel, frontmatter(
                kind="makale", group=tr or en, title=meta["title"],
                description=meta["description"], authors=meta.get("authors"),
                publication=meta.get("publication"), source=old_url("/" + rel),
            ) + "\n" + body + "\n")

    # KVKK — HARFİYEN; eski adres ve e-posta içerdiği için onay bekler.
    _, node = content_node("/tr/belgelerimiz")
    body = clean_html(node, "")
    write("tr/belgelerimiz", frontmatter(
        kind="kvkk", group="kvkk", title="Kişisel Veriler Aydınlatma ve Onam Metni",
        description="Dr. Mehmet Oğuz muayenehanesinde kişisel verilerin ve sağlık verilerinin işlenmesine ilişkin KVKK aydınlatma ve onam metni.",
        source=old_url("/tr/belgelerimiz"),
        draft="Metinde eski Alsancak adresi ve oguzmd@yahoo.com geçiyor. Güncel adres ve başvuru e-postası hekim tarafından onaylanmalı.",
    ) + "\n" + body + "\n")

    # Hekimin mektubu — metin i18n sözlüğünden gelir (ana sayfayla tek kaynak).
    write("tr/neden-emdr", frontmatter(
        kind="mektup", group="neden-emdr", title="Neden EMDR",
        description="Uzm. Dr. Mehmet Oğuz, EMDR terapisini neden seçtiğini anlatıyor.",
        source=old_url("/tr/neden-emdr"),
    ))
    write("en/why--emdr", frontmatter(
        kind="mektup", group="neden-emdr", title="Why EMDR",
        description="Dr Mehmet Oğuz explains why he chose to practise EMDR therapy.",
        source=old_url("/en/why--emdr"),
    ))

    # Konu sayfaları — Markdown'a çevrilir, sonra elle gözden geçirilir.
    for tr, en in inventory.TOPICS:
        for lang, slug in (("tr", tr), ("en", en)):
            if not slug:
                continue
            rel = f"{lang}/{slug}"
            title = old_title("/" + rel)
            _, node = content_node("/" + rel)
            body_html = clean_html(node, title)
            md = markdownify(body_html, heading_style="ATX", strip=["a"]).replace("\u00a0", " ")
            md = re.sub(r"[ \t]+\n", "\n", md)
            md = re.sub(r"\n{3,}", "\n\n", md).strip()
            text = BeautifulSoup(body_html, "lxml").get_text(" ")
            write(rel, frontmatter(
                kind="konu", group=tr, title=title,
                description=first_sentences(text), source=old_url("/" + rel),
            ) + "\n" + md + "\n")


if __name__ == "__main__":
    main()
