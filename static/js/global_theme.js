(function () {
  const THEME_KEY = 'mths-theme';

  function getStoredTheme() {
    return localStorage.getItem(THEME_KEY) || 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
    }
  }

  applyTheme(getStoredTheme());

  document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function () {
        const current = getStoredTheme();
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    const menuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    if (menuBtn && sidebar) {
      menuBtn.addEventListener('click', function () {
        sidebar.classList.toggle('open');
      });
    }

    document.querySelectorAll('.nav-link').forEach(function (link) {
      if (link.href === window.location.href) {
        link.classList.add('active');
      }
    });
  });
})();
