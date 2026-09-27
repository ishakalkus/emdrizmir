#!/usr/bin/env python3
"""Eski emdrizmir.com sitesini arşivler.

Canlı siteyi dört adres biçiminde (https/http × www/çıplak) tarar, her
sayfanın ham HTML'ini, ayıklanmış alanlarını (başlık, açıklama, canonical,
H1/H2, gövde metni, görseller, iç bağlantılar, belgeler) ve okunabilir bir
Markdown kopyasını kaydeder. Canlıda artık olmayan eski adresleri
archive.org'dan alır. Sonunda bütün adresleri urls.csv'ye yazar.

Kurulum ve çalıştırma (repo kökünden):
    python3 -m venv .venv-archive
    .venv-archive/bin/pip install requests beautifulsoup4 lxml markdownify
    .venv-archive/bin/python migration/archive.py

Eski sunucu "sayfa yok" durumunda 404 değil, 200 ile ana sayfayı döndürür
(soft 404). Betik bunu, var olmayan bir adresin yanıtıyla karşılaştırarak
ayırt eder.
"""

import csv
import hashlib
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent
LIVE = ROOT / "live"
WAYBACK = ROOT / "wayback"
ASSETS = ROOT / "assets"

HOSTS = {"www.emdrizmir.com", "emdrizmir.com"}
BASE = "https://www.emdrizmir.com"
VARIANTS = [
    ("https_www", "https://www.emdrizmir.com"),
    ("https_bare", "https://emdrizmir.com"),
    ("http_www", "http://www.emdrizmir.com"),
    ("http_bare", "http://emdrizmir.com"),
]
HOME_PATHS = {"/", "/tr/", "/en/", "/de/"}
ASSET_EXT = re.compile(
    r"\.(jpe?g|png|gif|svg|webp|bmp|ico|pdf|docx?|xlsx?|pptx?|rtf|txt|zip|mp4|mp3|css|js|woff2?|ttf|eot)$",
    re.I,
)
DOC_EXT = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|rtf|txt|zip|mp4|mp3)$", re.I)
IMG_EXT = re.compile(r"\.(jpe?g|png|gif|svg|webp|bmp|ico)$", re.I)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) emdrizmir-archive/1.0"
DELAY = 0.25

# Arşiv dışı bırakılan archive.org kayıtları: sunucu/tarayıcı gürültüsü.
WAYBACK_SKIP = re.compile(
    r"(/\.well-known/|/robots\.txt$|/sitemap\.xml$|/feed\.xml$|/admin|/_api/|/(next|prev|null)$|/ads\.txt|/app-ads\.txt)"
)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


WAYBACK_DELAY = 4  # archive.org dakikada ~15 isteğin üstünü reddediyor


def get(url, follow=False, timeout=30):
    slow = "web.archive.org" in url
    for attempt in range(3):
        try:
            time.sleep(WAYBACK_DELAY if slow else DELAY)
            return requests.get(
                url,
                allow_redirects=follow,
                timeout=timeout,
                headers={"User-Agent": UA},
            )
        except requests.RequestException as e:
            log(f"  ! {url}: {e.__class__.__name__} (deneme {attempt + 1})")
            time.sleep((30 if slow else 2) * (attempt + 1))
    return None


def norm_path(href, base_url):
    """Site içi bir bağlantıyı yol+sorgu biçimine çevirir; dışsa None."""
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
        return None
    u = urlsplit(urljoin(base_url, href))
    if u.scheme not in ("http", "https") or u.hostname not in HOSTS:
        return None
    path = u.path or "/"
    path = re.sub(r"/{2,}", "/", path)
    return path + (f"?{u.query}" if u.query else "")


