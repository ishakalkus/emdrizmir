# Yayına alma — Cloudflare Pages + Google

Bu belge sıfırdan yayına alma adımlarını sırayla anlatır.

---

## 1. Cloudflare Pages projesi

Cloudflare panelinde **Workers & Pages → Create → Pages → Connect to Git**
ile bu depoyu bağlayın ve şu ayarları girin:

| Ayar | Değer |
| --- | --- |
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Root directory | (boş) |
| Node version | `22` (`NODE_VERSION` ortam değişkeni ile) |

Üretim dalı olarak `main` seçin. Her push'ta yeniden derlenir; diğer
dallar önizleme dağıtımı olarak yayınlanır.

Git bağlamadan elle yüklemek isterseniz:

```bash
npm run deploy      # npx wrangler pages deploy dist
```

## 1b. Önce pages.dev, sonra alan adı

Alan adını bağlamadan önce `*.pages.dev` adresinde yayınlamak için **hiçbir
ayar girmeniz gerekmez.** Cloudflare derleme sırasında `CF_PAGES_URL`
değişkenini kendiliğinden tanımlar; site onu kanonik adres olarak kullanır.

Bu adreste site kendini **arama motorlarına kapatır**:

- her sayfa `noindex, nofollow` yayınlanır (hem meta etiketi hem
  `X-Robots-Tag` başlığı),
- `robots.txt` içeriği `Disallow: /` olur.

Sebebi şudur: geçici adres indekslenirse, gerçek alan adını bağladığınızda
aynı içerik iki adreste görünür ve kendi sitenizle sıralama yarışına girer.

Gerçek alan adını bağladığınızda tek yapmanız gereken, ortam
değişkenlerine `SITE_URL=https://www.emdrizmir.com` eklemek ve yeniden
dağıtmaktır; indeksleme, canonical, hreflang ve sitemap kendiliğinden
açılıp doğru adrese döner. Derleme çıktısı hangi modda olduğunu yazar:

```
⚠  GEÇİCİ ADRES: https://emdrizmir.pages.dev
   Sayfalar noindex, robots.txt her şeyi kapatıyor.
```

```
✓ Yayın adresi: https://www.emdrizmir.com — indekslemeye açık
```

`NOINDEX=1` ile indekslemeyi her adreste elle de kapatabilirsiniz.

## 2. Ortam değişkenleri

**Settings → Environment variables** altında, *Production* için:

| Değişken | Değer | Zorunlu mu |
| --- | --- | --- |
| `NODE_VERSION` | `22` | evet |
| `SITE_URL` | `https://www.emdrizmir.com` | alan adı bağlanınca. Boşsa `CF_PAGES_URL` kullanılır ve site noindex yayınlanır (bkz. 1b) |
| `GOOGLE_SITE_VERIFICATION` | Search Console'un verdiği kod | hayır |
| `GA_MEASUREMENT_ID` | `G-XXXXXXXXXX` | hayır (boşsa analitik hiç yüklenmez) |

`SITE_URL` yanlışsa `canonical`, `hreflang`, `sitemap.xml` ve `og:url`
yanlış adrese işaret eder; ilk yayından önce doğrulayın.

## 3. Alan adı ve yönlendirme

1. **Custom domains** altında `www.emdrizmir.com` ekleyin.
2. Çıplak alan adı için `emdrizmir.com` → `www.emdrizmir.com` **301**
   yönlendirmesi kurun (Cloudflare → Rules → Redirect Rules). Tek bir
   kanonik ana bilgisayar adı kullanmak, arama motorlarının aynı içeriği
   iki ayrı site sanmasını önler.
3. SSL/TLS modunu **Full (strict)** yapın.
4. `Always Use HTTPS` açık olsun.

`public/_headers` dosyası `Strict-Transport-Security` gönderir; HSTS
preload listesine başvurmadan önce çıplak alan adının da HTTPS'te
çalıştığından emin olun.

## 4. Google Search Console

1. <https://search.google.com/search-console> → **Mülk ekle** →
   *URL öneki* → `https://www.emdrizmir.com/`
2. Doğrulama yöntemi olarak **HTML etiketi**'ni seçin; verilen
   `content="…"` değerini `GOOGLE_SITE_VERIFICATION` ortam değişkenine
   yazıp yeniden dağıtın, sonra **Doğrula**'ya basın.
