# Eski site arşivi — emdrizmir.com

Eski sitenin (ajans sunucusu, `5.9.123.99`) **27.09.2026** tarihli tam
kopyası. Hosting kapanınca içerik kaybolacağı için alındı. Yeni siteye
taşınacak metinler, yönlendirme listesi ve URL envanteri bu klasöre
dayanır.

## Neler var

| Yol | İçerik |
|---|---|
| `urls.csv` | Bulunan **bütün** eski adresler, tek tablo (sütunlar aşağıda) |
| `inventory.csv` | Her eski adres için karar: yeni sayfa mı, 301 mi, hedefi ne (`inventory.py` üretir) |
| `live/` | Canlı sitedeki her gerçek sayfa: ham `.html`, ayıklanmış `.json`, okunur `.md` |
| `wayback/` | Canlıda artık olmayan, archive.org'dan alınan eski sayfalar (aynı üç biçim) |
| `wayback/wix-2017/` | 2017 Wix sürümü: blog yazıları (RSS'ten tam metin), site haritası |
| `assets/` | Sayfalarda kullanılan görseller, sunucudaki yollarıyla |
| `assets.csv` | Her görselin kaynağı (canlı / archive.org) ve durumu |
| `screenshots/` | Canlı sayfaların tam boy ekran görüntüsü (masaüstü, 1280 px) |
| `search-index/` | Google ve DuckDuckGo'da görünen adresler (27.09.2026) |
| `wayback-cdx.json` | archive.org'un bu alan adı için tuttuğu bütün kayıtların listesi |
| `extra-seeds.txt` | Menüden ulaşılamayan, elle bulunan adresler ve nasıl bulunduğu |
| `archive.py`, `screenshots.py` | Arşivi yeniden üreten betikler |

`.json` dosyasındaki alanlar: `title`, `meta_description`, `canonical`,
`hreflang`, `h1`/`h2`/`h3`, `breadcrumb`, `body_text` (gövde metninin
tamamı), `content_images`, `content_links`, `embeds` (YouTube vb.),
`internal_links`, `documents`, `page_images`, dört adres biçiminin durum
kodları (`variants`).

`.md` dosyası yalnızca içerik alanını okunur hâle getirir. **Hekimin
metinleri taşınırken kaynak `.html` dosyasıdır**; `.md` dönüşümü boşluk ve
satır sonlarını değiştirebilir.

### `urls.csv` sütunları

- `path` — eski adres (alan adı olmadan).
- `source` — adres nereden bulundu: `seed`, `link from …` (site içi
  bağlantı), `archive.org`, `_redirects`, `google`, `tahmin`,
  `search-index`, `wix-2017 sitemap/feed`.
- `classification`
  - `page`: gerçek içerikli sayfa, `live/` içinde.
  - `home`: dilin ana sayfası.
  - `soft404`: sunucu 200 döndürüyor ama ana sayfayı gösteriyor
    (sayfa aslında yok).
  - `404`: sunucu gerçekten 404 veriyor.
- `https_www`, `https_bare`, `http_www`, `http_bare` — dört biçimin durum
  kodu ve varsa yönlendirme hedefi.
- `title`, `h1`, `meta_description`, `canonical`, `word_count`, `documents`.
- `redirect_rule`, `redirect_target` — `public/_redirects` içinde bu
  adresi yakalayan kural.
- `live_file`, `wayback_latest`, `wayback_file`, `wayback_title`,
  `wayback_words`, `wix2017_file`.
- `google`, `duckduckgo` — arama motorunda görünüyor mu.

## Bulgular

### Sayılarla

- **197 eski adres** bulundu (`urls.csv`):
  - 104'ü canlıda gerçek sayfa: 49 TR, 37 EN, 17 DE ve kök `/`. Dördü dil
    ana sayfası.
  - 51'i soft 404 (200 dönüyor ama ana sayfayı gösteriyor).
  - 42'si gerçek 404.
- Adreslerin kaynağı: site içi bağlantılar, archive.org dizini (85),
  `_redirects` (47), 2017 site haritası ve RSS (20), Google (14 gizli EN
  sayfası), çeviriden tahmin edilip doğrulanan adresler (7).
- **Google**'da 78 kayıt, **DuckDuckGo**'da 25 kayıt var. Hepsi tabloda
  eşleşti (`google`, `duckduckgo` sütunları).
- **Canlıda boş olan 22 sayfa var.** İçerik alanında tek satır yazı yok,
  yalnızca resim ya da hiçbir şey: Kurumsal, Medya, Videolar (bir YouTube
  videosu hariç), hizmet sayfalarının çoğu (Çift Aile Terapisi, Çocuk ve
  Ergen Terapisi, Online Bireysel Terapi, VR, Psikoterapi Hizmetleri) ve
  DE/EN karşılıkları. Arşivde eksik bir şey yok; eski sitede de boşlar.
- archive.org'dan **22 eski sayfa** (15'i dolu metin) ve 2017 blogundan
  **8 yazı** alındı. 34 eski adresin archive.org'da yalnızca boş ya da ana
  sayfa kopyası var; bunlarda kurtarılacak içerik yok.