def safe_name(path):
    """/tr/panik-atak -> tr/panik-atak ; /tr/ -> tr/index ; / -> index"""
    p, _, q = path.partition("?")
    p = unquote(p).lstrip("/")
    if p == "" or p.endswith("/"):
        p += "index"
    p = re.sub(r"[^\w\-./çğıöşüÇĞİÖŞÜ]", "_", p)
    if q:
        p += "__q_" + re.sub(r"[^\w\-]", "_", unquote(q))
    return p


def lang_of(path):
    m = re.match(r"^/(tr|en|de|fr)(/|$)", path)
    return m.group(1) if m else ""


def text_of(node):
    if node is None:
        return ""
    t = node.get_text("\n")
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in t.splitlines()]
    out, blank = [], False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank and out:
            out.append("")
            blank = True
    return "\n".join(out).strip()


def clean(soup_node):
    for t in soup_node.find_all(["script", "style", "noscript"]):
        t.decompose()
    for c in soup_node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in soup_node.select(".fb-like, .fb-share-button, #fb-root"):
        t.decompose()
    return soup_node


def meta(soup, name):
    for m in soup.find_all("meta"):
        if (m.get("name") or m.get("property") or "").lower() == name:
            return m.get("content", "")
    return ""


def fingerprint(html):
    soup = BeautifulSoup(html, "lxml")
    body = soup.body or soup
    clean(body)
    # Sayfaya özgü tek fark <title> ve logonun title özniteliği; gövdeye bak.
    return hashlib.sha1(text_of(body).encode()).hexdigest()


def main_node(soup, generation):
    if generation == "live":
        n = soup.select_one("#content-wrap")
        if n is not None or soup.body is None:
            return n
        # Ana sayfalarda #content-wrap yok: menüleri at, gerisini (slayt
        # yazıları, bölümler, alt bilgideki iletişim) içerik say.
        for sel in (".wsmenucontainer", ".mobilenone", "#layerslider style"):
            for t in soup.body.select(sel):
                t.decompose()
        return soup.body
    for sel in (
        ".entry-content",
        "article",
        "#content-wrap",
        "#content",
        "main",
        "#SITE_CONTAINER",
        "body",
    ):
        n = soup.select_one(sel)
        if n is not None and text_of(n):
            return n
    return soup.body


def extract(html, url, generation="live"):
    if isinstance(html, bytes):
        html = html.decode("utf-8", "replace")
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.get_text() if soup.title else ""
    canonical = ""
    hreflang = []
    for l in soup.find_all("link"):
        rel = [r.lower() for r in (l.get("rel") or [])]
        if "canonical" in rel:
            canonical = l.get("href", "")
        if "alternate" in rel and l.get("hreflang"):
            hreflang.append({"hreflang": l["hreflang"], "href": l.get("href", "")})

    # Sayfa geneli bağlantılar ve görseller (menü dahil).
    all_links = []
    for a in soup.find_all("a", href=True):
        all_links.append({"href": a["href"], "text": text_of(a)})
    internal = OrderedDict()
    documents = OrderedDict()
    for a in all_links:
        p = norm_path(a["href"], url)
        if not p:
            continue
        if DOC_EXT.search(p.split("?")[0]) or (
            p.startswith("/upload/") and not IMG_EXT.search(p.split("?")[0])
        ):
            documents.setdefault(p, a["text"])
        elif not ASSET_EXT.search(p.split("?")[0]):
            internal.setdefault(p, a["text"])

    page_images = OrderedDict()
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        p = norm_path(src, url) if src else None
        if p:
            page_images.setdefault(p, img.get("alt", ""))
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", html):
        p = norm_path(m.group(1), url)
        if p and IMG_EXT.search(p.split("?")[0]):
            page_images.setdefault(p, "")

    h1_all = [text_of(h) for h in soup.find_all("h1")]

    main = main_node(soup, generation)
    main_html = ""
    main_text = ""
    content_images, content_links, iframes, h2, h3 = [], [], [], [], []
    if main is not None:
        clean(main)
        main_html = str(main)
        main_text = text_of(main)
        for img in main.find_all("img"):
            src = img.get("src") or img.get("data-src") or ""
            content_images.append(
                {"src": src, "path": norm_path(src, url), "alt": img.get("alt", "")}
            )
        for a in main.find_all("a", href=True):
            content_links.append({"href": a["href"], "text": text_of(a)})
        for f in main.find_all(["iframe", "embed", "video", "source"]):
            if f.get("src"):
                iframes.append(f["src"])
        h2 = [text_of(h) for h in main.find_all("h2")]
        h3 = [text_of(h) for h in main.find_all("h3")]

    crumbs = []
    bc = soup.select_one("#breadcrumb")
    if bc:
        crumbs = [text_of(li) for li in bc.find_all("li")]

    return {
        "url": url,
        "generation": generation,
        "html_lang": (soup.html.get("lang", "") if soup.html else ""),
        "title": title,
        "title_clean": re.sub(r"\s+", " ", title.replace(" ", " ")).strip(),
        "meta_description": meta(soup, "description"),
        "meta_keywords": meta(soup, "keywords"),
        "og_title": meta(soup, "og:title"),
        "og_description": meta(soup, "og:description"),
        "canonical": canonical,
        "hreflang": hreflang,
        "robots": meta(soup, "robots"),
        "h1": h1_all,
        "h2": h2,
        "h3": h3,
        "breadcrumb": crumbs,
        "body_text": main_text,
        "word_count": len(main_text.split()),
        "content_images": content_images,
        "content_links": content_links,
        "embeds": iframes,
        "internal_links": [{"path": p, "text": t} for p, t in internal.items()],
        "documents": [{"path": p, "text": t} for p, t in documents.items()],
        "page_images": [{"path": p, "alt": t} for p, t in page_images.items()],
        "_main_html": main_html,
    }


