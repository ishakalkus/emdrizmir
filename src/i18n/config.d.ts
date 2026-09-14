/** config.js için tip bildirimleri — çalışma zamanı kodu sade JS olarak kalır. */

export type Locale = 'tr' | 'en' | 'de' | 'fr';

export const SITE_URL: string;
export const GOOGLE_SITE_VERIFICATION: string;
export const GA_MEASUREMENT_ID: string;

export const CONTACT: {
  phone: string;
  phoneHref: string;
  phoneE164: string;
  whatsapp: string;
  whatsappNumber: string;
  email: string;
  street: string;
  postalCode: string;
  district: string;
  city: string;
  country: string;
  geo: { lat: number; lng: number };
  instagram: string;
  youtube: string;
  mapsQuery: string;
  foundingYear: string;
  openingHours: string;
};

export const LOCALES: readonly Locale[];
export const DEFAULT_LOCALE: Locale;
export const HREFLANG: Record<Locale, string>;

export function localePath(locale: Locale): string;
export function localeUrl(locale: Locale): string;
