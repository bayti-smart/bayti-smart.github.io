/* Smart Casa — tiny vanilla JS. No cookies, no third parties. Preferences live in localStorage only. */
(function () {
  'use strict';
  var d = document, h = d.documentElement;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || d).querySelectorAll(s)); };
  var LS = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var LANGS = ['ar', 'en', 'fr', 'es', 'de'];
  var pageLang = h.lang;

  /* 1. Old links such as /?lang=fr or /?lang=en#p-<id> -> new URLs */
  (function () {
    if (location.pathname !== '/') return;
    var q = new URLSearchParams(location.search), lg = q.get('lang'), hash = location.hash || '';
    var m = hash.match(/^#p-(.+)$/);
    if (!lg && !m) return;
    if (LANGS.indexOf(lg) < 0) lg = LS.get('sc_lang') || 'en';
    var pre = lg === 'en' ? '' : '/' + lg;
    var target = m ? pre + '/p/' + encodeURIComponent(decodeURIComponent(m[1])) + '/' : (pre ? pre + '/' : '/');
    if (target !== location.pathname) location.replace(target);
  })();

  /* 1b. Product images: retry once after a short delay, then show a neutral placeholder */
  d.addEventListener('error', function (e) {
    var im = e.target;
    if (!im || im.tagName !== 'IMG' || !im.closest('.card-img, .pp-img')) return;
    if (!im.dataset.retry) {
      im.dataset.retry = '1';
      var src = im.currentSrc || im.src;
      setTimeout(function () { im.src = src; }, 1500);
    } else {
      im.parentNode.classList.add('img-fail');
    }
  }, true);

  /* 2. Dropdowns close on outside click / Escape */
  d.addEventListener('click', function (e) {
    $$('details.dd[open]').forEach(function (x) { if (!x.contains(e.target)) x.removeAttribute('open'); });
  });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') $$('details.dd[open]').forEach(function (x) { x.removeAttribute('open'); });
  });

  /* 3. Mobile menu */
  var burger = $('.burger'), mnav = $('#mnav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* 4. Accessibility: text size + eye comfort */
  var fs = parseFloat(LS.get('sc_fs')) || 1;
  function setFs(v) {
    fs = Math.max(0.9, Math.min(1.3, Math.round(v * 100) / 100));
    h.style.setProperty('--fs', fs);
    LS.set('sc_fs', fs);
  }
  $$('[data-a11y]').forEach(function (btn) {
    var kind = btn.getAttribute('data-a11y');
    if (kind === 'comfort') btn.setAttribute('aria-pressed', h.classList.contains('comfort') ? 'true' : 'false');
    btn.addEventListener('click', function () {
      if (kind === 'dec') setFs(fs - 0.1);
      if (kind === 'inc') setFs(fs + 0.1);
      if (kind === 'comfort') {
        var on = h.classList.toggle('comfort');
        LS.set('sc_comfort', on ? '1' : '0');
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      }
    });
  });

  /* 5. Remember an explicit language choice */
  $$('a[data-lang]').forEach(function (a) {
    a.addEventListener('click', function () { LS.set('sc_lang', a.getAttribute('data-lang')); });
  });

  /* 6. Language suggestion banner (only if the visitor never chose a language) */
  (function () {
    var el = $('#lang-banner');
    if (!el || LS.get('sc_lang')) return;
    var pref = (navigator.language || 'en').slice(0, 2).toLowerCase();
    if (pref === pageLang) return;
    var data; try { data = JSON.parse(el.getAttribute('data-banner')); } catch (e) { return; }
    var alt = $('link[rel="alternate"][hreflang="' + pref + '"]');
    if (!data[pref] || !alt) return;
    $('span', el).textContent = data[pref].text;
    var go = $('a', el), x = $('.x', el);
    go.textContent = data[pref].go; go.href = alt.href; go.setAttribute('lang', pref);
    x.setAttribute('aria-label', data[pref].close);
    el.setAttribute('dir', pref === 'ar' ? 'rtl' : 'ltr'); el.setAttribute('lang', pref);
    el.classList.add('show');
    go.addEventListener('click', function () { LS.set('sc_lang', pref); });
    x.addEventListener('click', function () { el.classList.remove('show'); LS.set('sc_lang', pageLang); });
  })();

  /* 7. Back to top */
  var top = $('.back-top');
  if (top) {
    var onScroll = function () { top.classList.toggle('show', window.scrollY > 700); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    top.addEventListener('click', function () { window.scrollTo({ top: 0 }); });
  }

  /* 8. Product filter (products page) */
  var input = $('#filter');
  if (input) {
    var cards = $$('.card[data-s]'), empty = $('#empty'), chips = $$('.chip[data-cat]'), count = $('#count'), cat = 'all';
    var apply = function () {
      var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean), shown = 0;
      cards.forEach(function (c) {
        var s = c.getAttribute('data-s');
        var ok = (cat === 'all' || c.getAttribute('data-cat') === cat) && terms.every(function (t) { return s.indexOf(t) > -1; });
        c.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = count.getAttribute('data-tpl').replace('{n}', shown);
    };
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        cat = b.getAttribute('data-cat');
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        apply();
      });
    });
    input.addEventListener('input', apply);
    var q = new URLSearchParams(location.search).get('q'); if (q) input.value = q;
    var c0 = new URLSearchParams(location.search).get('cat');
    if (c0) { var b0 = chips.filter(function (x) { return x.getAttribute('data-cat') === c0; })[0]; if (b0) b0.click(); }
    apply();
  }
})();
