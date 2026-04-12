/* SpecAg Website — Main JS */

(function () {
  // Theme toggle
  const toggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  const saved = localStorage.getItem('specag-theme');

  if (saved) {
    html.setAttribute('data-theme', saved);
    toggle.textContent = saved === 'dark' ? '\u2600' : '\u263D';
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    html.setAttribute('data-theme', 'dark');
    toggle.textContent = '\u2600';
  }

  toggle.addEventListener('click', function () {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('specag-theme', next);
    toggle.textContent = next === 'dark' ? '\u2600' : '\u263D';
  });

  // Mobile hamburger menu
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', function () {
      nav.classList.toggle('open');
      hamburger.textContent = nav.classList.contains('open') ? '\u2715' : '\u2630';
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        hamburger.textContent = '\u2630';
      });
    });
  }

  // Tab functionality
  document.querySelectorAll('.tabs').forEach(function (tabContainer) {
    var buttons = tabContainer.querySelectorAll('.tab');
    var panels = tabContainer.parentElement.querySelectorAll('.tab-panel');

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = btn.getAttribute('data-tab');

        buttons.forEach(function (b) { b.classList.remove('active'); });
        panels.forEach(function (p) { p.classList.remove('active'); });

        btn.classList.add('active');
        var panel = document.getElementById(target);
        if (panel) panel.classList.add('active');
      });
    });
  });
})();

// Copy install command
function copyInstall() {
  navigator.clipboard.writeText('pip install specag').then(function () {
    var btns = document.querySelectorAll('.copy-btn');
    btns.forEach(function (btn) {
      var original = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(function () { btn.textContent = original; }, 2000);
    });
  });
}
