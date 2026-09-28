import { getCollection, type CollectionEntry } from 'astro:content';
import { LOCALES, localePath } from '../i18n/index.js';
import type { Locale } from '../i18n/config.js';

export type PageEntry = CollectionEntry<'pages'>;
export type Kind = PageEntry['data']['kind'];

/** src/content/pages/<dil>/<slug>.md → dil ve slug. */
export function parts(entry: PageEntry): { lang: Locale; slug: string } {
  const [lang, slug] = entry.id.split('/');
  if (!(LOCALES as readonly string[]).includes(lang) || !slug) {
    throw new Error(`Sayfa yolu <dil>/<slug>.md biçiminde olmalı: ${entry.id}`);
  }
  return { lang: lang as Locale, slug };
}

/**
 * Sayfanın adresi. Türkçe ana sayfa kökte (/) olsa da eski sitenin
 * Türkçe alt sayfaları /tr/ altındaydı; adresler korunduğu için alt
 * sayfalar dört dilde de /<dil>/<slug>/ biçimindedir.
 */
export function pagePath(entry: PageEntry): string {
  const { lang, slug } = parts(entry);
  return `/${lang}/${slug}/`;
}

let cache: PageEntry[] | undefined;
export async function allPages(): Promise<PageEntry[]> {
  cache ??= await getCollection('pages');
  return cache;
}

/** Aynı sayfanın dillerdeki adresleri (hreflang ve dil seçici için). */
export async function alternatesOf(entry: PageEntry): Promise<Partial<Record<Locale, string>>> {
  const out: Partial<Record<Locale, string>> = {};
  for (const other of await allPages()) {
    if (other.data.group !== entry.data.group) continue;
    const { lang } = parts(other);
    if (out[lang]) {
      throw new Error(`"${entry.data.group}" grubunda iki ${lang} sayfası var: ${out[lang]}, ${pagePath(other)}`);
    }
    out[lang] = pagePath(other);
  }
  return out;
}

/** Bir dildeki, belirli türdeki sayfalar; başlığa göre sıralı. */
export async function pagesOf(lang: Locale, kind: Kind): Promise<PageEntry[]> {
  return (await allPages())
    .filter((p) => parts(p).lang === lang && p.data.kind === kind)
    .sort((a, b) => a.data.title.localeCompare(b.data.title, lang));
}

/**
 * Bir gruptaki sayfanın o dildeki adresi; yoksa verilen yedek dillerdeki.
 * Ana sayfadaki makale listesi, Almanca/Fransızca ziyaretçiyi yazının
 * İngilizce ya da Türkçe aslına götürür.
 */
export async function groupHref(
  group: string,
  lang: Locale,
  fallback: Locale[] = ['en', 'tr']
): Promise<{ href: string; lang: Locale } | undefined> {
  const pages = (await allPages()).filter((p) => p.data.group === group);
  for (const code of [lang, ...fallback]) {
    const hit = pages.find((p) => parts(p).lang === code);
    if (hit) return { href: pagePath(hit), lang: code };
  }
  return undefined;
}

/** Sayfa türünün ana sayfadaki bölümü (içerik haritası ve geri bağlantı). */
export function sectionOf(kind: Kind, lang: Locale): string {
  const anchor = { konu: '#hizmetler', hizmet: '#hizmetler', makale: '#makaleler', mektup: '#neden', kvkk: '' }[kind];
  return localePath(lang) + anchor;
}