- **90 görsel** kayıtlı. 13'ü (2018 sürümüne ait görseller) ne sunucuda ne
  archive.org'da var; `assets.csv`'de `missing` olarak işaretli.
- 104 canlı sayfanın hepsinin ekran görüntüsü alındı.

### `_redirects` ile ilgili (URL envanteri adımında düzeltilecek)

- `/tr/cocuk-ve-ergen-terapisi` ve `/tr/psikoterapi-ve-psikolojik-danismanlik`
  eski sitede yok. Doğru adresler `/tr/cocuk-ve-ergen-terapisi-` (sonda
  tire) ve `/tr/psikoterapi-ve-psikolojik-danismanlik-hizmetleri`.
- 37 İngilizce, 17 Almanca sayfa ve eski sürümlerden kalan adreslerin
  çoğu henüz `_redirects`'te yok. Tam liste `urls.csv`'de
  (`redirect_rule` boş olanlar).

### Sunucu davranışı

- **Olmayan adresler 200 döner.** `/tr/xyz`, `/en/xyz`, `/upload/` gibi
  var olmayan bir adres, ana sayfayı 200 koduyla gösterir. Google bunları
  kopya sayfa olarak görür. Yeni sitede gerçek 404 olacak.
- **`www` ve çıplak alan adı ikisi de 200.** Birbirine yönlendirme yok;
  Google iki hâli de ayrı indekslemiş. `http` → `https` 301 var.
- **Hiçbir sayfada** `canonical`, meta description, `hreflang` yok.
  `robots.txt` ve `sitemap.xml` yok (ikisi de ana sayfayı döndürüyor).
- Kök düzeydeki eski adresler (ör. `/emdr-nedir`) sonda `/` yoksa gerçek
  404, varsa (`/emdr-nedir/`) soft 404.

### Menüden ulaşılamayan sayfalar

- Eski İngilizce **Study Areas** sayfasındaki bütün kutular `/en/`'e
  bağlı. İngilizce konu sayfalarına site içinden ulaşılamıyor, ama canlı
  ve Google'da indeksli (Panic Attack, Anxiety Disorders vb.). Adresleri
  `extra-seeds.txt`'te, nasıl bulunduklarıyla birlikte.
- Almanca menü, bazı maddelerde `/en/` altında Almanca/Türkçe adreslere
  bağlanıyor (`/en/kontakt`, `/en/unsere-artikel` …). Bunların hepsi
  soft 404; yani eski sitede kırık bağlantı.

### Sitenin eski sürümleri (archive.org)

1. **2017 — Wix.** Adresler `/single-post/2017/...` ve kökte konu adları.
   Sayfalar tarayıcıda çalışan uygulama olduğu için archive.org
   kopyalarında metin yok; ama blog yazılarının **tam metni** RSS
   akışında duruyor: `wayback/wix-2017/`. Yazar: Dr. Mehmet Oğuz. "Neden
   EMDR?" mektubunun 2017 hâli de burada.
2. **2018–2019 — başka bir sistem.** Kökte, sonu `/` olmadan adresler
   (`/emdr-nedir`, `/makaleler`, `/seans-sureleri-ve-sikligi`).
3. **2019–2021 — sonu `/` ile biten adresler** (`/panik-atak/`,
   `/kaygi-anksiyete-bozukluklari/`). Bunların archive.org kopyalarının
   çoğu, yeni sisteme geçildikten sonra alınmış ve ana sayfayı gösteriyor;
   gerçek içerik yoksa `urls.csv`'de `wayback_title` =
   "(yalnızca ana sayfa kopyası)".
4. **2021–bugün — şimdiki sistem.** `/tr/`, `/en/`, `/de/`.

DuckDuckGo hâlâ 2. ve 3. sürümden adresler gösteriyor (`/emdr-nedir/`,
`/iletisim/`, `/hakkimizda/`, `/belgelerimiz/` …). Bunlar yönlendirme
listesine girmeli.

### İçerikle ilgili notlar

- **Yazar:** "Hayata Başlangıç Boş Bir Tahta mıdır?" yazısının altında
  "Uz. Dr. Psikiyatrist Nihan Oğuz" imzası var. Google, "Viral Ensefalite
  Bağlı Deliryum" yazısında da yazar olarak "N Oğuz" gösteriyor. Makaleler
  taşınırken yazar adı kaynaktaki gibi korunmalı.
- **Belgelerimiz** (`/tr/belgelerimiz`) KVKK "Kişisel Veriler Aydınlatma
  ve Onam Metni"dir. PDF değil, sayfanın içinde metin olarak duruyor.
- **Eski adres:** İletişim ve alt bilgi alanlarında Alsancak adresi geçiyor
  (Kültür Mah. Talatpaşa Bulvarı …). Yeni adres Güzelbahçe; taşınırken
  eski adres alınmamalı.
