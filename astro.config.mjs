// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { SITE_URL, LOCALES, DEFAULT_LOCALE } from './src/i18n/config.js';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'always',
  build: {
    format: 'directory',
    // Bütün CSS harici dosyaya çıksın: CSP'de style-src 'self' kalabilsin
    // ve stil dosyası dört sayfa arasında paylaşılıp önbelleğe alınsın.
    inlineStylesheets: 'never',
  },

  i18n: {
    locales: [...LOCALES],
    defaultLocale: DEFAULT_LOCALE,
    routing: {
      // Türkçe kök dizinde (/), diğerleri /en/ /de/ /fr/ altında.
      prefixDefaultLocale: false,
      redirectToDefaultLocale: false,
    },
  },

  integrations: [
    sitemap({
      i18n: {
        defaultLocale: DEFAULT_LOCALE,
        locales: { tr: 'tr-TR', en: 'en', de: 'de', fr: 'fr' },
      },
      changefreq: 'monthly',
      priority: 0.8,
      lastmod: new Date(),
    }),
  ],

  image: {
    // Yalnızca kendi varlıklarımız işlenir; uzak kaynak yok.
    responsiveStyles: false,
  },

  vite: {
    build: {
      assetsInlineLimit: 0, // hiçbir varlık data: URI olarak gömülmesin
    },
  },
});
