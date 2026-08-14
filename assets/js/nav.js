// Mobile menu. The nav is visible by default so it still works with JS off;
// this script only takes over below the 860px breakpoint.
(function () {
  var btn = document.querySelector('.navToggle');
  var nav = document.getElementById('primaryNav');
  if (!btn || !nav) return;

  var mq = window.matchMedia('(max-width: 860px)');

  function sync() {
    if (mq.matches) {
      nav.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    } else {
      nav.hidden = false;
    }
  }

  btn.addEventListener('click', function () {
    var open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    nav.hidden = open;
  });

  mq.addEventListener('change', sync);
  sync();
})();
