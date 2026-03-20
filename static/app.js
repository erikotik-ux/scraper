/* ============================================
   ANTIGRAVITY INTELLIGENCE — DASHBOARD JS
   ============================================ */

const SAVED_KEY = 'ag_saved_articles';
let allArticles = [];
let currentFilter = 'all';

// ---- UTILS ----

function getSaved() {
  try { return JSON.parse(localStorage.getItem(SAVED_KEY) || '[]'); }
  catch { return []; }
}

function setSaved(ids) {
  localStorage.setItem(SAVED_KEY, JSON.stringify(ids));
}

function toggleSave(articleId, event) {
  event.preventDefault();
  event.stopPropagation();
  const saved = getSaved();
  const idx = saved.indexOf(articleId);
  if (idx > -1) saved.splice(idx, 1);
  else saved.push(articleId);
  setSaved(saved);
  renderArticles();
  updateCounts();
}

function timeAgo(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  if (isNaN(date)) return '';
  const diffMs = Date.now() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 1)  return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  return `${Math.floor(diffHours / 24)}d ago`;
}

function sourceClass(source) {
  if (source === 'bens_bites') return 'bens_bites';
  if (source === 'ai_rundown') return 'ai_rundown';
  return 'reddit';
}

function sourceLabel(article) {
  return article.source_display || article.source;
}

function formatLastUpdated(isoStr) {
  if (!isoStr) return 'Never refreshed';
  const date = new Date(isoStr);
  if (isNaN(date)) return '';
  return `Updated ${timeAgo(isoStr)}`;
}

function setCurrentDate() {
  const el = document.getElementById('current-date');
  if (!el) return;
  const now = new Date();
  el.textContent = now.toLocaleDateString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric', year: 'numeric'
  });
}

// ---- COUNTS ----

function updateCounts() {
  const saved = getSaved();
  const counts = { all: allArticles.length, bens_bites: 0, ai_rundown: 0, reddit: 0, saved: 0 };

  allArticles.forEach(a => {
    if (a.source === 'bens_bites') counts.bens_bites++;
    else if (a.source === 'ai_rundown') counts.ai_rundown++;
    else if (a.source === 'reddit') counts.reddit++;
    if (saved.includes(a.id)) counts.saved++;
  });

  document.getElementById('count-all').textContent     = counts.all;
  document.getElementById('count-bens').textContent    = counts.bens_bites;
  document.getElementById('count-rundown').textContent = counts.ai_rundown;
  document.getElementById('count-reddit').textContent  = counts.reddit;
  document.getElementById('count-saved').textContent   = counts.saved;
}

// ---- FILTER ----

function setFilter(filter) {
  currentFilter = filter;
  document.querySelectorAll('.pill').forEach(p => {
    p.classList.toggle('active', p.dataset.filter === filter);
  });
  renderArticles();
}

function filteredArticles() {
  const saved = getSaved();
  if (currentFilter === 'all') return allArticles;
  if (currentFilter === 'saved') return allArticles.filter(a => saved.includes(a.id));
  return allArticles.filter(a => a.source === currentFilter);
}

// ---- RENDER ----

function buildCard(article) {
  const saved = getSaved();
  const isSaved = saved.includes(article.id);
  const cls = sourceClass(article.source);
  const label = sourceLabel(article);
  const ago = timeAgo(article.published_at);

  const tagsHtml = (article.tags || []).map(t =>
    `<span class="card-tag">${escHtml(t)}</span>`
  ).join('');

  const imageHtml = article.thumbnail
    ? `<div class="card-image"><img src="${escAttr(article.thumbnail)}" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>`
    : '';

  return `
    <div class="article-card" onclick="openArticle('${escAttr(article.url)}')">
      ${imageHtml}
      <div class="card-header">
        <div class="card-header-left">
          <span class="source-badge ${cls}">${escHtml(label)}</span>
          ${ago ? `<span class="card-time">${ago}</span>` : ''}
        </div>
        <button class="btn-save ${isSaved ? 'saved' : ''}"
                onclick="toggleSave('${escAttr(article.id)}', event)"
                title="${isSaved ? 'Unsave' : 'Save article'}">
          ${isSaved
            ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>`
            : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>`
          }
        </button>
      </div>

      <div class="card-title">${escHtml(article.title)}</div>

      ${article.summary
        ? `<div class="card-summary">${escHtml(article.summary)}</div>`
        : ''
      }

      <div class="card-footer">
        <div class="card-tags">${tagsHtml}</div>
        <a class="btn-read" href="${escAttr(article.url)}" target="_blank" rel="noopener"
           onclick="event.stopPropagation()">
          Read
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7 17L17 7M17 7H7M17 7v10"/>
          </svg>
        </a>
      </div>
    </div>
  `;
}

function renderArticles() {
  const grid = document.getElementById('articles-grid');
  const emptyState = document.getElementById('empty-state');
  const articles = filteredArticles();

  grid.innerHTML = '';

  if (articles.length === 0) {
    emptyState.style.display = 'flex';
    const title = document.getElementById('empty-title');
    const sub = document.getElementById('empty-sub');
    if (currentFilter === 'saved') {
      title.textContent = 'No saved articles yet';
      sub.textContent = 'Bookmark articles to find them here later.';
    } else {
      title.textContent = 'No articles in the last 7 days';
      sub.textContent = 'Try refreshing to fetch the latest content.';
    }
    return;
  }

  emptyState.style.display = 'none';
  grid.innerHTML = articles.map(buildCard).join('');
}

function openArticle(url) {
  window.open(url, '_blank', 'noopener,noreferrer');
}

// ---- ESCAPE HELPERS ----

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escAttr(str) {
  if (!str) return '';
  return String(str).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// ---- FETCH ----

async function fetchArticles() {
  showSkeletons();
  try {
    const res = await fetch('/api/articles');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    allArticles = data.articles || [];
    updateLastUpdated(data.last_scraped);
    updateCounts();
    renderArticles();
  } catch (err) {
    console.error('[fetch]', err);
    showError('Failed to load articles. Is the server running?');
  }
}

async function refreshArticles() {
  const btn = document.getElementById('refresh-btn');
  btn.classList.add('loading');
  btn.disabled = true;

  try {
    const res = await fetch('/api/refresh', { method: 'POST' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    allArticles = data.articles || [];
    updateLastUpdated(data.last_scraped);
    updateCounts();
    renderArticles();
  } catch (err) {
    console.error('[refresh]', err);
    alert('Refresh failed. Check the console for details.');
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

// ---- UI HELPERS ----

function showSkeletons() {
  const grid = document.getElementById('articles-grid');
  grid.innerHTML = Array(6).fill('<div class="skeleton-card"></div>').join('');
  document.getElementById('empty-state').style.display = 'none';
}

function showError(msg) {
  const grid = document.getElementById('articles-grid');
  grid.innerHTML = '';
  document.getElementById('empty-state').style.display = 'flex';
  document.getElementById('empty-title').textContent = 'Something went wrong';
  document.getElementById('empty-sub').textContent = msg;
}

function updateLastUpdated(isoStr) {
  const el = document.getElementById('last-updated');
  if (el) el.textContent = formatLastUpdated(isoStr);
}

// ---- INIT ----

document.addEventListener('DOMContentLoaded', () => {
  setCurrentDate();
  fetchArticles();
});