def write_page(folder, path, raw, data, extra):
    return write_files(folder / safe_name(path), raw, data, extra)


def write_files(base, raw, data, extra):
    base.parent.mkdir(parents=True, exist_ok=True)
    (base.parent / (base.name + ".html")).write_bytes(raw)
    main_html = data.pop("_main_html")
    data.update(extra)
    (base.parent / (base.name + ".json")).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    md = markdownify(main_html, heading_style="ATX", strip=["span"]) if main_html else ""
    md = re.sub(r"\n{3,}", "\n\n", md.replace(" ", " ")).strip()
    fm = [
        "---",
        f"url: {data['url']}",
        f"title: {json.dumps(data['title_clean'], ensure_ascii=False)}",
        f"meta_description: {json.dumps(data['meta_description'], ensure_ascii=False)}",
        f"canonical: {json.dumps(data['canonical'])}",
        f"h1: {json.dumps(data['h1'], ensure_ascii=False)}",
    ]
    for k in ("status", "wayback_timestamp", "archived_at"):
        if k in data:
            fm.append(f"{k}: {data[k]}")
    fm.append("---")
    (base.parent / (base.name + ".md")).write_text(
        "\n".join(fm) + "\n\n" + md + "\n", encoding="utf-8"
    )
    return str((base.parent / (base.name + ".html")).relative_to(ROOT))


def variant_statuses(path):
    out = {}
    for key, origin in VARIANTS:
        r = get(origin + path)
        if r is None:
            out[key] = ("ERR", "")
        else:
            out[key] = (r.status_code, r.headers.get("Location", ""))
            r.close()
    return out


def load_redirects():
    rules = {}
    f = ROOT.parent / "public" / "_redirects"
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            rules.setdefault(parts[0], parts[1])
    return rules


def redirect_target(path, rules):
    p = path.split("?")[0]
    if p in rules:
        return rules[p], p
    for src, dst in rules.items():
        if src.endswith("*") and p.startswith(src[:-1]):
            return dst, src
    return "", ""


