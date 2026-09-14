# EMDR İzmir

Uzm. Dr. Mehmet Oğuz ve ekibinin Güzelbahçe/İzmir'deki psikiyatri ve
psikoterapi merkezinin tanıtım sitesi. Dört dilde yayınlanan statik bir
site: **Türkçe, English, Deutsch, Français**.

Tasarım tek dosyalık `index.html` sürümünden birebir korunarak
[Astro](https://astro.build) tabanlı bir Node projesine taşındı.

---

## Hızlı başlangıç

```bash
nvm use            # Node 22 (bkz. .nvmrc — en az 20.11)
npm ci
npm run dev        # http://localhost:4321
```

| Komut | Ne yapar |
| --- | --- |
| `npm run dev` | Geliştirme sunucusu, anlık yenileme |
| `npm run build` | `dist/` üretir, ardından CSP başlıklarını yazar |
| `npm run preview` | Üretilen `dist/` klasörünü yerelde servis eder |
| `npm run check` | Astro + TypeScript tip denetimi |
| `npm run assets` | Favicon, uygulama ikonları ve OG görselini logodan yeniden üretir |
| `npm run deploy` | Derler ve Wrangler ile Cloudflare Pages'e yükler |

Yayına alma adımları ve Google ayarları için **[DEPLOY.md](DEPLOY.md)**.

`*.pages.dev` adresinde site kendini indekslemeye kapatır (noindex +
`Disallow: /`), böylece geçici adres sonradan gerçek alan adıyla sıralama
yarışına girmez. `SITE_URL` gerçek alan adına çevrildiğinde indeksleme
kendiliğinden açılır.

---

## Klasör düzeni

```
src/
  assets/img/        Kaynak görseller (Astro derlemede boyutlandırır)
  assets/images.js   Görsel anahtarı → dosya eşlemesi
  components/        Bölüm bileşenleri (Hero, Protocol, Team, …)
  i18n/
    config.js        Alan adı, iletişim bilgileri, dil listesi
    tr.js en.js      Bütün metinler — dile göre ayrı sözlükler
    de.js fr.js
    index.js         Sözlük toplayıcı + yapı denkliği denetimi
  layouts/Base.astro <head>, başlık, alt bilgi, betik yüklemesi
  pages/             index.astro (tr) ve en/ de/ fr/ + 404
  scripts/site.js    Tek istemci betiği — dört dilde ortak
  styles/            site.css (özgün tasarım) + fonts.css
public/              Yazı tipleri, ikonlar, robots.txt, _headers, _redirects
scripts/             generate-assets.mjs, postbuild.mjs
```

## İçerik nasıl düzenlenir

Sayfadaki **bütün metinler** `src/i18n/` altındaki dört sözlüktedir; HTML
içinde gömülü yazı yoktur. Bir cümleyi değiştirmek için ilgili dilin
dosyasında karşılığını düzenlemek yeterlidir.

Dört sözlük aynı anahtar ağacını taşımak zorundadır. Bir dile alan ekleyip
diğerlerini unutursanız **derleme hata vererek durur** (`assertParity()`),
böylece bir dilde sessizce boş kalan bölüm oluşmaz.

Yeni bir görsel eklerken: dosyayı `src/assets/img/` içine koyun, anahtarını
`src/assets/images.js` dosyasına yazın, sözlükte `image: 'anahtar'` olarak
kullanın.

## Tasarım

`src/styles/site.css` özgün tasarımın CSS'idir. Taşıma sırasında yalnızca
şunlar değişti:

- Yazı tipi adları self-host edilen sürümlere bağlandı.
- Danışan yorumları bölümünün kuralları kaldırıldı.
- Satır içi `style="…"` nitelikleri sınıflara taşındı (CSP'de
  `style-src-attr 'unsafe-inline'` açmak zorunda kalmamak için).
- Dil seçici, harita onay katmanı ve "içeriğe atla" bağlantısı eklendi.
- Üç düzeltme: telefonda yatay kaydırmaya yol açan harita en-boy oranı,
  dar ekranda taşan başlık satırı ve WhatsApp düğmesinin kontrastı
  (ayrıntılar dosyadaki yorumlarda).

## Yapılan denetimler

- **Erişilebilirlik:** axe-core, WCAG 2.1 AA + best-practice — 4 dil ×
  açık/koyu tema × 390/1280 px, 14 senaryoda ihlal yok.
- **Yerleşim:** 4 dil × 18 ekran genişliğinde (320–1920 px) yatay taşma yok.
- **CSP:** üretilen politika gerçek başlık olarak uygulanıp test edildi;
  ihlal yok, tema/dil/harita etkileşimleri çalışıyor.

Bu denetimleri yeniden çalıştırmak için geçici olarak:

```bash
npm i -D playwright axe-core
```

## Sayfa ağırlığı

| | Önce (tek dosya) | Sonra (ilk yükleme) |
| --- | --- | --- |
| HTML + CSS + JS (gzip) | 680 KB | ~22 KB |
| Görseller | HTML'e base64 gömülü | Ayrı, responsive, ekran altındakiler tembel yüklenir |
| Üçüncü taraf istek | Google Fonts | yok |

## Gizlilik

Site ziyaretçi verisi toplamaz:

- Yazı tipleri kendi sunucumuzdan gelir; Google Fonts'a istek gitmez.
- Google Maps çerçevesi ancak ziyaretçi "Haritayı yükle"ye bastığında
  eklenir — onay verilmeden IP adresi Google'a gitmez.
- Randevu formu hiçbir sunucuya veri göndermez; yalnızca cihazda WhatsApp
  veya e-posta metni hazırlar.
- Analitik varsayılan olarak **kapalıdır**; açılırsa Consent Mode v2 ile
  bütün izinler "denied" başlar.

KVKK (6698) ve GDPR açısından anlamı için DEPLOY.md'deki ilgili bölüme bakın.
