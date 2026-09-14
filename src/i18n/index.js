import tr from './tr.js';
import en from './en.js';
import de from './de.js';
import fr from './fr.js';
import { LOCALES, DEFAULT_LOCALE, localePath, localeUrl, HREFLANG } from './config.js';

export const dictionaries = { tr, en, de, fr };

export { LOCALES, DEFAULT_LOCALE, localePath, localeUrl, HREFLANG };

export function t(locale) {
  const dict = dictionaries[locale];
  if (!dict) throw new Error(`Bilinmeyen dil: ${locale}`);
  return dict;
}

/** Dil seçici için her dilin adı ve kök yolu. */
export function languageLinks(current) {
  return LOCALES.map((code) => ({
    code,
    name: dictionaries[code].name,
    href: localePath(code),
    current: code === current,
  }));
}

/**
 * Dört sözlüğün aynı anahtar ağacına sahip olduğunu doğrular.
 * Bir dile çeviri eklerken/çıkarırken sessiz boşluk kalmasın diye
 * derleme sırasında (Layout içinden) çağrılır.
 */
export function assertParity() {
  const shape = (value, path, out) => {
    if (Array.isArray(value)) {
      out.push(`${path}[]:${value.length}`);
      value.forEach((v, i) => shape(v, `${path}[${i}]`, out));
    } else if (value && typeof value === 'object') {
      for (const k of Object.keys(value).sort()) shape(value[k], `${path}.${k}`, out);
    } else {
      out.push(`${path}:${typeof value}`);
    }
    return out;
  };

  const skip = new Set(['code', 'htmlLang', 'name', 'ogLocale']);
  const keysOf = (dict) => {
    const copy = { ...dict };
    for (const k of skip) delete copy[k];
    return shape(copy, '', []);
  };

  const base = keysOf(tr);
  const problems = [];
  for (const code of LOCALES) {
    if (code === DEFAULT_LOCALE) continue;
    const other = keysOf(dictionaries[code]);
    const missing = base.filter((k) => !other.includes(k));
    const extra = other.filter((k) => !base.includes(k));
    if (missing.length) problems.push(`${code}: eksik → ${missing.slice(0, 8).join(', ')}`);
    if (extra.length) problems.push(`${code}: fazla → ${extra.slice(0, 8).join(', ')}`);
  }
  if (problems.length) {
    throw new Error('i18n sözlükleri uyuşmuyor:\n  ' + problems.join('\n  '));
  }
  return true;
}