def wayback_index():
    """archive.org'daki HTML kayıtları: yol -> [(timestamp, original)]"""
    url = (
        "https://web.archive.org/cdx/search/cdx?url=emdrizmir.com&matchType=domain"
        "&output=json&fl=original,statuscode,mimetype,timestamp&limit=20000"
    )
    r = get(url, follow=True, timeout=120)
    cache = ROOT / "wayback-cdx.json"
    if r is not None and r.ok:
        rows = r.json()[1:]
    elif cache.exists():
        log("! archive.org dizini alınamadı, önceki wayback-cdx.json kullanılıyor")
        rows = json.loads(cache.read_text(encoding="utf-8"))
    else:
        sys.exit("archive.org dizini alınamadı; arşiv eksik kalmasın diye durduruldu.")
    idx = {}
    for original, status, mime, ts in rows:
        u = urlsplit(original)
        if u.hostname not in HOSTS or WAYBACK_SKIP.search(u.path):
            continue
        if mime != "text/html" and mime != "warc/revisit":
            continue
        if ASSET_EXT.search(u.path):
            continue
        path = (u.path or "/") + (f"?{u.query}" if u.query else "")
        idx.setdefault(path, []).append((ts, original, status))
    return idx, rows


def wix_2017(rows, started):
    """2017'deki Wix sürümü.

    Wix sayfaları tarayıcıda çalışan bir uygulama olduğu için archive.org
    kopyalarında metin yok. Blog yazılarının tam metni ise RSS akışında
    (feed.xml) duruyor; site haritası da o dönemin adreslerini veriyor.
    Dönen değer: yol -> (kaynak, dosya).
    """
    out = WAYBACK / "wix-2017"
    found = OrderedDict()

    def latest(path):
        caps = [
            (ts, orig) for orig, st, mime, ts in rows
            if st == "200" and urlsplit(orig).path == path and "xml" in mime
        ]
        return max(caps) if caps else None

    for path, name in (("/sitemap.xml", "sitemap.xml"), ("/feed.xml", "feed.xml")):
        cap = latest(path)
        if not cap:
            continue
        r = get(f"https://web.archive.org/web/{cap[0]}id_/{cap[1]}", follow=True, timeout=60)
        if r is None or r.status_code != 200:
            continue
        out.mkdir(parents=True, exist_ok=True)
        (out / name).write_bytes(r.content)
        root = ET.fromstring(r.content)
        if name == "sitemap.xml":
            for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                p = urlsplit(loc.text.strip()).path or "/"
                found.setdefault(p, ("wix-2017 sitemap", ""))
            continue
        for it in root.iter("item"):
            link = it.findtext("link") or ""
            p = urlsplit(link).path
            enc = it.find("{http://purl.org/rss/1.0/modules/content/}encoded")
            body = enc.text if enc is not None and enc.text else it.findtext("description") or ""
            slug = unquote(p.rsplit("/", 1)[-1])[:80]
            date = p.split("/")[2:5]
            f = out / ("-".join(date) + "_" + re.sub(r"[^\w\-]", "_", slug) + ".md")
            md = markdownify(body, heading_style="ATX").replace(" ", " ")
            fm = [
                "---",
                f"url: {link}",
                f"title: {json.dumps(it.findtext('title') or '', ensure_ascii=False)}",
                f"author: {json.dumps(it.findtext('{http://purl.org/dc/elements/1.1/}creator') or '', ensure_ascii=False)}",
                f"published: {it.findtext('pubDate') or ''}",
                f"source: archive.org {cap[0]} feed.xml",
                f"archived_at: {started}",
                "---",
            ]
            f.write_text("\n".join(fm) + "\n\n" + re.sub(r"\n{3,}", "\n\n", md).strip() + "\n", encoding="utf-8")
            found[p] = ("wix-2017 feed", str(f.relative_to(ROOT)))
    return found


def load_search_index():
    idx = {}
    f = ROOT / "search-index" / "resolved.csv"
    if f.exists():
        for row in csv.DictReader(open(f, encoding="utf-8")):
            idx.setdefault(row["path"], set()).add(row["engine"])
    return idx


