# Devir notu — emdrizmir.com taşıma işi

Bu dosyayı okuyan ajan: önceki oturum bulut ortamında çalışıyordu ve
eski siteye (emdrizmir.com) internet erişimi yoktu. Yerelde erişimin var;
işin kalanı bu yüzden sana geçti.

## Önce şunu bil: kullanıcıyla nasıl konuşacaksın

- Kullanıcı **web geliştirici değil.** Teknik terimlerle yazılmış uzun
  mesajları anlamadığını açıkça söyledi. **Kısa, sade Türkçe** yaz. Jargon
  gerekiyorsa tek cümleyle ne anlama geldiğini açıkla.
- Kullanıcı site sahibi değil, siteyi hekim adına hazırlıyor.
  Hekim: **Uzm. Dr. Mehmet Oğuz** (psikiyatri/psikoterapi, İzmir).
- **Ajanstan hiçbir şey istenmeyecek.** Kullanıcı bunu açıkça söyledi.
  Bilgiyi kendin bul (tarama, Google indeksi, archive.org).
- `main`'e yapılan her push Cloudflare Pages'te otomatik yayına çıkar.
  Push etmeden önce kullanıcıya sor.

## Proje

- Astro 5, statik site, Cloudflare Pages. `npm ci` → `npm run dev`,
  `npm run build`, `npm run check`.
- Dört dil: TR `/`, EN `/en/`, DE `/de/`, FR `/fr/`. Her dil **tek sayfa**.
  Çok dilli olmasının sebebi, hekimin Türkiye'de yaşayan yabancılara da
  hizmet vermesi (sağlık turizmi değil).
- Sitedeki bütün metinler `src/i18n/{tr,en,de,fr}.js` dosyalarında.
  İletişim, adres, saatler ve yasal alanlar `src/i18n/config.js`
  dosyasında. `assertParity()` dört sözlüğün anahtarları aynı değilse
  derlemeyi durdurur.
- `scripts/postbuild.mjs` iki iş yapar: CSP'yi satır içi betiklerin
  sha256 özetleriyle yazar ve `_redirects` dosyasını doğrular (gölgeleme,
  döngü, ölü hedef).
- Site `*.pages.dev` adresinde kendini arama motorlarına kapatır
  (noindex). Gerçek alan adına geçince `SITE_URL=https://www.emdrizmir.com`
  verilir ve indeksleme açılır. Ayrıntısı `DEPLOY.md` içinde.
- `DEPLOY.md` şunları da içeriyor: 14.09.2026 tarihli WHOIS/DNS durumu,
  e-posta riski, Search Console ve Business Profile adımları.
- Son commit: `be7a33d` (main, push edildi).

## Dokunulmayacak şeyler

- **Hekimin kendi yazdığı metinler düzeltilmeyecek.** Sitede bu metin
  `why.*` anahtarları, yani "Neden EMDR" mektubu. Eski sitedeki makaleler
  de bu kapsamda. Taşınırken **harfiyen** korunur.
- İçerikler şu yönetmeliğe uymak zorunda: *Sağlık Hizmetlerinde Tanıtım
  ve Bilgilendirme Faaliyetleri Hakkında Yönetmelik*, Resmî Gazete
  12.11.2025, sayı 33075. Adres:
  https://www.resmigazete.gov.tr/eskiler/2025/11/20251112-2.htm
  - md. 5/1/e: hasta yorumu/referans yasak. Danışan yorumları bu yüzden
    kaldırıldı; geri gelmeyecek.
  - md. 5/1/ı: son güncelleme tarihi ve site editörü sitede yayınlanıyor.
  - md. 13: 2023 tarihli eski yönetmeliği yürürlükten kaldırdı. Eski
    yönetmeliğe göre değerlendirme yapma.
  - Eski sayfalardan taşınan hekim-dışı metinlerde yanıltıcı veya abartılı
    ifade varsa (ör. "kesin tedavi", "hızlı ve etkili çözüm") yumuşat.
    Neyi değiştirdiğini kullanıcıya listele. Hekimin metinlerine dokunma;
    orada bir sorun görürsen yalnızca kullanıcıya bildir.

## Asıl görev: Google sıralamasını kaybetmeden eski siteden yeni siteye geçmek

### Durum

- Alan adı `emdrizmir.com`. Kayıt kuruluşu **Squarespace**. Kullanıcı
  alan adını **Cloudflare Registrar**'a taşımak istiyor; hekim onay verdi.
- Hosting ve e-posta ajansın sunucusunda: `5.9.123.99` (Hetzner).
  Nameserver'lar: `ns1/ns2.izajans.com`.
- Eski sitede Google'da yaklaşık 60 sayfa indeksli. Yapı `/tr/slug`,
  `/en/slug`, `/de/slug`; FR yoktu. Hem `www` hem çıplak alan adı
  indeksli. `sitemap.xml` yok.