- **Danışan yorumları** (`/tr/danisan-yorumlari`, `/en/client-comments`)
  arşivde duruyor; yönetmelik md. 5/1/e gereği yeni sitede
  yayınlanmayacak.

## URL envanteri (`inventory.csv`)

Her eski adres için tek satır. `inventory.py` kararları kendi içindeki
tablolardan alır; bir karar değişecekse orası düzenlenip betik yeniden
çalıştırılır (`python3 migration/inventory.py`). Kararı olmayan ya da
yanlış yazılmış bir adres kalırsa betik durur.

Sütunlar: `eski_adres`, `dil`, `tur`, `karar` (`yeni-sayfa` / `301` /
`kural-kaldir`), `hedef`, `hreflang_esi`, `gerekce`, eski durum ve kelime
sayısı, `google`/`duckduckgo`, `simdiki_kural` (şimdiki `_redirects`),
`degisim` (bu kural için ne yapılacak).

**Kural:** konu sayfaları, makaleler ve KVKK sayfası korunur (HANDOFF.md
varsayılanı). Kullanıcı kararıyla (28.09.2026) hizmet sayfaları ve
"Neden EMDR" mektubu da eklendi. Gerisi en yakın ilgili yere 301 alır.

- **64 sayfa eski adresinde** yeniden yayınlanır, **12 sayfa** yeni açılır:
  - 21 TR + 19 EN konu sayfası.
  - 5 TR + 4 EN makale.
  - Hizmet sayfaları, 6 hizmet × 4 dil. Eski sayfalar boştu, **yeni metin
    yazılacak**; yayından önce hekim onayı alınmalı (tanıtım
    yönetmeliği). TR ve DE eski adreslerinde kalır (DE eskisi gibi Türkçe
    slug'lı). EN ve FR eski sitede hiç olmadı; bu 12 sayfa kendi dilinde
    yeni adresle açılır ve envanterde yalnızca dil eşi olarak görünür.
  - "Neden EMDR" mektubu (TR + EN): hekimin metni, ana sayfada kısa bölüm
    ve bu sayfaya bağlantı kalır.
  - KVKK aydınlatma metni (TR).
  - Dil eşleri `hreflang_esi`'nde. Karşılığı olmayanlar: TR `depresyon`,
    `okula-uyum`, `hayata-baslangic-bos-bir-tahta-midir`.
- **124 adres 301 alır.** Hepsi aynı dildeki en yakın sayfaya ya da ana
  sayfa bölümüne gider. Dil ana sayfasına düşen 20 adres, ya eski sitede
  boş olan sayfalar (Medya, Videolar, Belgeler) ya da yönetmelik gereği
  kaldırılan danışan yorumları.
- İçeriği yeni ana sayfada birebir bulunan sayfalar (İletişim, Randevu
  Formu, Ekibimiz, Hakkımızda, Kurumsal, liste sayfaları) ayrı sayfa
  olmaz; ilgili bölüme 301 alır. Bunlara gelen aramalar isim aramaları
  ve ana sayfa bu aramalarda zaten çıkıyor.
- Eski Almanca menüdeki kırık `/en/<türkçe-slug>` hizmet bağlantıları,
  aynı hizmetin yeni İngilizce sayfasına 301 alır.
- Eski Almanca site aslında İngilizce metinlerle kurulmuştu; Almanca içerik
  yalnızca menüdeydi. Korunacak Almanca sayfa yok.
- `_redirects`'teki `/tr/*` splat'ı kalkacak (yeni `/tr/…` sayfalarını
  yutuyor). Yerine tekil kurallar gelecek.
- Eski sürümlerden kalan kök adresler (2017–2021) konusu belliyse o konu
  sayfasına, değilse ilgili ana sayfa bölümüne gider. 2017 Wix yazıları
  (`/single-post/…`, Türkçe karakterli adresler) tek kuralla `/#neden`'e.
- `www`'suz ve `http` hâller `_redirects`'te değil, Cloudflare'de alan adı
  düzeyinde çözülecek (çıplak → `www` 301, `http` → `https`).

## Yeniden üretmek

Hosting kapanmadan önce arşiv yeniden alınabilir (repo kökünden):

```bash
python3 -m venv .venv-archive
.venv-archive/bin/pip install requests beautifulsoup4 lxml markdownify playwright
.venv-archive/bin/python migration/archive.py
.venv-archive/bin/python migration/screenshots.py
```

`archive.py` archive.org'a dakikada ~15 istekten fazla gitmez, aksi
hâlde archive.org bağlantıyı keser. Tam tur yaklaşık 30 dakika sürer.
archive.org dizini alınamazsa kayıtlı `wayback-cdx.json` kullanılır;
o da yoksa betik eksik arşiv üretmemek için durur.

`archive.py --reextract` ağa çıkmadan, kayıtlı ham HTML'den `.json` ve
`.md` dosyalarını yeniden üretir (ayıklama kuralı değişirse). `urls.csv`
bu modda değişmez.
