/**
 * Marka varlıklarını (favicon, uygulama ikonları, OG görseli) logodan üretir.
 * Yalnızca içerik değiştiğinde elle çalıştırılır:  node scripts/generate-assets.mjs
 * Çıktılar public/ altına yazılır ve depoya işlenir.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const ROOT = path.resolve(import.meta.dirname, '..');
const PUBLIC = path.join(ROOT, 'public');

const ACCENT = '#2A5AAD';
const ACCENT_DEEP = '#1D3F7E';
const AMBER = '#D9821B';
const INK = '#16202E';

/* Logodaki simge (baş + beyin) — yazı olmadan, kare çerçevede. */
const MARK = `
  <path fill="${INK}" d="M96.5,3.9c11.2,0,21.2,3.1,28,7.9C118.7,4.8,108.3,0,96.5,0s-22.2,4.8-28,11.9C75.2,7,85.3,3.9,96.5,3.9z"/>
  <path fill="${AMBER}" d="M98.3,12.4l-1.9,3.7l-1.9-3.7c-3.5,0.8-6,3.9-6,7.7c0,2.7,1.3,5.1,3.4,6.5v-7.8h9v7.8c2.1-1.4,3.4-3.8,3.4-6.5C104.4,16.3,101.8,13.2,98.3,12.4z"/>
  <path fill="${ACCENT}" d="M96.5,6.9c-7.3,0-13.2,5.9-13.2,13.2c0,5.7,3.6,10.5,8.7,12.4v-3.6c-3.2-1.6-5.4-4.9-5.4-8.8c0-5.5,4.4-9.9,9.9-9.9c5.5,0,9.9,4.4,9.9,9.9c0,3.8-2.2,7.1-5.4,8.8v3.6c5.1-1.8,8.7-6.7,8.7-12.4C109.6,12.8,103.7,6.9,96.5,6.9z"/>
`;

/* Tam yazı markası — "EMDR İZMİR" harfleri de vektör yol olarak gelir,
   böylece OG görseli hiçbir sistem yazı tipine bağlı kalmaz. */
const WORDMARK_PATHS = `
  <path d="M96.5,3.9c11.2,0,21.2,3.1,28,7.9C118.7,4.8,108.3,0,96.5,0s-22.2,4.8-28,11.9C75.2,7,85.3,3.9,96.5,3.9z"/>
  <path d="M0,50V28.6h11.5V31h-7v7h6v2.3h-6v7.3H12V50H0z"/>
  <path d="M17.9,50l0.3-21.4h5.5l6,15.8h0.1l5.9-15.8h5.1L41,50h-4.4l-0.2-16.2h-0.1l-6,16.2h-3.4l-6-16.2h-0.1L20.7,50H17.9z"/>
  <path d="M48,28.6h7.3c3.3,0,5.9,0.9,7.6,2.7c1.8,1.8,2.7,4.5,2.7,8c0,3.5-0.9,6.1-2.6,7.9c-1.8,1.8-4.3,2.7-7.7,2.7H48V28.6z M55.4,47.7c1.3,0,2.3-0.3,3-0.8c0.8-0.5,1.3-1.4,1.7-2.6c0.4-1.2,0.5-2.8,0.5-4.9c0-2.1-0.2-3.7-0.5-4.9c-0.4-1.2-0.9-2.1-1.7-2.7c-0.8-0.5-1.8-0.8-3.1-0.8h-2.7v16.7H55.4z"/>
  <path d="M71.3,28.6h6.6c2.4,0,4.3,0.6,5.7,1.8c1.4,1.2,2,2.8,2,5c0,1.4-0.3,2.6-1,3.6c-0.7,1-1.6,1.8-2.7,2.4l4.9,8.7h-5.2l-4-7.8h-1.7V50h-4.5V28.6z M77.5,40.1c0.8,0,1.4-0.1,1.9-0.4c0.4-0.3,0.8-0.7,1-1.4c0.2-0.7,0.3-1.6,0.3-2.7c0-1.7-0.2-2.9-0.7-3.7c-0.5-0.7-1.3-1.1-2.5-1.1h-1.6v9.3H77.5z"/>
  <path d="M93.3,50V20.1h6.4V50H93.3z"/>
  <path d="M108.7,50v-1.9L119,31h-9.7v-2.4h15.2v2l-10.3,17h10.3V50H108.7z"/>
  <path d="M131.8,50l0.3-21.4h5.5l6,15.8h0.1l5.9-15.8h5.1l0.2,21.4h-4.4l-0.2-16.2h-0.1l-6,16.2h-3.4l-6-16.2h-0.1L134.6,50H131.8z"/>
  <path d="M163.2,50V28.6h4.5V50H163.2z"/>
  <path d="M176.2,28.6h6.6c2.4,0,4.3,0.6,5.7,1.8c1.4,1.2,2,2.8,2,5c0,1.4-0.3,2.6-1,3.6c-0.7,1-1.6,1.8-2.7,2.4l4.9,8.7h-5.2l-4-7.8h-1.7V50h-4.5V28.6z M182.4,40.1c0.8,0,1.4-0.1,1.9-0.4c0.4-0.3,0.8-0.7,1-1.4c0.2-0.7,0.3-1.6,0.3-2.7c0-1.7-0.2-2.9-0.7-3.7c-0.5-0.7-1.3-1.1-2.5-1.1h-1.6v9.3H182.4z"/>
`;

/* ── favicon.svg — koyu/açık temada da okunur, yuvarlak köşeli zemin ── */
const faviconSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#F3F6FA"/>
  <g transform="translate(-64.5 15.5) scale(1)">${MARK}</g>
