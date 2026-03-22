/**
 * Vidya Prakashan Mandir — Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss alerts after 5 seconds ──────────────────
  document.querySelectorAll('.vp-alert').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // ── Smooth scroll for anchor links ───────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Navbar scroll effect ──────────────────────────────────
  const navbar = document.querySelector('.vp-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
      } else {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.3)';
      }
    });
  }

  // ── Add to cart AJAX handler ──────────────────────────────
  document.querySelectorAll('.add-to-cart-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const bookId = this.dataset.bookId;
      const csrfToken = getCookie('csrftoken');

      fetch(`/cart/add/${bookId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Update cart badge
          const badge = document.querySelector('.navbar .badge');
          if (badge) {
            badge.textContent = data.cart_count;
            badge.style.display = 'inline';
          }
          // Show toast
          showToast(data.message || 'Added to cart!', 'success');
          // Animate button
          this.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i>Added!';
          this.classList.add('btn-success');
          setTimeout(() => {
            this.innerHTML = '<i class="bi bi-cart-plus me-1"></i>Add to Cart';
            this.classList.remove('btn-success');
          }, 2000);
        }
      })
      .catch(err => {
        showToast('Please login to add items to cart.', 'warning');
      });
    });
  });

  // ── Fade-in animation on scroll ──────────────────────────
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.book-card, .category-card, .stat-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });

  // ── Toast notification helper ─────────────────────────────
  window.showToast = function (message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;flex-direction:column;gap:0.5rem;';
      document.body.appendChild(container);
    }

    const icons = { success: 'check-circle-fill', warning: 'exclamation-triangle-fill', danger: 'x-circle-fill', info: 'info-circle-fill' };
    const colors = { success: '#198754', warning: '#fd7e14', danger: '#dc3545', info: '#0d6efd' };

    const toast = document.createElement('div');
    toast.style.cssText = `background:#fff;border:1px solid #dee2e6;border-radius:10px;padding:0.85rem 1.25rem;
      box-shadow:0 8px 24px rgba(0,0,0,0.12);display:flex;align-items:center;gap:0.75rem;
      min-width:260px;border-left:4px solid ${colors[type]};animation:fadeInUp 0.3s ease;`;
    toast.innerHTML = `
      <i class="bi bi-${icons[type]}" style="color:${colors[type]};font-size:1.1rem;"></i>
      <span style="font-size:0.88rem;flex:1;">${message}</span>
      <button onclick="this.parentElement.remove()" style="background:none;border:none;cursor:pointer;font-size:1rem;color:#6c757d;">×</button>`;

    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  };

  // ── CSRF cookie helper ────────────────────────────────────
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(function (cookie) {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(c.substring(name.length + 1));
        }
      });
    }
    return cookieValue;
  }

  // ── Quantity input validation ─────────────────────────────
  document.querySelectorAll('input[type="number"][name="quantity"]').forEach(function (input) {
    input.addEventListener('change', function () {
      if (this.value < 1) this.value = 1;
      if (this.value > 99) this.value = 99;
    });
  });

  // ── Star rating UI ────────────────────────────────────────
  const stars = document.querySelectorAll('.star-input');
  stars.forEach(function (star) {
    star.addEventListener('mouseover', function () {
      const val = this.dataset.value;
      stars.forEach(s => {
        s.style.color = parseInt(s.dataset.value) <= parseInt(val) ? '#ffc107' : '#dee2e6';
      });
    });
    star.addEventListener('click', function () {
      const val = this.dataset.value;
      const ratingInput = document.querySelector('input[name="rating"]');
      if (ratingInput) ratingInput.value = val;
    });
  });

});
