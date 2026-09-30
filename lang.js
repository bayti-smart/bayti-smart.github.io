const LANGS_META = {
  ar: { dir: 'rtl', flag: '🇩🇿' }, en: { dir: 'ltr', flag: '🇺🇸' },
  fr: { dir: 'ltr', flag: '🇫🇷' }, es: { dir: 'ltr', flag: '🇪🇸' }, de: { dir: 'ltr', flag: '🇩🇪' },
};
const LANG_ORDER = ['ar', 'en', 'fr', 'es', 'de'];

(function () {
  var LANG = 'ar';
  try { LANG = localStorage.getItem('site_lang') || 'ar'; } catch (e) {}
  var contentLang = (LANG === 'ar') ? 'ar' : 'en'; // محتوى الصفحات الثابتة متوفر بالعربي والإنجليزي فقط حاليًا

  function apply() {
    var root = document.documentElement;
    root.lang = LANG;
    root.dir = LANGS_META[LANG].dir;
    document.querySelectorAll('[data-l]').forEach(function (el) {
      el.hidden = el.dataset.l !== contentLang;
    });
    var select = document.getElementById('langSelect');
    if (select) select.value = LANG;
    var t = document.body.dataset[contentLang === 'ar' ? 'titleAr' : 'titleEn'];
    if (t) document.title = t;
  }

  function buildLangSwitch() {
    var box = document.getElementById('langSwitch');
    if (!box) return;
    var select = document.createElement('select');
    select.id = 'langSelect';
    select.className = 'lang-select';
    select.setAttribute('aria-label', 'Language / اللغة');
    LANG_ORDER.forEach(function (code) {
      var opt = document.createElement('option');
      opt.value = code;
      opt.textContent = LANGS_META[code].flag + ' ' + code.toUpperCase();
      select.appendChild(opt);
    });
    select.value = LANG;
    select.addEventListener('change', function () {
      LANG = select.value;
      contentLang = (LANG === 'ar') ? 'ar' : 'en';
      try { localStorage.setItem('site_lang', LANG); } catch (e) {}
      apply();
    });
    box.appendChild(select);
  }

  function applyEyeComfort(on) {
    document.documentElement.classList.toggle('eye-comfort', on);
    var btn = document.getElementById('eyeComfortBtn');
    if (btn) btn.classList.toggle('is-active', on);
  }
  function initEyeComfort() {
    var btn = document.getElementById('eyeComfortBtn');
    if (!btn) return;
    var on = false;
    try { on = localStorage.getItem('eye_comfort') === '1'; } catch (e) {}
    applyEyeComfort(on);
    btn.addEventListener('click', function () {
      on = !on;
      try { localStorage.setItem('eye_comfort', on ? '1' : '0'); } catch (e) {}
      applyEyeComfort(on);
    });
  }

  function applyFontScale(scale) {
    document.documentElement.style.setProperty('--font-scale', scale);
  }
  function initFontControls() {
    var dec = document.getElementById('fontDec');
    var inc = document.getElementById('fontInc');
    if (!dec || !inc) return;
    var scale = 1;
    try { scale = parseFloat(localStorage.getItem('font_scale') || '1'); } catch (e) {}
    applyFontScale(scale);
    function save() { try { localStorage.setItem('font_scale', scale); } catch (e) {} applyFontScale(scale); }
    dec.addEventListener('click', function () { scale = Math.max(0.85, +(scale - 0.1).toFixed(2)); save(); });
    inc.addEventListener('click', function () { scale = Math.min(1.4, +(scale + 0.1).toFixed(2)); save(); });
  }

  function initBackToTop() {
    var btn = document.getElementById('backToTop');
    if (!btn) return;
    window.addEventListener('scroll', function () {
      btn.classList.toggle('is-visible', window.scrollY > 500);
    });
    btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  buildLangSwitch();
  initEyeComfort();
  initFontControls();
  initBackToTop();
  apply();
})();
