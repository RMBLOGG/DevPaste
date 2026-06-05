// DevPaste — main.js

// Theme toggle
document.addEventListener('DOMContentLoaded', function () {
  const html = document.documentElement;
  const btn = document.getElementById('themeToggle');
  const icon = document.getElementById('themeIcon');
  const saved = localStorage.getItem('devpaste-theme') || 'dark';

  html.setAttribute('data-theme', saved);
  updateIcon(saved);

  if (btn) {
    btn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('devpaste-theme', next);
      updateIcon(next);
    });
  }

  function updateIcon(theme) {
    if (!icon) return;
    icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
  }

  // Auto-dismiss toasts
  document.querySelectorAll('.toast.show').forEach(el => {
    setTimeout(() => {
      const bsToast = bootstrap.Toast.getOrCreateInstance(el);
      bsToast.hide();
    }, 4000);
  });
});

// Show JS toast notification
function showToast(message, type = 'info') {
  const container = document.getElementById('jsToast');
  if (!container) return;

  const typeClass = type === 'success' ? 'toast-success' : type === 'error' ? 'toast-error' : 'toast-info';
  const icon = type === 'success' ? 'bi-check-circle-fill' : type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle';

  const el = document.createElement('div');
  el.className = `toast show align-items-center ${typeClass}`;
  el.setAttribute('role', 'alert');
  el.innerHTML = `
    <div class="d-flex">
      <div class="toast-body" style="font-size:12px;font-family:var(--font-mono)">
        <i class="bi ${icon} me-2"></i>${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>`;

  container.appendChild(el);
  setTimeout(() => { el.remove(); }, 3500);
}