- Yeni site dil başına tek sayfa. Şu an `public/_redirects` eski
  adresleri ana sayfadaki bölümlere yönlendiriyor (48 kural). **Asıl SEO
  riski bu:** çok sayıda farklı sayfayı ana sayfaya 301'lemek Google
  gözünde "soft 404" olur. "panik atak izmir" gibi konu aramalarındaki
  sıralama kaybolur. Alan adı ya da hosting değişikliği tek başına
  sıralamayı etkilemez.
- `emdrizmir.com.tr` adında başka birine ait bir site Google'da aynı
  isimle çıkıyor. Kullanıcıya bildirildi, cevap bekleniyor.

### Google'da görülen eski sayfalar

`_redirects` içinde slug'ı bilinenlerin dışında Google'da şu başlıklar
da var; slug'ları henüz bilinmiyor:

- **TR:** Yas Süreci, Ayrılık Kaygısı, Öfke Kontrolü, Cinsel Sorunlar,
  İlişki ve Evlilik Sorunları, İş Yaşamına İlişkin Sorunlar, Ders
  Başarısızlığı ve Sınav Kaygısı, Hamilelik Süreci ve Sonrası – Depresyon,
  Stresle Başa Çıkma ve Öfke Kontrolü, Sanal Gerçeklik (VR) ile Alıştırma,
  Viral Ensefalite Bağlı Deliryum, Covid-19 ve Ruhsal Değişim, Randevu
  Formu, Videolar, Medya, Belgelerimiz. **Belgelerimiz** sayfasında KVKK
  "Danışan Aydınlatma Metni" var ve yeni sitede karşılığı yok. Yasal
  olarak da gerekli.
- **EN:** Anxiety Disorders, Panic Attack, Separation Anxiety,
  Psychosomatic Disorders, Personality Disorder, Sexual Problems,
  Adaptation Problems, Eating Disorders, Behaviour Disorders, The Mourning
  Process, Relationship and Marriage Problems, Problems Regarding Business
  Life, Course Failure and Exam Anxiety, makalelerin İngilizceleri,
  Videos, Documents, Media.
- **DE:** Kontakt, Über uns, Unser Team, Unsere Artikel, Unsere
  Studienbereiche, Unsere Dokumente, Medien.
- Eski içerikte eski adres geçiyor: **Alsancak**. Yeni ve doğru adres:
  Yalı Mah. 268. Sk. No: 17, 35310 Güzelbahçe/İzmir.

### Yapılacaklar, sırayla

1. **Eski siteyi eksiksiz arşivle.** Hosting kapanınca içerik kaybolur;
   bu yüzden ilk iş bu.
   - **Yapıldı (28.09.2026).** Sonuç ve bulgular: `migration/README.md`.
     Envanter için başlangıç noktası `migration/urls.csv`. Öne çıkanlar:
     menüden ulaşılamayan 20 EN + 1 DE sayfa; 22 boş eski sayfa; bazı
     makalelerin yazarı Uz. Dr. Nihan Oğuz; 2017 blog yazılarının tam
     metni `migration/wayback/wix-2017/` içinde.
   - Şu kombinasyonların hepsini tara: `https`/`http` × `www`/çıplak alan
     adı, üç dil.
   - Her sayfa için kaydet: URL, HTTP durum kodu, `<title>`, meta
     description, canonical, H1/H2, gövde metninin tamamı, görseller,
     iç bağlantılar, PDF/belgeler.
   - Menüden ulaşılamayan sayfalar için archive.org'u da kontrol et.
   - Arşivi repoya koy: `migration/`. Toplam URL listesini de bir CSV
     olarak ekle.
2. **URL envanteri çıkar.** Her eski URL için şu sütunlar olsun: eski
   URL → ne yapılacak (aynı adreste yeni sayfa / en yakın sayfaya 301)
   → hedef. `_redirects`'te olmayan eski adresleri bul.
   - **Yapıldı (28.09.2026):** `migration/inventory.csv`, kararlar
     `migration/inventory.py` içinde. 50 yeni sayfa, 139 yönlendirme,
     `_redirects`'ten kalkacak 2 yanlış kural. Özet: `migration/README.md`.
   - Yeni sitede iki makalenin yazarı yanlıştı (Hayata Başlangıç → Nihan
     Oğuz; Beyin Tümörleri → Nihan Oğuz, Cem İlnem, Ferhan Yener);
     dört dilde düzeltildi. Nihan Oğuz, Dr. Mehmet Oğuz'un eşi ve
     klinikte birlikte çalışan psikiyatr/terapist; onun metinleri de
     "hekimin kendi metni" kuralına girer.
3. **Search Console verisi.** Kullanıcı DNS'i Cloudflare'e aldığında
   (aşağıdaki 1. adım), Domain mülkünü TXT kaydıyla doğrulatacak.
   Doğrulamadan sonra son 16 ayın performans verisi görünür. Sayfa
   bazında tıklama ve gösterimleri al; hangi sayfaların korunacağına
   buna göre karar ver. Veri gelene kadar varsayılan şu: konu sayfaları,
   makaleler ve KVKK sayfası korunur.