def main():
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rules = load_redirects()

    # 1) "Sayfa yok" yanıtının parmak izi (her dil öneki için).
    soft = set()
    for prefix in ("/", "/tr/", "/en/", "/de/", "/fr/"):
        r = get(f"{BASE}{prefix}bu-sayfa-yok-arsiv-kontrol-{int(time.time())}")
        if r is not None and r.status_code == 200:
            soft.add(fingerprint(r.content))
    home_fp = {}
    for hp in HOME_PATHS:
        r = get(BASE + hp)
        if r is not None and r.status_code == 200:
            home_fp[fingerprint(r.content)] = hp
    log(f"soft-404 parmak izleri: {len(soft)}, ana sayfalar: {len(home_fp)}")

    # 2) Tohumlar: ana sayfalar, _redirects kaynakları, archive.org adresleri.
    wb_idx, wb_rows = wayback_index()
    log(f"archive.org HTML adresi: {len(wb_idx)}")
    seeds = OrderedDict()
    for p in ["/", "/tr/", "/en/", "/de/", "/fr/"]:
        seeds[p] = "seed"
    for src in rules:
        if "*" not in src:
            seeds.setdefault(src, "_redirects")
    for p in wb_idx:
        seeds.setdefault(p, "archive.org")
    for line in (ROOT / "extra-seeds.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            p, _, src = line.partition("\t")
            seeds.setdefault(p.strip(), src.strip() or "extra-seeds")
    search_idx = load_search_index()
    for p in search_idx:
        seeds.setdefault(p, "search-index")
    wix = wix_2017(wb_rows, started)
    log(f"wix-2017 adresi: {len(wix)}")
    for p, (src, _) in wix.items():
        seeds.setdefault(p, src)

    queue = list(seeds.items())
    seen = {}
    records = OrderedDict()
    assets = OrderedDict()

    while queue:
        path, source = queue.pop(0)
        if path in seen:
            continue
        seen[path] = source
        url = BASE + path
        r = get(url)
        if r is None:
            records[path] = {"path": path, "source": source, "final_status": "ERR"}
            continue
        rec = {"path": path, "source": source, "https_www": r.status_code}
        if r.is_redirect:
            rec["location"] = r.headers.get("Location", "")
            loc = norm_path(rec["location"], url)
            if loc and loc not in seen:
                queue.append((loc, f"redirect from {path}"))
        rec["classification"] = ""
        if r.status_code == 200 and "html" in r.headers.get("Content-Type", ""):
            fp = fingerprint(r.content)
            if path in HOME_PATHS:
                rec["classification"] = "home"
            elif fp in home_fp or fp in soft:
                rec["classification"] = "soft404"
                rec["same_as"] = home_fp.get(fp, "")
            else:
                rec["classification"] = "page"
            data = extract(r.content, url)
            rec["data"] = data
            if rec["classification"] in ("page", "home"):
                for l in data["internal_links"]:
                    if l["path"] not in seen:
                        queue.append((l["path"], f"link from {path}"))
                for i in data["page_images"]:
                    assets.setdefault(i["path"], path)
                for d in data["documents"]:
                    assets.setdefault(d["path"], path)
                rec["raw"] = r.content
        elif r.status_code == 404:
            rec["classification"] = "404"
        records[path] = rec
        log(f"{r.status_code} {rec['classification']:8} {path}")

    # 3) Dört adres biçimi.
    log("adres biçimleri kontrol ediliyor…")
    todo = [p for p in records if not ASSET_EXT.search(p.split("?")[0])]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for path, v in zip(todo, pool.map(variant_statuses, todo)):
            records[path]["variants"] = v

    # 4) Sayfaları yaz.
    for path, rec in records.items():
        if "raw" in rec:
            rec["file"] = write_page(
                LIVE,
                path,
                rec.pop("raw"),
                rec["data"],
                {
                    "status": rec["https_www"],
                    "classification": rec["classification"],
                    "variants": {k: list(v) for k, v in rec.get("variants", {}).items()},
                    "archived_at": started,
                },
            )

    # 5) Canlıda olmayanlar için archive.org.
    live_ok = {p for p, r in records.items() if r.get("classification") in ("page", "home")}
    live_ok_norm = {p.rstrip("/") for p in live_ok}
    for path, caps in wb_idx.items():
        rec = records.get(path)
        if path in live_ok or path.rstrip("/") in live_ok_norm:
            if rec is not None:
                rec["wayback_latest"] = max(c[0] for c in caps)
            continue
        # En yeni kayıttan geriye doğru, içeriği gerçek olan ilk kopyayı al.
        # 2021 sonrası kopyaların çoğu, eski adresin yeni sistemde ana
        # sayfaya düştüğü "soft 404" hâlidir (layerslider = ana sayfa).
        good = sorted({c for c in caps if c[2] == "200"}, reverse=True)
        wr = None
        for ts, original, _ in good[:8]:
            cand = get(f"https://web.archive.org/web/{ts}id_/{original}", follow=True, timeout=60)
            if cand is None or cand.status_code != 200:
                continue
            if b"layerslider" in cand.content and path not in HOME_PATHS:
                continue
            if len(cand.content.strip()) < 200:  # 2019'da sunucu boş yanıt vermiş
                continue
            wr = cand
            break
        if wr is None:
            if good:
                log(f"  ! archive.org'da gerçek içerik yok: {path}")
                rec = records.setdefault(path, {"path": path, "source": "archive.org"})
                rec["wayback_latest"] = good[0][0]
                rec["wayback_title"] = "(boş ya da yalnızca ana sayfa kopyası)"
            continue
        data = extract(wr.content, original, generation="wayback")
        for i in data["page_images"]:
            assets.setdefault(i["path"], "wayback:" + path)
        f = write_page(
            WAYBACK,
            path,
            wr.content,
            data,
            {"wayback_timestamp": ts, "wayback_url": f"https://web.archive.org/web/{ts}/{original}", "archived_at": started},
        )
        rec = records.setdefault(path, {"path": path, "source": "archive.org"})
        rec["wayback_latest"] = ts
        rec["wayback_file"] = f
        rec["wayback_title"] = data["title_clean"]
        rec["wayback_words"] = data["word_count"]
        log(f"WB {ts} {path}")

    # 6) Görseller ve belgeler (canlı sunucudan; yoksa archive.org'dan).
    log(f"varlık indiriliyor: {len(assets)}")
    asset_rows = []
    extra = []
    for p in list(assets):
        if "/thumbs/" in p:
            extra.append(p.replace("/thumbs/", "/", 1))
    for p in extra:
        assets.setdefault(p, "full-size of thumb")
    wb_assets = {}
    for original, st, mime, ts in wb_rows:
        u = urlsplit(original)
        if st == "200" and mime != "text/html" and u.hostname in HOSTS:
            wb_assets.setdefault(u.path, []).append((ts, original))
    for p, ref in assets.items():
        dest = ASSETS / unquote(p.split("?")[0]).lstrip("/")
        status, origin = "", "live"
        if dest.exists():
            status = "cached"
        else:
            r = get(BASE + p, follow=True)
            ok = r is not None and r.status_code == 200 and "text/html" not in r.headers.get("Content-Type", "")
            if not ok:
                caps = sorted(wb_assets.get(p.split("?")[0], []), reverse=True)
                # Yalnızca archive.org dizininde gerçekten kaydı olanları iste.
                tries = [f"https://web.archive.org/web/{ts}id_/{o}" for ts, o in caps[:2]]
                for t in tries:
                    r = get(t, follow=True, timeout=60)
                    ok = r is not None and r.status_code == 200 and "text/html" not in r.headers.get("Content-Type", "")
                    if ok:
                        break
                origin = "archive.org"
            if ok:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(r.content)
                status = "ok"
            else:
                status = f"missing ({r.status_code if r is not None else 'ERR'})"
                origin = ""
        asset_rows.append({"path": p, "file": str(dest.relative_to(ROOT)) if dest.exists() else "", "status": status, "origin": origin, "first_seen_on": ref})

    # 7) CSV'ler.
    cols = [
        "path", "lang", "source", "classification", "https_www", "location",
        "https_bare", "http_www", "http_bare", "title", "h1", "meta_description",
        "canonical", "word_count", "documents", "redirect_rule", "redirect_target",
        "live_file", "wayback_latest", "wayback_file", "wayback_title", "wayback_words",
        "wix2017_file", "google", "duckduckgo",
    ]
    with open(ROOT / "urls.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for path in sorted(records, key=lambda p: (lang_of(p) or "zz", p)):
            rec = records[path]
            d = rec.get("data", {})
            v = rec.get("variants", {})
            tgt, rule = redirect_target(path, rules)

            def vs(k):
                if k not in v:
                    return ""
                s, loc = v[k]
                return f"{s} → {loc}" if loc else str(s)

            w.writerow({
                "path": path,
                "lang": lang_of(path),
                "source": rec.get("source", ""),
                "classification": rec.get("classification", "wayback-only" if "wayback_file" in rec else ""),
                "https_www": rec.get("https_www", ""),
                "location": rec.get("location", ""),
                "https_bare": vs("https_bare"),
                "http_www": vs("http_www"),
                "http_bare": vs("http_bare"),
                "title": d.get("title_clean", "") if rec.get("classification") in ("page", "home") else "",
                "h1": " | ".join(d.get("h1", [])) if rec.get("classification") in ("page", "home") else "",
                "meta_description": d.get("meta_description", "") if rec.get("classification") in ("page", "home") else "",
                "canonical": d.get("canonical", ""),
                "word_count": d.get("word_count", "") if rec.get("classification") in ("page", "home") else "",
                "documents": " ".join(x["path"] for x in d.get("documents", [])) if rec.get("classification") in ("page", "home") else "",
                "redirect_rule": rule,
                "redirect_target": tgt,
                "live_file": rec.get("file", ""),
                "wayback_latest": rec.get("wayback_latest", ""),
                "wayback_file": rec.get("wayback_file", ""),
                "wayback_title": rec.get("wayback_title", ""),
                "wayback_words": rec.get("wayback_words", ""),
                "wix2017_file": wix.get(path, ("", ""))[1],
                "google": "evet" if "google" in search_idx.get(path, ()) else "",
                "duckduckgo": "evet" if "duckduckgo" in search_idx.get(path, ()) else "",
            })
    with open(ROOT / "assets.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["path", "file", "status", "origin", "first_seen_on"])
        w.writeheader()
        w.writerows(asset_rows)
    with open(ROOT / "wayback-cdx.json", "w", encoding="utf-8") as fh:
        json.dump(wb_rows, fh, ensure_ascii=False, indent=0)
    log("bitti")


def reextract():
    """Kayıtlı ham HTML'den .json ve .md'yi yeniden üretir; ağa çıkmaz."""
    for folder, gen in ((LIVE, "live"), (WAYBACK, "wayback")):
        for j in sorted(folder.rglob("*.json")):
            old = json.loads(j.read_text(encoding="utf-8"))
            raw = j.with_suffix(".html").read_bytes()
            data = extract(raw, old["url"], generation=gen)
            keep = {k: v for k, v in old.items() if k not in data}
            write_files(j.with_suffix(""), raw, data, keep)
            log(f"{data['word_count']:6} {j.relative_to(ROOT)}")


if __name__ == "__main__":
    reextract() if "--reextract" in sys.argv else main()
