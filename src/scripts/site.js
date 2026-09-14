/**
 * EMDR İzmir — istemci tarafı davranışlar.
 *
 * Dosya dört dilde de aynıdır ve tek bir dosya olarak önbelleğe alınır:
 * dile bağlı bütün metinler HTML'deki data-* niteliklerinden okunur.
 * Her bölüm kendi elemanı yoksa sessizce atlanır.
 */
(function () {
  'use strict';

  var $ = function (id) {
    return document.getElementById(id);
  };

  /* ── yıl ─────────────────────────────────────────────────── */
  var yr = $('yr');
  if (yr) yr.textContent = String(new Date().getFullYear());

  /* ── tema anahtarı ───────────────────────────────────────── */
  var root = document.documentElement;
  var themeBtn = $('themeBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var isDark =
        root.getAttribute('data-theme') === 'dark' ||
        (!root.hasAttribute('data-theme') &&
          window.matchMedia('(prefers-color-scheme: dark)').matches);
      var next = isDark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try {
        localStorage.setItem('emdrizmir-theme', next);
      } catch (e) {
        /* özel sekmede localStorage kapalı olabilir */
      }
    });
  }

  /* ── başlıktaki yapışkan çizgi ───────────────────────────── */
  var top = $('top');
  if (top) {
    var onScroll = function () {
      top.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── mobil çekmece ───────────────────────────────────────── */
  var menuBtn = $('menuBtn');
  var drawer = $('drawer');
  if (menuBtn && drawer) {
    var setDrawer = function (open) {
      drawer.setAttribute('data-open', String(open));
      menuBtn.setAttribute('aria-expanded', String(open));
    };
    menuBtn.addEventListener('click', function () {
      setDrawer(drawer.getAttribute('data-open') !== 'true');
    });
    drawer.addEventListener('click', function (ev) {
      if (ev.target.closest('a')) setDrawer(false);
    });
  }

  /* ── dil menüsü ──────────────────────────────────────────── */
  var langBtn = $('langBtn');
  var langMenu = $('langMenu');
  if (langBtn && langMenu) {
    var setLangs = function (open) {
      langMenu.setAttribute('data-open', String(open));
      langBtn.setAttribute('aria-expanded', String(open));
    };
    langBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      setLangs(langMenu.getAttribute('data-open') !== 'true');
    });
    document.addEventListener('click', function (ev) {
      if (!ev.target.closest('.langs')) setLangs(false);
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') setLangs(false);
    });
  }

  /* ── çift yönlü uyarım şeridini duraklat ─────────────────── */
  var bls = $('bls');
  var blsBtn = $('blsBtn');
  if (bls && blsBtn) {
    blsBtn.addEventListener('click', function () {
      var paused = bls.classList.toggle('is-paused');
      blsBtn.textContent = paused
        ? blsBtn.getAttribute('data-resume') || 'Devam et'
        : blsBtn.getAttribute('data-pause') || 'Duraklat';
      blsBtn.setAttribute('aria-pressed', String(paused));
    });
  }

  /* ── harita: yalnızca tıklandığında yüklenir ──────────────
     Google Maps çerçevesi baştan gömülmez; ziyaretçinin IP'si
     onayı olmadan Google'a gitmez (KVKK / GDPR). */
  var map = $('map');
  var mapBtn = $('mapConsent');
  if (map && mapBtn) {
    mapBtn.addEventListener('click', function () {
      if (map.getAttribute('data-loaded') === 'true') return;
      var frame = document.createElement('iframe');
      frame.src = map.getAttribute('data-src') || '';
      frame.title = map.getAttribute('data-title') || '';
      frame.loading = 'lazy';
      frame.referrerPolicy = 'no-referrer-when-downgrade';
      frame.allowFullscreen = true;
      map.appendChild(frame);
      map.setAttribute('data-loaded', 'true');
    });
  }

  /* ── randevu mesajını oluştur ─────────────────────────────
     Form hiçbir sunucuya istek atmaz; yalnızca cihazda metin kurar. */
  var form = $('apptForm');
  if (form) {
    /* Form hiçbir sunucuya gönderilmez. Bir alandayken Enter'a basmak
       sayfayı yeniden yükleyip yazılanları silerdi; engelliyoruz.
       Böylece CSP'de form-action 'none' kalabiliyor. */
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
    });

    var val = function (id) {
      var el = $(id);
      return el ? (el.value || '').trim() : '';
    };
    var label = function (key) {
      return form.getAttribute('data-l-' + key) || key;
    };

    var compose = function () {
      var lines = [form.getAttribute('data-greeting') || ''];
      if (val('f-name')) lines.push(label('name') + ': ' + val('f-name'));
      if (val('f-tel')) lines.push(label('tel') + ': ' + val('f-tel'));
      lines.push(label('mode') + ': ' + val('f-mode'));
      if (val('f-msg')) lines.push('', val('f-msg'));
      return lines.join('\n');
    };

    var waBtn = $('sendWa');
    if (waBtn) {
      waBtn.addEventListener('click', function () {
        var number = form.getAttribute('data-wa') || '';
        window.open(
          'https://wa.me/' + number + '?text=' + encodeURIComponent(compose()),
          '_blank',
          'noopener'
        );
      });
    }

    var mailBtn = $('sendMail');
    if (mailBtn) {
      mailBtn.addEventListener('click', function () {
        var subject =
          (form.getAttribute('data-subject') || 'Randevu') +
          ' — ' +
          (val('f-name') || 'EMDR İzmir');
        window.location.href =
          'mailto:' +
          (form.getAttribute('data-mail') || '') +
          '?subject=' +
          encodeURIComponent(subject) +
          '&body=' +
          encodeURIComponent(compose());
      });
    }
  }
})();
