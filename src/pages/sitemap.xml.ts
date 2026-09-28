import type { APIRoute } from 'astro';
import { SITE_URL } from '../i18n/config.js';
import { HREFLANG, LOCALES, localePath } from '../i18n/index.js';
import type { Locale } from '../i18n/config.js';
import { allPages, alternatesOf, pagePath } from '../lib/pages';

/**
 * Site haritası. Dil eşleri, sayfalardaki hreflang ile aynı kaynaktan
 * (src/content/pages → group) gelir: alt sayfaların slug'ları dile göre
 * değiştiği için adres benzerliğinden tahmin edilemez.
 */
type Entry = { path: string; alternates: Partial<Record<Locale, string>> };

const escape = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export const GET: APIRoute = async () => {
  const homes = Object.fromEntries(LOCALES.map((code) => [code, localePath(code)]));
  const entries: Entry[] = LOCALES.map((code) => ({ path: localePath(code), alternates: homes }));
  for (const page of await allPages()) {
    entries.push({ path: pagePath(page), alternates: await alternatesOf(page) });
  }

  const lastmod = new Date().toISOString().slice(0, 10);
  const urls = entries.map(({ path, alternates }) => {
    const codes = LOCALES.filter((code) => alternates[code]);
    const links =
      codes.length > 1
        ? [
            ...codes.map(
              (code) =>
                `    <xhtml:link rel="alternate" hreflang="${HREFLANG[code]}" href="${escape(SITE_URL + alternates[code])}"/>`
            ),
            `    <xhtml:link rel="alternate" hreflang="x-default" href="${escape(
              SITE_URL + (alternates.tr ?? alternates.en ?? alternates[codes[0]])
            )}"/>`,
          ]
        : [];
    return [
      '  <url>',
      `    <loc>${escape(SITE_URL + path)}</loc>`,
      `    <lastmod>${lastmod}</lastmod>`,
      ...links,
      '  </url>',
    ].join('\n');
  });

  const body = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ...urls,
    '</urlset>',
    '',
  ].join('\n');

  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