</svg>`;

/* ── uygulama ikonu — maskelenebilir, dolu zeminli ── */
const appIconSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" fill="${ACCENT}"/>
  <g transform="translate(-514 124) scale(8)">
    <path fill="#FFFFFF" d="M96.5,3.9c11.2,0,21.2,3.1,28,7.9C118.7,4.8,108.3,0,96.5,0s-22.2,4.8-28,11.9C75.2,7,85.3,3.9,96.5,3.9z"/>
    <path fill="${AMBER}" d="M98.3,12.4l-1.9,3.7l-1.9-3.7c-3.5,0.8-6,3.9-6,7.7c0,2.7,1.3,5.1,3.4,6.5v-7.8h9v7.8c2.1-1.4,3.4-3.8,3.4-6.5C104.4,16.3,101.8,13.2,98.3,12.4z"/>
    <path fill="#FFFFFF" d="M96.5,6.9c-7.3,0-13.2,5.9-13.2,13.2c0,5.7,3.6,10.5,8.7,12.4v-3.6c-3.2-1.6-5.4-4.9-5.4-8.8c0-5.5,4.4-9.9,9.9-9.9c5.5,0,9.9,4.4,9.9,9.9c0,3.8-2.2,7.1-5.4,8.8v3.6c5.1-1.8,8.7-6.7,8.7-12.4C109.6,12.8,103.7,6.9,96.5,6.9z"/>
  </g>
</svg>`;

/* ── OG görseli katmanı: karartma + yazı markası + çift yönlü uyarım noktaları ── */
const dots = Array.from({ length: 7 }, (_, i) => {
  const x = 90 + i * 44;
  const o = 0.22 + i * 0.1;
  return `<circle cx="${x}" cy="500" r="6" fill="#FFFFFF" opacity="${o.toFixed(2)}"/>`;
}).join('');

const ogOverlaySvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="veil" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0%"   stop-color="${ACCENT_DEEP}" stop-opacity="0.95"/>
      <stop offset="55%"  stop-color="${ACCENT_DEEP}" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="${INK}"        stop-opacity="0.92"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#veil)"/>
  <g transform="translate(90 200) scale(3.6)">
    <g fill="#FFFFFF">${WORDMARK_PATHS}</g>
    <path fill="${AMBER}" d="M98.3,12.4l-1.9,3.7l-1.9-3.7c-3.5,0.8-6,3.9-6,7.7c0,2.7,1.3,5.1,3.4,6.5v-7.8h9v7.8c2.1-1.4,3.4-3.8,3.4-6.5C104.4,16.3,101.8,13.2,98.3,12.4z"/>
    <path fill="#8FB2F0" d="M96.5,6.9c-7.3,0-13.2,5.9-13.2,13.2c0,5.7,3.6,10.5,8.7,12.4v-3.6c-3.2-1.6-5.4-4.9-5.4-8.8c0-5.5,4.4-9.9,9.9-9.9c5.5,0,9.9,4.4,9.9,9.9c0,3.8-2.2,7.1-5.4,8.8v3.6c5.1-1.8,8.7-6.7,8.7-12.4C109.6,12.8,103.7,6.9,96.5,6.9z"/>
  </g>
  <rect x="90" y="430" width="132" height="3" fill="${AMBER}"/>
  ${dots}
  <line x1="90" y1="500" x2="354" y2="500" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="1"/>
</svg>`;

async function main() {
  await fs.mkdir(path.join(PUBLIC, 'og'), { recursive: true });

  await fs.writeFile(path.join(PUBLIC, 'favicon.svg'), faviconSvg);

  const appIcon = Buffer.from(appIconSvg);
  for (const size of [180, 192, 512]) {
    const name = size === 180 ? 'apple-touch-icon.png' : `icon-${size}.png`;
    await sharp(appIcon).resize(size, size).png({ compressionLevel: 9 }).toFile(path.join(PUBLIC, name));
  }

  // .ico — 32x32, eski tarayıcılar ve arama sonucu küçük resimleri için
  await sharp(Buffer.from(faviconSvg)).resize(32, 32).toFormat('png').toFile(path.join(PUBLIC, 'favicon-32.png'));
  const ico = await sharp(Buffer.from(faviconSvg)).resize(32, 32).png().toBuffer();
  await fs.writeFile(path.join(PUBLIC, 'favicon.ico'), toIco(ico, 32));
  await fs.rm(path.join(PUBLIC, 'favicon-32.png'));

  // OG: klinik fotoğrafı + marka katmanı
  const photo = await sharp(path.join(ROOT, 'src/assets/img/hero-clinic.webp'))
    .resize(1200, 630, { fit: 'cover', position: 'attention' })
    .toBuffer();

  await sharp(photo)
    .composite([{ input: Buffer.from(ogOverlaySvg), top: 0, left: 0 }])
    .jpeg({ quality: 86, mozjpeg: true })
    .toFile(path.join(PUBLIC, 'og/emdrizmir.jpg'));

  console.log('Varlıklar üretildi: favicon.svg, favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png, og/emdrizmir.jpg');
}

/** Tek boyutlu PNG'yi .ico kabuğuna sarar. */
function toIco(png, size) {
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(1, 4);
  const entry = Buffer.alloc(16);
  entry.writeUInt8(size === 256 ? 0 : size, 0);
  entry.writeUInt8(size === 256 ? 0 : size, 1);
  entry.writeUInt8(0, 2);
  entry.writeUInt8(0, 3);
  entry.writeUInt16LE(1, 4);
  entry.writeUInt16LE(32, 6);
  entry.writeUInt32LE(png.length, 8);
  entry.writeUInt32LE(22, 12);
  return Buffer.concat([header, entry, png]);
}

main();
