/**
 * İçerik sözlüklerindeki görsel anahtarlarını gerçek dosyalara bağlar.
 * Böylece i18n dosyalarında dosya yolu değil, yalnızca anahtar durur.
 */
import svcIndividual from './img/svc-individual.webp';
import svcCoupleFamily from './img/svc-couple-family.webp';
import svcVr from './img/svc-vr.webp';
import svcOnline from './img/svc-online.webp';
import svcCounselling from './img/svc-counselling.webp';
import svcChildAdolescent from './img/svc-child-adolescent.webp';
import drMehmetOguz from './img/dr-mehmet-oguz.jpg';
import drNihanOguz from './img/dr-nihan-oguz.jpg';
import ahmetCengizKoksal from './img/ahmet-cengiz-koksal.jpg';

export const images = {
  'svc-individual': svcIndividual,
  'svc-couple-family': svcCoupleFamily,
  'svc-vr': svcVr,
  'svc-online': svcOnline,
  'svc-counselling': svcCounselling,
  'svc-child-adolescent': svcChildAdolescent,
  'dr-mehmet-oguz': drMehmetOguz,
  'dr-nihan-oguz': drNihanOguz,
  'ahmet-cengiz-koksal': ahmetCengizKoksal,
};

export function image(key) {
  const found = images[key];
  if (!found) throw new Error(`Tanımsız görsel anahtarı: ${key}`);
  return found;
}
