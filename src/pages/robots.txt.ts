import type { APIRoute } from 'astro';
import { SITE_URL } from '../i18n/config.js';

/**
 * robots.txt derleme sırasında üretilir; Sitemap satırı böylece
 * SITE_URL ile daima aynı alan adını gösterir.
 */
export const GET: APIRoute = () =>
  new Response(
    [
      `# EMDR İzmir — ${SITE_URL}`,
      'User-agent: *',
      'Allow: /',
      '',
      '# Derleme çıktısındaki iç varlıklar taranmasın',
      'Disallow: /_astro/',
      '',
      `Sitemap: ${SITE_URL}/sitemap-index.xml`,
      '',
    ].join('\n'),
    { headers: { 'Content-Type': 'text/plain; charset=utf-8' } }
  );
