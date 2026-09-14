/** index.js için tip bildirimleri. */
import type { Locale } from './config.js';

/**
 * İçerik sözlüğü. Ağacı çok derin olduğu ve yalnızca şablonlarda
 * okunduğu için gevşek tutulur; dört dil arasındaki yapı denkliği
 * derleme sırasında assertParity() ile ayrıca doğrulanır.
 */
export type Dictionary = Record<string, any>;

export const dictionaries: Record<Locale, Dictionary>;

export function t(locale: Locale): Dictionary;

export function languageLinks(current: Locale): Array<{
  code: Locale;
  name: string;
  href: string;
  current: boolean;
}>;

export function assertParity(): true;
export function assertHours(): true;

export {
  LOCALES,
  DEFAULT_LOCALE,
  localePath,
  localeUrl,
  HREFLANG,
} from './config.js';
export type { Locale };
