// DevPaste — main.js

// ── THEME ──
(function() {
  const stored = localStorage.getItem('dp-theme');
  if (stored === 'light') document.documentElement.setAttribute('data-theme', 'light');
  else document.documentElement.setAttribute('data-theme', 'dark');
})();

document.addEventListener('DOMContentLoaded', function() {

  // ── THEME TOGGLE ──
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon   = document.getElementById('themeIcon');

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('dp-theme', t);
    if (themeIcon) {
      themeIcon.className = t === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
    }
  }

  const current = localStorage.getItem('dp-theme') || 'dark';
  applyTheme(current);

  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      const cur = document.documentElement.getAttribute('data-theme') || 'dark';
      applyTheme(cur === 'dark' ? 'light' : 'dark');
    });
  }

  // ── NAVBAR TOGGLER ──
  const toggler  = document.querySelector('.navbar-toggler');
  const collapse = document.getElementById('navbarContent');
  if (toggler && collapse) {
    toggler.addEventListener('click', function() {
      collapse.classList.toggle('show');
    });
    document.addEventListener('click', function(e) {
      if (!toggler.contains(e.target) && !collapse.contains(e.target)) {
        collapse.classList.remove('show');
      }
    });
  }

  // ── AUTO-DISMISS TOASTS ──
  document.querySelectorAll('.toast.show').forEach(function(el) {
    setTimeout(function() {
      el.classList.remove('show');
    }, 4000);
  });
  document.querySelectorAll('.btn-close[data-bs-dismiss="toast"]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      btn.closest('.toast').classList.remove('show');
    });
  });

  // ── JS TOAST HELPER ──
  window.showToast = function(msg, type) {
    type = type || 'info';
    const container = document.getElementById('jsToast');
    if (!container) return;
    const colors = { success: 'var(--green)', error: 'var(--red)', info: 'var(--cyan)' };
    const icons  = { success: 'bi-check-circle-fill', error: 'bi-exclamation-triangle-fill', info: 'bi-info-circle-fill' };
    const div = document.createElement('div');
    div.className = 'toast show align-items-center';
    div.style.borderLeft = '3px solid ' + (colors[type] || colors.info);
    div.innerHTML =
      '<div class="d-flex">' +
        '<div class="toast-body">' +
          '<i class="bi ' + (icons[type] || icons.info) + ' me-2" style="color:' + (colors[type] || colors.info) + '"></i>' +
          msg +
        '</div>' +
        '<button type="button" class="btn-close me-2 m-auto"></button>' +
      '</div>';
    div.querySelector('.btn-close').addEventListener('click', function() { div.remove(); });
    container.appendChild(div);
    setTimeout(function() { div.remove(); }, 4000);
  };

  // ── COPY TO CLIPBOARD ──
  document.querySelectorAll('[data-copy]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const target = document.getElementById(btn.dataset.copy);
      const text   = btn.dataset.copyText || (target ? target.textContent : '');
      navigator.clipboard.writeText(text.trim()).then(function() {
        btn.classList.add('copy-done');
        const orig = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check2"></i> Copied';
        setTimeout(function() {
          btn.classList.remove('copy-done');
          btn.innerHTML = orig;
        }, 2000);
        showToast('Disalin ke clipboard!', 'success');
      }).catch(function() {
        showToast('Gagal menyalin.', 'error');
      });
    });
  });

  // ── COPY RAW URL ──
  const copyUrlBtn = document.getElementById('copyUrlBtn');
  if (copyUrlBtn) {
    copyUrlBtn.addEventListener('click', function() {
      navigator.clipboard.writeText(window.location.href).then(function() {
        showToast('URL disalin!', 'success');
      });
    });
  }

  // ── HIGHLIGHT.JS ──
  if (typeof hljs !== 'undefined') {
    document.querySelectorAll('pre code').forEach(function(block) {
      hljs.highlightElement(block);
    });
  }

  // ── LINE NUMBERS ──
  const codeBlock = document.getElementById('pasteCode');
  const lnBlock   = document.getElementById('lineNumbers');
  if (codeBlock && lnBlock) {
    var lines = codeBlock.textContent.split('\n');
    // Remove trailing empty line
    if (lines[lines.length - 1] === '') lines.pop();
    lnBlock.innerHTML = lines.map(function(_, i) {
      return '<span>' + (i + 1) + '</span>';
    }).join('');
  }

  // ── DELETE MODAL ──
  const deleteBtn   = document.getElementById('deleteBtn');
  const deleteModal = document.getElementById('deleteModal');
  const cancelDel   = document.getElementById('cancelDelete');
  if (deleteBtn && deleteModal) {
    deleteBtn.addEventListener('click', function() {
      deleteModal.style.display = 'flex';
    });
  }
  if (cancelDel && deleteModal) {
    cancelDel.addEventListener('click', function() {
      deleteModal.style.display = 'none';
    });
  }
  if (deleteModal) {
    deleteModal.addEventListener('click', function(e) {
      if (e.target === deleteModal) deleteModal.style.display = 'none';
    });
  }

});
