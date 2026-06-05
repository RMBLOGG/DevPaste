/* =============================================
   DevPaste — Main JavaScript
   ============================================= */

// ---- Theme Management ----
(function initTheme() {
  const stored = localStorage.getItem('devpaste-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', stored);
  updateThemeIcon(stored);
})();

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeIcon');
  if (!icon) return;
  icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
}

document.addEventListener('DOMContentLoaded', function () {

  // Theme toggle
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('devpaste-theme', next);
      updateThemeIcon(next);
    });
  }

  // Auto-dismiss flash toasts
  document.querySelectorAll('.toast.show').forEach(function (el) {
    setTimeout(function () {
      const toast = new bootstrap.Toast(el, { delay: 4000 });
      toast.show();
      setTimeout(function () { el.remove(); }, 4500);
    }, 200);
  });

  // Syntax highlight (if hljs is loaded and code blocks exist)
  if (typeof hljs !== 'undefined') {
    document.querySelectorAll('pre code').forEach(function (el) {
      hljs.highlightElement(el);
    });
  }

});

// ---- Toast Notification ----
function showToast(message, type = 'success') {
  const container = document.getElementById('jsToast');
  if (!container) return;

  const icons = {
    success: 'bi-check-circle-fill text-success',
    error: 'bi-exclamation-triangle-fill text-danger',
    info: 'bi-info-circle-fill text-info',
  };

  const id = 'toast-' + Date.now();
  const html = `
    <div id="${id}" class="toast show align-items-center toast-${type}" role="alert" aria-live="assertive">
      <div class="d-flex">
        <div class="toast-body">
          <i class="bi ${icons[type] || icons.info} me-2"></i>${escapeHtml(message)}
        </div>
        <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  `;

  container.insertAdjacentHTML('beforeend', html);
  const el = document.getElementById(id);

  setTimeout(function () {
    if (el) {
      el.classList.remove('show');
      setTimeout(function () { if (el.parentNode) el.remove(); }, 300);
    }
  }, 3500);
}

// ---- Clipboard Utilities ----
function copyToClipboard(text, successMessage) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text).then(function () {
      showToast(successMessage || 'Copied!', 'success');
      return true;
    }).catch(function () {
      fallbackCopy(text, successMessage);
    });
  } else {
    fallbackCopy(text, successMessage);
  }
}

function fallbackCopy(text, successMessage) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
    showToast(successMessage || 'Copied!', 'success');
  } catch (err) {
    showToast('Copy failed. Please copy manually.', 'error');
  }
  document.body.removeChild(ta);
}

// ---- Escape HTML ----
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---- Copy paste code (global, used by view.html inline scripts) ----
// These functions are exposed globally so inline onclick handlers can call them.
window.showToast = showToast;
window.copyToClipboard = copyToClipboard;