3. **Site haritaları** bölümüne şunu ekleyin:

   ```
   sitemap-index.xml
   ```

   Bu dosya derlemede üretilir ve dört dilin tamamını, karşılıklı
   `hreflang` bağlarıyla içerir.
4. **Uluslararası hedefleme** ayarını *kullanmayın*: site tek bir ülkeye
   değil, dört dile hitap ediyor; `hreflang` etiketleri zaten doğru
   sinyali veriyor.

Dizine alınmayı hızlandırmak için **URL Denetimi** ile dört adresi tek tek
isteyebilirsiniz: `/`, `/en/`, `/de/`, `/fr/`.

## 5. Google Business Profile (harita sonuçları)

Bir muayenehane için yerel aramada en çok işe yarayan adım budur.

1. <https://business.google.com> üzerinde işletmeyi doğrulayın.
2. Kategori: **Psikiyatrist** (ikincil: *Psikoterapist*).
3. Adres, telefon ve internet sitesi alanlarının sitedeki bilgilerle
   **birebir aynı** yazıldığından emin olun:

   ```
   Yalı Mah. 268. Sk. No: 17, 35310 Güzelbahçe / İzmir
   +90 539 650 11 59
   https://www.emdrizmir.com
   ```

   Sitedeki `MedicalClinic` yapılandırılmış verisi de aynı değerleri
   bildirir (`src/i18n/config.js`). İkisi arasındaki tutarlılık, Google'ın
   iki kaydı eşleştirmesini kolaylaştırır.
4. Çalışma saatlerini profilde güncellerseniz `src/i18n/config.js`
   içindeki `openingHours` alanını da güncelleyin.

## 6. Google Analytics (isteğe bağlı)

`GA_MEASUREMENT_ID` **boş bırakılırsa** siteden Google'a hiçbir istek
gitmez ve çerez yazılmaz. Önerilen varsayılan budur.

Açmaya karar verirseniz:

- Kod, Consent Mode v2 ile yüklenir ve `ad_storage`, `ad_user_data`,
  `ad_personalization`, `analytics_storage` izinlerinin tamamı
  **`denied`** başlar. Bu hâliyle çerez yazılmaz.
- Ölçüm yapabilmek için ziyaretçiden açık onay alan bir arayüz eklemek ve
  onay gelince şunu çağırmak gerekir:

  ```js
  gtag('consent', 'update', { analytics_storage: 'granted' });
  ```

- Onay arayüzü olmadan izinleri `granted` yapmayın: KVKK md. 5 ve GDPR
  md. 6 açısından açık rıza olmadan ölçüm çerezi yazmak sorun yaratır.
- Analitiği açtığınızda `scripts/postbuild.mjs`, Google'ın alan adlarını
  CSP'ye kendiliğinden ekler; elle düzenleme gerekmez.

## 7. Yayın sonrası kontrol listesi

```bash
# Güvenlik başlıkları
curl -sI https://www.emdrizmir.com/ | grep -i "content-security\|strict-transport\|x-frame"

# Dört dil de 200 dönüyor mu
for p in "" en/ de/ fr/; do
  curl -s -o /dev/null -w "%{http_code} /$p\n" "https://www.emdrizmir.com/$p"
done

# Site haritası
curl -s https://www.emdrizmir.com/sitemap-index.xml
```

Ayrıca:

- [Rich Results Test](https://search.google.com/test/rich-results) —
  `MedicalClinic` ve `Physician` verisi okunuyor mu.
- [PageSpeed Insights](https://pagespeed.web.dev/) — mobil Core Web Vitals.
- [securityheaders.com](https://securityheaders.com/) — başlık notu.
- Facebook/LinkedIn paylaşım önizlemesi — `og/emdrizmir.jpg` görünüyor mu.

## 8. Gönderilen güvenlik başlıkları

`public/_headers` dosyasında tanımlıdır; `Content-Security-Policy` satırı
her derlemede satır içi betiklerin sha256 özetleriyle yeniden yazılır
(`scripts/postbuild.mjs`), böylece politikada `'unsafe-inline'` yer almaz.

| Başlık | Değer |
| --- | --- |
| `Content-Security-Policy` | `default-src 'self'`, betikler yalnızca özet eşleşmesiyle, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'none'` |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | kamera, mikrofon, konum, ödeme vb. tamamen kapalı |
| `Cross-Origin-Opener-Policy` | `same-origin` |

`frame-src` yalnızca `https://www.google.com` içindir; Google Maps
çerçevesi de ancak ziyaretçi onayıyla eklenir.

---

## Yayından önce doğrulanması gerekenler

Adres ve çalışma saatleri hekimden alındı ve yerine işlendi:

```
Yalı Mah. 268. Sk. No: 17, 35310 Güzelbahçe / İzmir
Pazartesi – Cumartesi, 10:00 – 18:00
```

Saatler iki yerde durur ve ikisi de güncellenmelidir:

- `src/i18n/config.js` → `openingHours` (yapılandırılmış veri, makine biçimi)
- `src/i18n/{tr,en,de,fr}.js` → `contact.hoursValue` ve `contact.hoursClosed`
  (iletişim bölümünde görünen metin)

Yalnızca birini değiştirirseniz derleme `assertHours()` ile durur; yani
ikisinin birbirinden kopması mümkün değildir. Google Business Profile'daki
saatleri de aynı tutmayı unutmayın.

### İsteğe bağlı: kesin koordinat

`config.js` içindeki `geo` alanı şu an `null`. Bu hâliyle yapılandırılmış
veriye koordinat **hiç yazılmaz**; konum yalnızca kesin olan `address` ve
`hasMap` alanlarıyla bildirilir. Yaklaşık bir koordinat yayınlamak
Google'a yanlış pim bildireceği için, koordinat yayınlamamaktan kötüdür.

Kesin koordinatı eklemek isterseniz: Google Maps'i **masaüstü tarayıcıda**
açın, muayenehanenin tam olduğu noktaya **sağ tıklayın**; açılan menünün
en üstündeki `38.xxxxx, 26.xxxxx` satırına tıklayınca panoya kopyalanır.
Sonra:

```js
geo: { lat: 38.12345, lng: 26.67890 },
```

Alan doldurulduğu anda `GeoCoordinates` düğümü yapılandırılmış veriye
kendiliğinden geri eklenir. Harita pimi zaten Google Business Profile'dan
geldiği için bu alan zorunlu değildir.

Ayrıca sitedeki dört dilin metinleri bu taşıma sırasında hazırlandı.
Hekimlik içeriği olduğu için, İngilizce/Almanca/Fransızca sürümlerin
yayından önce ilgili dili bilen biri tarafından okunması önerilir —
özellikle unvanlar, kurum adları ve tanı terimleri.

---

## Mevzuat: Sağlık Hizmetlerinde Tanıtım ve Bilgilendirme Yönetmeliği

Dayanak: **RG 12/11/2025, sayı 33075.** Yayımı tarihinde yürürlüğe girdi
(md. 14), geçiş süresi yok. 29/7/2023 tarihli önceki yönetmeliği
yürürlükten kaldırdı (md. 13).

### Zorunlu — md. 5/1/ı

> "İnternet sitelerindeki bilgilendirmenin son güncelleme tarihi ile
> internet sitesi editörüne ulaşılabilecek iletişim bilgileri açıkça
> belirtilir."

Bu ikisi alt bilgide, dört dilde yayınlanır:

- **Son güncelleme tarihi** her derlemede kendiliğinden yazılır, dilin
  biçimine göre ("14 Eylül 2026" / "14 septembre 2026") ve makine okunur
  `<time datetime>` ile birlikte.
- **Site editörü** `src/i18n/config.js` → `CONTACT.legal.editorName` ve
  `editorEmail` alanlarından gelir. Şu an muayenehane sahibi ve genel
  e-posta yazılıdır; **siteyi fiilen kim güncelliyorsa onu yazın.**

Editör bilgisi boş bırakılırsa her derleme uyarır:

```
⚠  ZORUNLU (Yönetmelik md. 5/1/ı): site editörünün iletişim bilgisi eksik.
```

### İsteğe bağlı — kurum bilgileri

Ruhsat unvanı, kuruluş türü, ruhsat sayı/tarihi, belgeyi veren müdürlük
ve mesul müdür alanları **bu yönetmelikte sayılmaz**; kuruluş türüne göre
kendi mevzuatı (ör. Ayakta Teşhis ve Tedavi Yapılan Özel Sağlık
Kuruluşları Hakkında Yönetmelik) isteyebilir. `CONTACT.legal` içinde
dururlar; doldurulanlar alt bilgide "Kurum bilgileri" başlığıyla dört
dilde yayınlanır, boş kalanlar hiç basılmaz.

### Yapılan metin düzeltmeleri

Hekimin kendi kaleme aldığı "Neden EMDR" mektubuna **dokunulmamıştır**;
düzeltmeler yalnızca kurum metinlerinde yapılmıştır.

| Madde | Ne değişti |
| --- | --- |
| 5/1/d | Ekip başlığı "uzman, akredite psikoterapistler" → "Psikiyatri uzmanı hekimler ve kurum ekibimiz". 1219 sayılı Kanunda ana/yan dal olmayan bir uzmanlık ünvanı artık kullanılmıyor; hekimlerin kendi "Psikiyatri Uzmanı" ünvanı yerinde |
| 5/1/ç | "tüm kaygı bozukluklarında … tıbbi hastalıkların tedavisinde etkilidir" → EMDR'ın TSSB'de uluslararası kılavuzlarda yer aldığı, diğer tablolarda hekim değerlendirmesiyle tedavi planının parçası olabileceği |
| 5/1/ç | "bedeniniz artık alarma geçmez" → tepkinin azalmasının *hedeflendiği* ve sonuçların kişiden kişiye değiştiği |
| 5/1/ğ | "20.000" sayısının ölçülmüş bir veri değil, bilgi işleme modelinde kullanılan yaklaşık bir değer olduğu belirtildi |
| 5/1/f, g | "Üzerinde Çalıştığımız Konular" etiketleri randevu formuna bağlıydı; artık bağlantı değil, düz liste |

### Dil sürümlerinin kapsamı — md. 8

Hekim, **Türkiye'de yaşayan yabancı danışanlara** hizmet verdiği için
farklı dillerde site istemiştir. Site bunu kendi metninde açıkça beyan
eder: iletişim bölümündeki "Görüşme dilleri" satırının altında dört
dilde "Türkiye'de yaşayan yabancı danışanlarımız için görüşmeler bu
dillerde yürütülebilir" notu yer alır.

Buna uygun olarak yurt dışına yönelen ifadeler kaldırılmıştır: online
terapi hizmeti artık "yurt dışından danışanlar" değil, "İzmir dışında
yaşayan danışanlar" der; "Yurt dışı" etiketi "İzmir dışı" olmuştur.

**Ancak bu, hukuki değerlendirmenin yerine geçmez.** Md. 8, uluslararası
sağlık turizmi tanıtımını yetki belgesine bağlar ve md. 8/1/a bu
faaliyetin *ayrı bir internet sitesi* üzerinden yürütülmesini şart koşar.
Muayenehanenin sağlık turizmi faaliyeti yoksa bu madde kapsam dışıdır;
ileride böyle bir faaliyet düşünülürse yabancı dil sayfaları ayrı bir
siteye taşınmalı ve yetki belgesi alınmalıdır. Yayından önce bir sağlık
hukuku danışmanına teyit ettirin.

### Açık kalan konular

| Konu | Madde | Durum |
| --- | --- | --- |
| Hekimin mektubundaki "en kalıcı sonuçlar", "ispatlanmış" ifadeleri | 5/1/h, 5/1/ç | Hekim kendi metnine dokunulmamasını istedi |
| Görsel içeriklerde uyarı ibaresi ("Her cerrahi veya girişimsel işlemde…") | 7/1/k | Muayenehanede cerrahi/girişimsel işlem yok; uygulanıp uygulanmayacağı yorum gerektirir |
| Instagram/YouTube paylaşımlarında yorum, beğeni ve yeniden paylaşımın kapatılması | 7/1/ğ | Site dışı, hesap ayarlarından yapılır |
| "Online Bireysel Terapi" — uzaktan sağlık hizmeti yetkisi | Ayrı yönetmelik | Teyit edilmeli |

Hasta teşekkür ve memnuniyet ifadeleri **md. 5/1/e ile yasaktır**;
danışan yorumları bölümü bu yüzden kaldırılmıştır.

