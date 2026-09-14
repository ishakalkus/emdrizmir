/**
 * Site geneli sabitler ve dil yapılandırması.
 * Kanonik alan adı ortam değişkeni ile geçersiz kılınabilir:
 *   SITE_URL=https://www.emdrizmir.com npm run build
 */

export const SITE_URL = (
  process.env.SITE_URL || 'https://www.emdrizmir.com'
).replace(/\/+$/, '');

/** Google Search Console doğrulama etiketi (opsiyonel). */
export const GOOGLE_SITE_VERIFICATION = process.env.GOOGLE_SITE_VERIFICATION || '';

/** GA4 ölçüm kimliği. Boşsa hiçbir analitik kodu üretilmez. */
export const GA_MEASUREMENT_ID = process.env.GA_MEASUREMENT_ID || '';

/** Değişmeyen iletişim bilgileri — her dilde aynı. */
export const CONTACT = {
  phone: '+90 539 650 11 59',
  phoneHref: 'tel:+905396501159',
  phoneE164: '+905396501159',
  whatsapp: 'https://wa.me/905396501159',
  whatsappNumber: '905396501159',
  email: 'info@emdrizmir.com',
  street: 'Yalı Mah. 268. Sk. No: 17',
  postalCode: '35310',
  district: 'Güzelbahçe',
  city: 'İzmir',
  country: 'TR',
  // DOĞRULANMALI: Güzelbahçe merkezi için yaklaşık değerler. Bu koordinatlar
  // MedicalClinic yapılandırılmış verisinde Google'a bildirildiği için,
  // yayına almadan önce muayenehanenin gerçek konumuyla değiştirin
  // (Google Maps'te pime sağ tıklayıp koordinatları kopyalayabilirsiniz).
  geo: { lat: 38.3697, lng: 26.8806 },
  instagram: 'https://instagram.com/dr.mehmetoguz/',
  youtube: 'https://www.youtube.com/channel/UC908HStKWliDLCuiIF4IDxA',
  mapsQuery:
    'Yal%C4%B1%20Mah.%20268.%20Sk.%20No%3A17%20G%C3%BCzelbah%C3%A7e%20%C4%B0zmir',
  foundingYear: '1999',
  // DOĞRULANMALI: varsayım. Yapılandırılmış veride yayınlanır ve Google
  // Business Profile'daki saatlerle tutarlı olmalıdır.
  openingHours: 'Mo-Fr 09:00-19:00, Sa 09:00-14:00',
};

/** Desteklenen diller. Sıra, dil seçicideki sıradır. */
export const LOCALES = ['tr', 'en', 'de', 'fr'];
export const DEFAULT_LOCALE = 'tr';

/** Bir dilin kök yolu: tr → "/", diğerleri → "/en/" gibi. */
export function localePath(locale) {
  return locale === DEFAULT_LOCALE ? '/' : `/${locale}/`;
}

/** Mutlak kanonik URL. */
export function localeUrl(locale) {
  return SITE_URL + localePath(locale);
}

/** hreflang etiketinde kullanılan bölge kodları. */
export const HREFLANG = {
  tr: 'tr-TR',
  en: 'en',
  de: 'de',
  fr: 'fr',
};
