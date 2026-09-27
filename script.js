let ALL_PRODUCTS = [];
let ACTIVE_CATEGORY = 'all';

async function loadProducts() {
  try {
    const res = await fetch('products.json?_=' + Date.now());
    const data = await res.json();
    ALL_PRODUCTS = data.products || [];
    renderCategories(data.categories || []);
    renderStats(data);
    renderGrid();
  } catch (err) {
    console.error('فشل تحميل المنتجات:', err);
    document.getElementById('productGrid').innerHTML =
      '<p>تعذّر تحميل المنتجات حاليًا. حاول تحديث الصفحة.</p>';
  }
}

function renderStats(data) {
  document.getElementById('statCount').textContent = (data.products || []).length;
  if (data.updated_at) {
    const d = new Date(data.updated_at);
    document.getElementById('statUpdated').textContent =
      d.toLocaleDateString('ar-EG', { year: 'numeric', month: 'short', day: 'numeric' });
  }
}

function renderCategories(categories) {
  const nav = document.getElementById('catNav');
  categories.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'cat-btn';
    btn.dataset.cat = cat.id;
    btn.textContent = cat.name;
    btn.addEventListener('click', () => setActiveCategory(cat.id));
    nav.appendChild(btn);
  });
}

function setActiveCategory(catId) {
  ACTIVE_CATEGORY = catId;
  document.querySelectorAll('.cat-btn').forEach(b => {
    b.classList.toggle('is-active', b.dataset.cat === catId);
  });
  renderGrid();
}

function renderGrid() {
  const grid = document.getElementById('productGrid');
  const emptyState = document.getElementById('emptyState');
  const query = document.getElementById('searchInput').value.trim().toLowerCase();

  const filtered = ALL_PRODUCTS.filter(p => {
    const matchesCat = ACTIVE_CATEGORY === 'all' || p.category === ACTIVE_CATEGORY;
    const matchesQuery = !query || p.title.toLowerCase().includes(query) ||
      (p.description || '').toLowerCase().includes(query);
    return matchesCat && matchesQuery;
  });

  grid.innerHTML = filtered.map(renderCard).join('');
  emptyState.hidden = filtered.length > 0;
}

function renderCard(p) {
  const tags = (p.tags || []).map(t => `<span class="tag">${escapeHtml(t)}</span>`).join('');
  const stars = '★'.repeat(Math.round(p.rating || 0));
  return `
    <article class="card">
      <img class="card-img" src="${escapeHtml(p.image)}" alt="${escapeHtml(p.title)}" loading="lazy">
      <div class="card-body">
        <div class="card-tags">${tags}</div>
        <h3 class="card-title">${escapeHtml(p.title)}</h3>
        <p class="card-desc">${escapeHtml(p.description || '')}</p>
        <div class="card-meta">
          <span class="rating"><strong>${stars}</strong> (${p.reviews_count || 0})</span>
          <span class="price">${p.price} <small>${p.currency || ''}</small></span>
        </div>
        <a class="buy-btn" href="${escapeHtml(p.affiliate_url)}" target="_blank" rel="nofollow sponsored noopener">
          عرض المنتج
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
document.getElementById('year').textContent = new Date().getFullYear();

loadProducts();
