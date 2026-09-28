import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Ana sayfanın dışındaki sayfalar: eski siteden taşınan konu sayfaları,
 * makaleler, hizmet sayfaları, KVKK metni ve hekimin mektubu.
 *
 * Dosya yolu adresin kendisidir: src/content/pages/tr/panik-atak.md →
 * /tr/panik-atak/. Eski sitenin adresleri birebir korunduğu için kimlik
 * slug'a çevrilmez (ör. "obsesif--kompulsif-bozukluk" çift tirelidir).
 *
 * Her konu dört dilde yok; bu yüzden metinler i18n sözlüklerinde değil,
 * burada durur. Aynı sayfanın dilleri `group` ile bağlanır (hreflang).
 */
const pages = defineCollection({
  loader: glob({
    pattern: '*/*.md',
    base: './src/content/pages',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    kind: z.enum(['konu', 'makale', 'hizmet', 'mektup', 'kvkk']),
    /** Dil eşlerini bağlayan anahtar; aynı sayfanın her dilinde aynı. */
    group: z.string(),
    /** H1 ve <title>'ın ilk kısmı. Eski sayfadaki başlığa yakın tutulur. */
    title: z.string(),
    /** Meta açıklama. */
    description: z.string().max(170),
    /** Makalelerde yazarlar, kaynaktaki gibi. */
    authors: z.string().optional(),
    /** Makalelerde yayın bilgisi (dergi, yıl, sayfa). */
    publication: z.string().optional(),
    /**
     * Makalenin kendi (harfiyen taşınan) metninde yazar ve yayın satırı
     * zaten var; başlıkta tekrar gösterilmez. Yapılandırılmış veride yine
     * kullanılır.
     */
    bylineInBody: z.boolean().default(false),
    /** Eski sitedeki adresi (arşiv: migration/). */
    source: z.string().optional(),
    /**
     * Onay bekleyen metin: neden beklediği yazılır. Taslak sayfalar geçici
     * adreste uyarı bandıyla yayınlanır; gerçek alan adıyla derlemede
     * taslak kalmışsa derleme durur (scripts/postbuild.mjs).
     */
    draft: z.string().optional(),
  }),
});

export const collections = { pages };
