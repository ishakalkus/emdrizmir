/**
 * Derleme sonrası adım:
 *
 *  1. dist içindeki bütün satır içi <script> ve <style> bloklarının sha256
 *     özetini çıkarır ve Content-Security-Policy'yi bu özetlerle kurar.
 *     Böylece CSP'de 'unsafe-inline' açmak gerekmez.
 *  2. dist/_headers dosyasındaki __CSP__ yer tutucusunu doldurur.
 *  3. Kaçak satır içi style="" niteliği kaldıysa uyarır (CSP'yi bozar).
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = path.resolve(import.meta.dirname, '..');
const DIST = path.join(ROOT, 'dist');
const GA = process.env.GA_MEASUREMENT_ID || '';

const sha256 = (text) =>
  `'sha256-${crypto.createHash('sha256').update(text, 'utf8').digest('base64')}'`;

async function walk(dir) {
  const out = [];
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else out.push(full);
  }
  return out;
}

const files = (await walk(DIST)).filter((f) => f.endsWith('.html'));
if (files.length === 0) throw new Error('dist içinde HTML bulunamadı — önce astro build çalışmalı.');

const scriptHashes = new Set();
const styleHashes = new Set();
const inlineStyleAttrs = [];

for (const file of files) {
  const html = await fs.readFile(file, 'utf8');
  const rel = path.relative(DIST, file);

  // src'siz <script> blokları
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (/\bsrc\s*=/i.test(m[1])) continue;
    if (m[2].length === 0) continue;
    scriptHashes.add(sha256(m[2]));
  }

  for (const m of html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)) {
    if (m[1].length === 0) continue;
    styleHashes.add(sha256(m[1]));
  }

  for (const m of html.matchAll(/\sstyle\s*=\s*"[^"]*"/gi)) {
    inlineStyleAttrs.push(`${rel}: ${m[0].trim().slice(0, 60)}`);
  }
}

if (inlineStyleAttrs.length) {
  console.warn(
    `\n⚠  ${inlineStyleAttrs.length} satır içi style="" niteliği bulundu. ` +
      `CSP'de style-src-attr açık bırakılmadığı için bunlar uygulanmaz — sınıfa taşıyın:`
  );
  for (const s of inlineStyleAttrs.slice(0, 10)) console.warn('   ' + s);
}

const scriptSrc = ["'self'", ...scriptHashes];
const styleSrc = ["'self'", ...styleHashes];
const connectSrc = ["'self'"];

if (GA) {
  scriptSrc.push('https://www.googletagmanager.com');
  connectSrc.push(
    'https://www.google-analytics.com',
    'https://region1.google-analytics.com',
    'https://analytics.google.com'
  );
}

const csp = [
  "default-src 'self'",
  `script-src ${scriptSrc.join(' ')}`,
  `style-src ${styleSrc.join(' ')}`,
  "img-src 'self' data:",
  "font-src 'self'",
  `connect-src ${connectSrc.join(' ')}`,
  // Google Maps çerçevesi yalnızca ziyaretçi "Haritayı yükle"ye bastığında eklenir
  'frame-src https://www.google.com',
  "manifest-src 'self'",
  "base-uri 'none'",
  "object-src 'none'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  'upgrade-insecure-requests',
].join('; ');

const headersPath = path.join(DIST, '_headers');
let headers = await fs.readFile(headersPath, 'utf8');

// Yer tutucu yalnızca Content-Security-Policy satırında aranır: dosyanın
// başındaki açıklama metninde geçen bir söz, yanlışlıkla politika yerine
// doldurulmasın.
const placeholder = /^(\s*Content-Security-Policy:\s*)__CSP__\s*$/m;
if (!placeholder.test(headers)) {
  throw new Error('_headers içinde "Content-Security-Policy: __CSP__" satırı bulunamadı.');
}
headers = headers.replace(placeholder, `$1${csp}`);

if (headers.includes('__CSP__')) {
  throw new Error('_headers içinde doldurulmamış __CSP__ yer tutucusu kaldı.');
}
await fs.writeFile(headersPath, headers);

console.log(
  `\n✓ CSP yazıldı — ${scriptHashes.size} satır içi betik, ${styleHashes.size} satır içi stil özeti` +
    (GA ? ', GA4 açık' : ', analitik kapalı') +
    `\n  ${csp}\n`
);
