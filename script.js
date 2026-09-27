const UI = {
  ar: {
    dir: 'rtl',
    brandName: 'بيتي الذكي',
    pageTitle: 'بيتي الذكي — أفضل إكسسوارات المنزل الذكي',
    all: 'الكل',
    searchPlaceholder: 'ابحث عن جهاز...',
    heroTitle: 'منزلك أذكى بخطوة واحدة',
    heroSub: 'جمعنا لك أفضل أجهزة المنزل الذكي بعد مقارنة الأسعار والتقييمات، حتى توفّر وقت البحث وتشتري بثقة.',
    statProducts: 'منتج مُختار',
    statCategories: 'فئات',
    statUpdated: 'آخر تحديث',
    emptyState: 'لا توجد منتجات مطابقة لبحثك. جرّب كلمة أخرى.',
    disclosure: 'إفصاح: هذا الموقع يشارك في برامج تسويق بالعمولة (Amazon Associates، AliExpress Affiliate)، وقد نحصل على عمولة عند الشراء عبر روابطنا دون أي تكلفة إضافية عليك.',
    viewProduct: 'عرض المنتج',
    locale: 'ar-EG',
  },
  en: {
    dir: 'ltr',
    brandName: 'Smart Casa',
    pageTitle: 'Smart Casa — Best Smart Home Accessories',
    all: 'All',
    searchPlaceholder: 'Search for a device...',
    heroTitle: 'A smarter home, one step away',
    heroSub: 'We compared prices and ratings to hand-pick the best smart home devices, so you save research time and buy with confidence.',
    statProducts: 'curated products',
    statCategories: 'categories',
    statUpdated: 'last updated',
    emptyState: 'No products match your search. Try a different term.',
    disclosure: 'Disclosure: this site participates in affiliate programs (Amazon Associates, AliExpress Affiliate). We may earn a commission on purchases through our links at no extra cost to you.',
    viewProduct: 'View product',
    locale: 'en-US',
  },
};

let ALL_PRODUCTS = [];
let ALL_CATEGORIES = [];
let ACTIVE_CATEGORY = 'all';
let LANG = localStorage.getItem('site_lang') || 'ar';
let LAST_UPDATED = null;

function t(key) {
  return (UI[LANG] && UI[LANG][key]) || (UI.ar[key] || key);
}

function applyLanguage() {
  document.getElementById('htmlRoot').setAttribute('lang', LANG);
  document.getElementById('htmlRoot').setAttribute('dir', UI[LANG].dir);
  document.title = t('pageTitle');

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (key === 'copyright') {
      el.innerHTML = (LANG === 'ar' ? '© ' : '© ') + '<span id="year"></span> ' + t('brandName');
      document.getElementById('year').textContent = new Date().getFullYear();
    } else {
      el.textContent = t(key);
    }
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('is-active', btn.dataset.lang === LANG);
  });

  renderCategoryLabels();
  renderStats();
  renderGrid();
}

async function loadProducts() {
  try {
    const res = await fetch('products.json?_=' + Date.now());
    const data = await res.json();
    ALL_PRODUCTS = data.products || [];
    ALL_CATEGORIES = data.categories || [];
    LAST_UPDATED = data.updated_at || null;
    renderCategoryButtons();
    applyLanguage();
  } catch (err) {
    console.error('فشل تحميل المنتجات / Failed to load products:', err);
    document.getElementById('productGrid').innerHTML =
      '<p>تعذّر تحميل المنتجات حاليًا / Could not load products right now.</p>';
  }
}

function renderStats() {
  document.getElementById('statCount').textContent = ALL_PRODUCTS.length;
  if (LAST_UPDATED) {
    const d = new Date(LAST_UPDATED);
    document.getElementById('statUpdated').textContent =
      d.toLocaleDateString(t('locale'), { year: 'numeric', month: 'short', day: 'numeric' });
  }
}

function renderCategoryButtons() {
  const nav = document.getElementById('catNav');
  nav.querySelectorAll('.cat-btn:not([data-cat="all"])').forEach(b => b.remove());
  ALL_CATEGORIES.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'cat-btn';
    btn.dataset.cat = cat.id;
    btn.textContent = cat.name[LANG] || cat.name.ar;
    btn.addEventListener('click', () => setActiveCategory(cat.id));
    nav.appendChild(btn);
  });
}

function renderCategoryLabels() {
  document.querySelectorAll('.cat-btn').forEach(btn => {
    if (btn.dataset.cat === 'all') return;
    const cat = ALL_CATEGORIES.find(c => c.id === btn.dataset.cat);
    if (cat) btn.textContent = cat.name[LANG] || cat.name.ar;
  });
}

function setActiveCategory(catId) {
  ACTIVE_CATEGORY = catId;
  document.querySelectorAll('.cat-btn').forEach(b => {
    b.classList.toggle('is-active', b.dataset.cat === catId);
  });
  renderGrid();
}

function localize(product) {
  return product.i18n[LANG] || product.i18n.ar || product.i18n.en;
}

function renderGrid() {
  const grid = document.getElementById('productGrid');
  const emptyState = document.getElementById('emptyState');
  const query = document.getElementById('searchInput').value.trim().toLowerCase();

  const filtered = ALL_PRODUCTS.filter(p => {
    const text = localize(p);
    const matchesCat = ACTIVE_CATEGORY === 'all' || p.category === ACTIVE_CATEGORY;
    const matchesQuery = !query ||
      text.title.toLowerCase().includes(query) ||
      (text.description || '').toLowerCase().includes(query);
    return matchesCat && matchesQuery;
  });

  grid.innerHTML = filtered.map(renderCard).join('');
  emptyState.hidden = filtered.length > 0;
}

function renderCard(p) {
  const text = localize(p);
  const tags = (text.tags || []).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
  const stars = '★'.repeat(Math.round(p.rating || 0));
  return `
    <article class="card">
      <img class="card-img" src="${escapeHtml(p.image)}" alt="${escapeHtml(text.title)}" loading="lazy">
      <div class="card-body">
        <div class="card-tags">${tags}</div>
        <h3 class="card-title">${escapeHtml(text.title)}</h3>
        <p class="card-desc">${escapeHtml(text.description || '')}</p>
        <div class="card-meta">
          <span class="rating"><strong>${stars}</strong> (${p.reviews_count || 0})</span>
          <span class="price">${p.price} <small>${p.currency || ''}</small></span>
        </div>
        <a class="buy-btn" href="${escapeHtml(p.affiliate_url)}" target="_blank" rel="nofollow sponsored noopener">
          ${escapeHtml(t('viewProduct'))}
        </a>
      </div>
    </article>
  `;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str ?? '';
  return div.innerHTML;
}

document.getElementById('searchInput').addEventListener('input', () => renderGrid());
document.querySelector('[data-cat="all"]').addEventListener('click', () => setActiveCategory('all'));

document.querySelectorAll('.lang-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    LANG = btn.dataset.lang;
    localStorage.setItem('site_lang', LANG);
    applyLanguage();
  });
});

loadProducts();
