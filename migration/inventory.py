#!/usr/bin/env python3
"""Eski adres envanteri: her eski adres için yeni sitede ne olacağı.

Girdi: urls.csv (archive.py çıktısı) ve public/_redirects.
Çıktı: inventory.csv.

Karar türleri:
  yeni-sayfa  Aynı adreste, yeni tasarımla ayrı sayfa olarak yayınlanır.
  301         Hedefe kalıcı yönlendirilir.
  404         Bırakılır (yeni sitede gerçek 404).

Varsayılan (Search Console verisi gelene kadar, HANDOFF.md): konu
sayfaları, makaleler ve KVKK sayfası korunur. Geri kalan her adres en
yakın ilgili sayfaya ya da ana sayfa bölümüne gider. Bir kararı
değiştirmek için aşağıdaki tabloları düzenleyip betiği yeniden çalıştırın:
    python3 migration/inventory.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ── Korunacak sayfalar ve dil eşleri (hreflang) ────────────────────────
# Her satır bir sayfanın dillerdeki adresleri; olmayan dil None.
# TR ↔ EN eşleşmesi başlıkların çevirisine göre yapıldı.
TOPICS = [
    ("kaygi-bozukluklari", "anxiety-disorders"),
    ("panik-atak", "panic-attack"),
    ("depresyon", None),
    ("travma-sonrasi-stres-bozuklugu", "post-traumatic-stress-disorder"),
    ("kisilik-bozukluklari", "personality-disorder"),
    ("obsesif--kompulsif-bozukluk", "obsessive-compulsive-disorder"),
    ("yeme-bozukluklari", "eating-disorders"),
    ("psikosomatik-bozukluklar", "psychosomatic-disorders"),
    ("uyum-problemleri", "adaptation-problems"),
    ("davranis-bozukluklari", "behaviour-disorders"),
    ("ayrilik-kaygisi", "separation-anxiety"),
    ("ofke-kontrolu", "anger-management"),
    ("stresle-basa-cikma-ve-ofke-kontrolu", "coping-with-stress-and-anger-management"),
    ("cinsel-sorunlar", "sexual-problems"),
    ("yas-sureci", "the-mourning-process"),
    ("iliski-ve-evlilik-sorunlari", "relationship-and-marriage-problems"),
    ("aile-iliskileri", "family-relations"),
    ("is-yasamina-iliskin-sorunlar", "problems-regarding-business-life"),
    ("ders-basarisizligi-ve-sinav-kaygisi", "course-failure-and-exam-anxiety"),
    ("okula-uyum", None),
    ("hamilelik-sureci-ve-sonrasi--depresyon", "the-pregnancy-process-and-its-consequences---depression"),
]
ARTICLES = [
    ("bir-olgu-nedeniyle-bebek-bezi-fetisizmi", "diaper-fetishism-due-to-a-case"),
    ("viral-ensefalite-bagli-deliryum-bir-olgu-sunumu", "delirium-due-to-viral-encephalitis-a-case-report"),
    ("beyin-tumorlerin-neden-oldugu-psikiyatrik-tablolar-iki-olgu-sunumu", "caused-by-brain-tumors-psychiatric-tables-two-case-reports"),
    ("covid-19-ve-ruhsal-degisim-olmak-ya-da-olmamak", "covid-19-and-mental-change-to-be-or-not-to-be-"),
    ("hayata-baslangic-bos-bir-tahta-midir", None),
]
KVKK = [("belgelerimiz", None)]
# Hekimin mektubu. Kullanıcı kararı (28.09.2026): Google'da indeksli ve
# metin hazır; ayrı sayfa olur, ana sayfada kısa bölüm ve bağlantı kalır.
LETTER = [("neden-emdr", "why--emdr")]

# Hizmet sayfaları. Eski sitede içleri boştu ama Google'da indeksliler;
# kullanıcı kararı (28.09.2026): dört dilde, yeni metinle yayınlanır.
# TR ve DE eski adreslerinde (DE eskisi gibi Türkçe slug'lı) kalır. EN ve
# FR eski sitede hiç olmadı; adresleri yeni ve kendi dillerinde.
SERVICE_PAGES = [
    # (TR/DE eski slug, EN yeni slug, FR yeni slug)
    ("bireysel-yetiskin-psikoterapisi", "individual-adult-psychotherapy", "psychotherapie-individuelle-adulte"),
    ("cift-aile-terapisi", "couple-and-family-therapy", "therapie-de-couple-et-de-famille"),
    ("cocuk-ve-ergen-terapisi-", "child-and-adolescent-therapy", "therapie-enfant-et-adolescent"),
    ("online-bireysel-terapi", "online-individual-therapy", "therapie-individuelle-en-ligne"),
    ("psikoterapi-ve-psikolojik-danismanlik-hizmetleri", "psychotherapy-and-psychological-counselling", "psychotherapie-et-accompagnement-psychologique"),
    ("sanal-gerceklik-vr-ile-alistirma--exposure-tedavisi", "virtual-reality-exposure-therapy", "therapie-exposition-realite-virtuelle"),
]
SERVICES = [tr for tr, _, _ in SERVICE_PAGES]

GROUPS = []  # (tür, {dil: slug})
for kind, pairs in (("konu", TOPICS), ("makale", ARTICLES), ("kvkk", KVKK), ("mektup", LETTER)):
    GROUPS += [(kind, {"tr": tr, "en": en}) for tr, en in pairs]
GROUPS += [("hizmet", {"tr": tr, "de": tr, "en": en, "fr": fr}) for tr, en, fr in SERVICE_PAGES]

# Eski sitede hiç olmamış, yeni açılan adresler: envanterde satırları
# yok, yalnızca eski sayfaların dil eşi olarak görünürler.
NEW_ONLY = {f"/en/{en}" for _, en, _ in SERVICE_PAGES} | {f"/fr/{fr}" for _, _, fr in SERVICE_PAGES}

KEEP = {}  # yol -> (tür, hreflang eşleri)
for kind, langs in GROUPS:
    urls = {lang: f"/{lang}/{slug}" for lang, slug in langs.items() if slug}
    for lang, url in urls.items():
        KEEP[url] = (kind, " ".join(u + "/" for l, u in urls.items() if l != lang))

# ── Yönlendirmeler: yol -> (tür, hedef, gerekçe) ──────────────────────
R = {}


def rd(kind, target, why, *paths):
    for p in paths:
        assert p not in R, p
        R[p] = (kind, target, why)


# Dil kökleri
rd("ana-sayfa", "/", "Yeni sitede Türkçe ana sayfa kökte.", "/tr/", "/tr")
rd("ana-sayfa", "/en/", "Sonda / eksik.", "/en")
rd("ana-sayfa", "/de/", "Sonda / eksik.", "/de")
rd("ana-sayfa", "/fr/", "Sonda / eksik.", "/fr")

# Aynı sayfanın yazım farkları
rd("makale", "/tr/viral-ensefalite-bagli-deliryum-bir-olgu-sunumu/",
   "Eski yazım hatalı adres (baglideliryum).", "/tr/viral-ensefalite-baglideliryum-bir-olgu-sunumu")
rd("makale", "/tr/covid-19-ve-ruhsal-degisim-olmak-ya-da-olmamak/",
   "Aynı yazının sonu tireli eski adresi.", "/tr/covid-19-ve-ruhsal-degisim-olmak-ya-da-olmamak-")

# Eski Almanca menü hizmetlere /en/ altında Türkçe slug'la bağlanıyordu;
# bu adreslerde hiç sayfa olmadı. Artık aynı hizmetin EN sayfasına gider.
for tr, en, _ in SERVICE_PAGES:
    rd("kirik-baglanti", f"/en/{en}/",
       "Eski Almanca menüdeki kırık bağlantı; aynı hizmetin İngilizce sayfası.", f"/en/{tr}")

# Kurumsal, ekip
why_team = "Yeni ana sayfanın ekip bölümü."
rd("kurumsal", "/#ekip", why_team, "/tr/kurumsal", "/tr/hakkimizda", "/tr/ekibimiz")
rd("kurumsal", "/en/#ekip", why_team, "/en/corporate", "/en/about-us", "/en/our-team")
rd("kurumsal", "/de/#ekip", why_team, "/de/uber-uns", "/de/unser-team")
rd("kirik-baglanti", "/en/#ekip", "Eski Almanca menüdeki kırık bağlantı.", "/en/institution")

# Blog sayfalarında yalnızca hekimin "Neden EMDR" mektubu vardı.
why_blog = "Eski blogda yalnızca 'Neden EMDR' mektubu vardı."
rd("mektup", "/tr/neden-emdr/", why_blog, "/tr/blog")
rd("mektup", "/en/why--emdr/", why_blog, "/en/blog")
rd("mektup", "/de/#neden", why_blog + " Almanca mektup ana sayfada.", "/de/blog")
rd("kirik-baglanti", "/en/why--emdr/", "Eski Almanca menüdeki kırık bağlantı.", "/en/neden-emdr")

# Liste sayfaları
rd("liste", "/#makaleler", "Makale listesi; yeni ana sayfada makaleler bölümü.", "/tr/makalelerimiz")
rd("liste", "/en/#makaleler", "Makale listesi; yeni ana sayfada makaleler bölümü.", "/en/articles")
rd("liste", "/de/#makaleler", "Makale listesi; yeni ana sayfada makaleler bölümü.", "/de/unsere-artikel")
rd("kirik-baglanti", "/en/#makaleler", "Eski Almanca menüdeki kırık bağlantı.", "/en/unsere-artikel")
rd("liste", "/#hizmetler", "Çalışma alanları listesi.", "/tr/calisma-alanlarimiz")
rd("liste", "/en/#hizmetler", "Çalışma alanları listesi.", "/en/study-areas")
rd("liste", "/de/#hizmetler", "Çalışma alanları listesi.", "/de/unsere-studienbereiche")
rd("kirik-baglanti", "/en/#hizmetler", "Eski Almanca menüdeki kırık bağlantı.", "/en/unsere-studienbereiche")

# İletişim ve randevu
why_contact = "Yeni ana sayfanın iletişim ve randevu bölümü."
rd("iletisim", "/#iletisim", why_contact, "/tr/iletisim", "/tr/randevu-formu")
rd("iletisim", "/en/#iletisim", why_contact, "/en/contact", "/en/appointment-form")
rd("iletisim", "/de/#iletisim", why_contact, "/de/kontakt", "/de/terminformular")
rd("kirik-baglanti", "/en/#iletisim", "Eski Almanca menüdeki kırık bağlantı.", "/en/kontakt")

# İçi boş ya da karşılığı olmayan sayfalar
why_empty = "Eski sayfa boştu; yeni sitede karşılığı yok."
rd("medya", "/", why_empty + " (Videolar'da yalnızca tek YouTube videosu vardı.)",
   "/tr/medya", "/tr/videolar")
rd("medya", "/en/", why_empty, "/en/media", "/en/videos", "/en/documents")
rd("medya", "/de/", why_empty, "/de/medien", "/de/videos", "/de/unsere-dokumente")

# Danışan yorumları: Yönetmelik md. 5/1/e gereği kaldırıldı.
why_rev = "Danışan yorumları Yönetmelik md. 5/1/e gereği yayınlanmıyor."
rd("yorum", "/", why_rev, "/tr/danisan-yorumlari")
rd("yorum", "/en/", why_rev, "/en/client-comments")
rd("yorum", "/de/", why_rev + " (Almanca menüdeki bu bağlantı zaten kırıktı.)", "/de/client-comments")

# ── Eski sürümlerden kalan kök adresler (2017 Wix, 2018, 2019–2021) ───
# Bunlar yıllardır 404 ya da soft 404. Sıralama değeri büyük ölçüde
# gitmiş olsa da eski bağlantılardan gelen ziyaretçi için en yakın
# sayfaya yönlendiriliyor. DuckDuckGo bir kısmını hâlâ gösteriyor.
def old(target, why, *paths):
    rd("eski-surum", target, why, *paths)


old("/tr/panik-atak/", "Aynı konu.", "/panik-atak/", "/panik-bozukluk")
old("/tr/kaygi-bozukluklari/", "Aynı konu.", "/kaygi-anksiyete-bozukluklari/", "/kaygi-bozukluklari")
old("/tr/kaygi-bozukluklari/", "Sosyal fobi bir kaygı bozukluğu.",
    "/sosyal-fobi-tedavisinde-emdr-gucu", "/sosyal-fobi-tedavisinde-emdr-gucu-emdr/")
old("/tr/ders-basarisizligi-ve-sinav-kaygisi/", "Sınav kaygısı konusu.",
    "/yuksek-duzeydeki-sinav-kaygisi-ile-bas-etmenin-yollari",
    "/yuksek-duzeydeki-sinav-kaygisi-ile-bas-etmenin-yollari-ve-emdr-emdr/")
old("/tr/ders-basarisizligi-ve-sinav-kaygisi/", "En yakın konu (öğrenme güçlüğü).", "/oegrenme-bozukluklari")
old("/tr/depresyon/", "Aynı konu.", "/depresyonla-yasamak-zorunda-degiliz/")
old("/tr/cinsel-sorunlar/", "Aynı konu.", "/cinsel-sorunlar-ve-cinsel-terapi/", "/cinsel-islev-bozukluklari")
old("/tr/travma-sonrasi-stres-bozuklugu/", "Travma konusu.",
    "/cinsel-istismara-bagli-travmalarda-emdr-terapisinin-basarisi/",
    "/emdr-tedavisinin-ruhsal-travmalardaki-etkisi",
    "/emdr-tedavisinin-ruhsal-travmalardaki-etkisi-emdr/",
    "/tssb", "/travma-sonrasi-stres-bozuklugiu")
old("/tr/psikosomatik-bozukluklar/", "Bedensel belirtilerle giden bozukluklar = psikosomatik.",
    "/bedensel-belirtilerle-giden-psikiyatrik-bozukluklarda-emdr-tedavisi",
    "/bedensel-belirtilerle-giden-psikiyatrik-bozukluklarda-emdr-tedavisi-emdr/")
old("/tr/obsesif--kompulsif-bozukluk/", "Aynı konu.", "/obsesif-kompulsif-bozukluk")
old("/tr/yeme-bozukluklari/", "Aynı konu.", "/yeme-bozukluklari")
old("/tr/uyum-problemleri/", "Aynı konu.", "/uyum-bozukluklari")
old("/#hizmetler", "Konu listesinde var ya da en yakın bölüm hizmetler.",
    "/hizmetlerimiz", "/bipolar-bozukluk", "/dikkat-eksikligi-hiperaktivite-bozu",
    "/sizofreni-ve-psikotik-bozukluklar", "/alkol-ve-madde-bagimliligi",
    "/internet-ve-oyun-bagimliligi", "/kumar-bagimliligi")
old("/tr/bireysel-yetiskin-psikoterapisi/", "Şema terapi bireysel psikoterapide kullanılan bir yöntem.",
    "/sema-terapisi-nedir-nasil-uygulanir-", "/sema-terapisi-nedir-nasil-uygulanir/")
old("/#emdr", "EMDR'yi anlatan yazılar; yeni ana sayfada 'EMDR nedir' bölümü.",
    "/emdr-nedir", "/emdr-nedir/",
    "/emdr-nin-tanimi-ve-1980-lerden-gunumuze-dunyadaki-yeri",
    "/emdr-nin-tanimi-ve-1980-lerden-gunumuze-dunyadaki-yeri/",
    "/emdr-terapisinde-grup-tedavisi-mumkun-mu-", "/emdr-terapisinde-grup-tedavisi-mumkun-mu/",
    "/madde-ve-alkol-bagimliligi-icin-yeni-populer-yontem-emdr-psikoterapisi/")
old("/#protokol", "Seans süresi ve sıklığı; yeni ana sayfada seans akışı bölümü.",
    "/seans-sureleri-ve-sikligi", "/seans-sureleri-ve-sikligi/")
old("/tr/neden-emdr/", "Hekimin mektubu.", "/neden-emdr", "/neden-emdr/")
old("/#ekip", "Hekim ve ekip tanıtımı.", "/hakkimda", "/hakkimizda/", "/ekibimiz", "/ekibimiz/",
    "/psikiyatri-nedir-psikiyatrist-kimdir/", "/psikiyatri-2")
old("/#ekip", "2018'de hekimin belgeleri (sertifika görselleri) vardı; KVKK metni değil.",
    "/belgelerimiz", "/belgelerimiz/")
old("/#iletisim", "İletişim ve randevu.", "/iletisim", "/iletisim/", "/online-randevu-al",
    "/randevu", "/sorulafr")
old("/#makaleler", "Blog ve makale listesi.", "/makaleler", "/blog", "/blog/",
    "/soner-yalcin-in-karakutu-isimli-kitabina-psikiyatri-ve-psikoloji-bilimi-adina-tepkimiz/")
old("/", "Boş medya sayfası.", "/medya", "/medya/")
old("/", "Ücret üzerine mektup; yeni sitede karşılığı yok.", "/bir-soru-ustune", "/bir-soru-uzerine/")
old("/", "İçeriği hiçbir kaynakta kalmamış.", "/daha-iyi-hissediyorum/")

# 2017 Wix blogu: yazıların hepsi hekimin kişisel yazıları. Adresler
# Türkçe karakterli olduğundan tek tek değil, tek kuralla yakalanır.
SPLATS = {"/single-post/*": ("eski-surum", "/tr/neden-emdr/", "2017 blog yazıları; en yakın yer hekimin mektubu.")}

# _redirects'te olup eski sitede hiç var olmamış adresler (önceki
# oturumda Google'daki kısaltılmış görünümden yanlış çıkarılmış).
NEVER_EXISTED = {
    "/tr/cocuk-ve-ergen-terapisi": "Doğrusu /tr/cocuk-ve-ergen-terapisi- (sonda tire).",
    "/tr/psikoterapi-ve-psikolojik-danismanlik": "Doğrusu /tr/psikoterapi-ve-psikolojik-danismanlik-hizmetleri.",
}


def load_redirects():
    rules = []
    for line in (ROOT.parent / "public" / "_redirects").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            src, dst, *_ = line.split()
            rules.append((src, dst))
    return rules


def current_rule(path, rules):
    for src, dst in rules:
        if src == path or (src.endswith("*") and path.startswith(src[:-1])):
            return src, dst
    return "", ""


def main():
    rows = list(csv.DictReader(open(ROOT / "urls.csv", encoding="utf-8")))
    rules = load_redirects()
    out, missing = [], []
    for r in rows:
        p = r["path"]
        norm = p.rstrip("/") if p not in ("/",) and p.count("/") > 2 else p
        rule_src, rule_dst = current_rule(p, rules)
        rec = {
            "eski_adres": p,
            "dil": r["lang"],
            "eski_durum": r["classification"],
            "kelime": r["word_count"],
            "google": r["google"],
            "duckduckgo": r["duckduckgo"],
            "baslik": r["title"] or r["wayback_title"],
        }
        if p == "/":
            rec.update(tur="ana-sayfa", karar="yeni-sayfa", hedef="/", hreflang_esi="",
                       gerekce="Türkçe ana sayfa.")
        elif p in ("/en/", "/de/", "/fr/"):
            rec.update(tur="ana-sayfa", karar="yeni-sayfa", hedef=p, hreflang_esi="",
                       gerekce="Dil ana sayfası." + (" Eski sitede Fransızca yoktu." if p == "/fr/" else ""))
        elif norm in KEEP:
            kind, pair = KEEP[norm]
            rec.update(tur=kind, karar="yeni-sayfa", hedef=norm + "/", hreflang_esi=pair,
                       gerekce=("Aynı sayfanın sonu / ile biten hâli. " if p != norm else "")
                       + {"konu": "Konu sayfası korunur.", "makale": "Makale korunur.",
                          "kvkk": "KVKK aydınlatma metni; yasal olarak gerekli.",
                          "mektup": "Hekimin mektubu; Google'da indeksli, metin hazır.",
                          "hizmet": "Hizmet sayfası; eski sayfa boştu, yeni metin yazılacak."}[kind])
        elif p in R:
            kind, target, why = R[p]
            rec.update(tur=kind, karar="301", hedef=target, hreflang_esi="", gerekce=why)
        elif p in NEVER_EXISTED:
            rec.update(tur="hic-olmamis", karar="kural-kaldir", hedef="", hreflang_esi="",
                       gerekce="Eski sitede hiç olmamış adres. " + NEVER_EXISTED[p])
        else:
            for src, (kind, target, why) in SPLATS.items():
                if p.startswith(src[:-1]):
                    rec.update(tur=kind, karar="301", hedef=target, hreflang_esi="",
                               gerekce=why + f" (kural: {src})")
                    break
            else:
                missing.append(p)
                continue

        # Şimdiki _redirects ile karşılaştırma.
        rec["simdiki_kural"] = f"{rule_src} → {rule_dst}" if rule_src else ""
        if rec["karar"] == "yeni-sayfa":
            if p in ("/", "/en/", "/de/", "/fr/"):
                degisim = "aynı"
            elif rule_src:
                degisim = "kural kaldırılacak (sayfayı yutuyor)"
            else:
                degisim = "sayfa eklenecek"
        elif rec["karar"] == "kural-kaldir":
            degisim = "kural kaldırılacak"
        elif not rule_src:
            degisim = "kural eklenecek"
        elif rule_dst == rec["hedef"] and rule_src == p:
            degisim = "aynı"
        elif rule_src.endswith("*"):
            degisim = "tekil kural eklenecek (şimdi splat yakalıyor)"
        else:
            degisim = "hedef değişecek"
        rec["degisim"] = degisim
        out.append(rec)

    if missing:
        sys.exit("Kararı olmayan adresler:\n  " + "\n  ".join(missing))

    # Tabloda olup urls.csv'de olmayan karar varsa (yazım hatası) yakala.
    known = {r["path"] for r in rows}
    stray = [p for p in list(R) + list(NEVER_EXISTED) if p not in known]
    stray += [p for p in KEEP if p not in known and p not in NEW_ONLY]
    if stray:
        sys.exit("urls.csv'de olmayan adres için karar yazılmış:\n  " + "\n  ".join(stray))

    order = {"yeni-sayfa": 0, "301": 1, "kural-kaldir": 2, "404": 3}
    out.sort(key=lambda r: (order[r["karar"]], r["dil"] or "zz", r["tur"], r["eski_adres"]))
    cols = ["eski_adres", "dil", "tur", "karar", "hedef", "hreflang_esi", "gerekce",
            "eski_durum", "kelime", "google", "duckduckgo", "simdiki_kural", "degisim", "baslik"]
    with open(ROOT / "inventory.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    print(len(out), "adres")
    print("karar:", dict(Counter(r["karar"] for r in out)))
    print("değişim:", dict(Counter(r["degisim"] for r in out)))
    print("yeni sayfa:", dict(Counter((r["dil"], r["tur"]) for r in out if r["karar"] == "yeni-sayfa")))


if __name__ == "__main__":
    main()
