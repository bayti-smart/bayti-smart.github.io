(function () {
  var LANG = 'ar';
  try { LANG = localStorage.getItem('site_lang') || 'ar'; } catch (e) {}

  function apply() {
    var root = document.documentElement;
    root.lang = LANG;
    root.dir = LANG === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-l]').forEach(function (el) {
      el.hidden = el.dataset.l !== LANG;
    });
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      b.classList.toggle('is-active', b.dataset.lang === LANG);
    });
    var t = document.body.dataset[LANG === 'ar' ? 'titleAr' : 'titleEn'];
    if (t) document.title = t;
  }

  document.querySelectorAll('.lang-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      LANG = b.dataset.lang;
      try { localStorage.setItem('site_lang', LANG); } catch (e) {}
      apply();
    });
  });

  apply();
})();
