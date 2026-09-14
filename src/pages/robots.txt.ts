import type { APIRoute } from 'astro';
import { SITE_URL, IS_PREVIEW } from '../i18n/config.js';

/**
 * robots.txt derleme sırasında üretilir; Sitemap satırı böylece
 * SITE_URL ile daima aynı alan adını gösterir.
 */
const body = IS_PREVIEW
  ? [
      `# EMDR İzmir — geçici adres (${SITE_URL})`,
      '# Gerçek alan adı bağlanana kadar tarama tamamen kapalı:',
      '# aynı içerik iki adreste indekslenip siteyle yarışmasın.',
      'User-agent: *',
      'Disallow: /',
      '',
    ]
  : [
      `# EMDR İzmir — ${SITE_URL}`,
      'User-agent: *',
      'Allow: /',
      '',
      '# Derleme çıktısındaki iç varlıklar taranmasın',
      'Disallow: /_astro/',
      '',
      `Sitemap: ${SITE_URL}/sitemap-index.xml`,
      '',
    ];

export const GET: APIRoute = () =>
  new Response(body.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