4. **Önemli sayfaları eski adreslerinde yeniden yayınla.**
   - Yeni tasarımı kullan, slug'ı **birebir aynı** tut.
   - Başlık ve H1 eskisine yakın olsun.
   - Ana sayfadaki hizmetler ve makaleler bölümü bu sayfalara bağlantı
     versin; hiçbir sayfa sitede bağlantısız kalmasın.
   - `hreflang` yalnızca gerçekten var olan çeviriler arasında kurulsun.
   - Sayfalar sitemap'e girsin.
   - Bu içerik muhtemelen `src/i18n/*.js` yerine Astro content collection
     olarak daha iyi durur, çünkü her konu dört dilde yok ve
     `assertParity()` dört dilin aynı olmasını istiyor.
   - **Dikkat:** Cloudflare Pages'te `_redirects` kuralları, aynı adreste
     dosya olsa bile uygulanır. `/tr/*` splat'ı ve tekil kurallar yeni
     sayfaları yutar; onları buna göre kaldır. `postbuild.mjs`
     doğrulayıcısını, kuralın gerçek bir sayfayı gölgelediği durumu da
     yakalayacak şekilde genişlet.
   - Proje `trailingSlash: 'always'` ile derleniyor. Eski adresler ise
     sonda `/` olmadan (`/tr/panik-atak`). Pages bu durumda tek bir 308
     yönlendirmesi yapar. Bu kabul edilebilir; yine de canonical'ın
     tutarlı olduğunu doğrula.
5. **Kalan eski adresler** için 301'i en yakın **ilgili** sayfaya ver,
   ana sayfaya değil.

### Geçiş sırası

Kullanıcı bu adımları kendisi yapacak; sen adım adım, sade dille yol
göster:

1. **DNS'i Cloudflare'e al.** Cloudflare'de zone oluşturulur. Mevcut
   kayıtların **hepsi** kopyalanır; web ve e-posta hâlâ `5.9.123.99`'u
   göstermeli. Sonra Squarespace'te nameserver'lar değiştirilir. Bu
   adımda dışarıdan hiçbir şey değişmez.
2. **Search Console'u DNS TXT kaydıyla doğrula** (yukarıdaki 3. adım).
3. **Transferi başlat.** Squarespace'te kilit kapatılır ve transfer kodu
   alınır, kod Cloudflare Registrar'a girilir. Cloudflare bunun için
   nameserver'ların zaten Cloudflare'de olmasını ister.
   - WHOIS'te tescil sahibi şu an **ajans** görünüyor: Adnan Kahveci / iz
     ajans. Tescil sahibini hekim olarak **transfer bittikten sonra**
     değiştir. Önce değiştirilirse alan adına 60 günlük transfer kilidi
     konabilir.
   - Alan adının bitiş tarihi: 11.08.2027.
4. **Yeni siteyi hazırla.** Eski sayfalar eklenmiş ve yönlendirmeler
   tamamlanmış olsun. Cloudflare Pages projesinin kurulup kurulmadığını
   kullanıcıya sor.
5. **Siteyi yeni adrese çevir.**
   - `www` ve çıplak alan adı Pages'e yönlendirilir. Çıplak alan adından
     `www`'ya 301 verilir.
   - `SITE_URL` ayarlanır.
   - **E-posta kayıtlarına dokunulmaz.**
6. **Sonrası:** sitemap Search Console'a gönderilir. Eski URL listesinin
   hepsi test edilir: her biri 200 dönmeli ya da tek bir 301/308 ile
   200'e gitmeli. Dört hafta boyunca "Sayfalar" raporunda 404 takip
   edilir.

### E-posta riski (henüz çözülmedi)

- `MX` kaydı çıplak alan adını gösteriyor. Çıplak alan adı Pages'e
  çevrilirse `info@emdrizmir.com` **çalışmaz.** Çözümü `DEPLOY.md`'de:
  `mail` A kaydı açılır ve MX ona yönlendirilir.
- Posta kutuları ajansın sunucusunda. **Eski hosting iptal edilirse
  e-posta da gider.** Kullanıcı e-postayı nasıl taşıyacağını bilmiyor.
  Hosting kapatılmadan önce bu çözülmeli (Google Workspace, Microsoft
  365, Yandex 360 vb.). Kullanıcıya basitçe anlat.

## Açık kalan küçük işler

- `config.js` → `CONTACT.legal` ruhsat alanları boş (isteğe bağlı).
- `GOOGLE_SITE_VERIFICATION` boş. Domain mülkü TXT ile doğrulanırsa buna
  gerek kalmaz.
- **Google Business Profile hâlâ eski Alsancak adresini gösteriyor.**
  Yerel arama için en kritik düzeltme bu; kullanıcıya hatırlat.
- md. 7/1/ğ: Instagram/YouTube'da yorum ayarları.
- Online terapi için uzaktan sağlık hizmeti izni. Kullanıcıya sorulacak.
