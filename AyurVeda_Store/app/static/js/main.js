/* AyurVeda Store – Main JS */

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });

  // Confirm before deleting (admin)
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(el.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });

  // Quantity +/- buttons (product detail page)
  window.changeQty = function (delta) {
    var input = document.getElementById('quantity');
    if (!input) return;
    var val = parseInt(input.value) + delta;
    var max = parseInt(input.max) || 999;
    if (val >= 1 && val <= max) input.value = val;
  };

  // Highlight active nav link
  var path = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === path) {
      link.classList.add('active', 'text-success');
    }
  });
});
