/* ============================================
   TriDAV Impex – Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ---- Page Loading Overlay ----
  const loader = document.getElementById('page-loader');
  if (loader) {
    setTimeout(() => { loader.classList.add('loaded'); }, 300);
  }

  // ---- Navbar Scroll Effect ----
  const navbar = document.getElementById('navbar');
  const handleNavScroll = () => {
    if (window.scrollY > 20) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', handleNavScroll, { passive: true });

  // ---- Mobile Menu Toggle ----
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuIcon = document.getElementById('menu-icon');
  const closeIcon = document.getElementById('close-icon');

  mobileToggle?.addEventListener('click', () => {
    const isOpen = !mobileMenu.classList.contains('hidden');
    mobileMenu.classList.toggle('hidden', isOpen);
    menuIcon?.classList.toggle('hidden', !isOpen);
    closeIcon?.classList.toggle('hidden', isOpen);
    document.body.style.overflow = isOpen ? '' : 'hidden';
  });

  // Close mobile menu on outside click
  document.addEventListener('click', (e) => {
    if (mobileMenu && !mobileMenu.classList.contains('hidden') &&
        !mobileToggle?.contains(e.target) &&
        !mobileMenu?.contains(e.target)) {
      mobileMenu.classList.add('hidden');
      menuIcon?.classList.remove('hidden');
      closeIcon?.classList.add('hidden');
      document.body.style.overflow = '';
    }
  });

  // ---- Search Bar Toggle ----
  const searchToggle = document.getElementById('search-toggle');
  const searchBar = document.getElementById('search-bar');

  searchToggle?.addEventListener('click', () => {
    const isHidden = searchBar.classList.contains('hidden');
    searchBar.classList.toggle('hidden', !isHidden);
    if (isHidden) {
      searchBar.querySelector('input')?.focus();
    }
  });

  // ---- Scroll Reveal Animation ----
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  };

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => {
    revealObserver.observe(el);
  });

  // ---- Lazy Load Images ----
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imageObserver.unobserve(img);
        }
      });
    }, { rootMargin: '200px 0px' });

    lazyImages.forEach(img => imageObserver.observe(img));
  }

  // ---- Parallax Background on Hero ----
  const parallaxBg = document.querySelector('.parallax-bg');
  if (parallaxBg) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      parallaxBg.style.transform = `translateY(${scrollY * 0.3}px)`;
    }, { passive: true });
  }

  // ---- Smooth number counter for Stats ----
  const countupEls = document.querySelectorAll('[data-countup]');
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.countup, 10);
        const suffix = el.dataset.suffix || '';
        animateCounter(el, 0, target, 1500, suffix);
        countObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  countupEls.forEach(el => countObserver.observe(el));

  function animateCounter(el, from, to, duration, suffix) {
    const startTime = performance.now();
    const update = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(from + (to - from) * eased) + suffix;
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  }

  // ---- Quick View Modal ----
  window.quickView = function(slug) {
    const modal = document.getElementById('quick-view-modal');
    const content = document.getElementById('quick-view-content');
    if (!modal || !content) return;

    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
    content.innerHTML = '<div class="animate-pulse text-gray-400 text-center py-10">Loading product details...</div>';

    fetch(`/products/${slug}/quick-view/`)
      .then(res => res.json())
      .then(data => {
        content.className = 'w-full';
        content.innerHTML = `
          <h2 class="font-serif text-2xl font-bold text-charcoal-900 mb-1">${data.name}</h2>
          <p class="text-sm text-gray-500 mb-4">${data.short_description || ''}</p>
          <div class="grid grid-cols-2 gap-3 text-sm mb-5">
            ${data.material ? `<div><span class="text-xs text-gray-400 uppercase">Material</span><p class="font-medium text-gray-800">${data.material}</p></div>` : ''}
            ${data.gsm ? `<div><span class="text-xs text-gray-400 uppercase">GSM</span><p class="font-medium text-gray-800">${data.gsm} g/m²</p></div>` : ''}
            ${data.thread_count ? `<div><span class="text-xs text-gray-400 uppercase">Thread Count</span><p class="font-medium text-gray-800">${data.thread_count}TC</p></div>` : ''}
            ${data.size ? `<div><span class="text-xs text-gray-400 uppercase">Sizes</span><p class="font-medium text-gray-800">${data.size}</p></div>` : ''}
            <div><span class="text-xs text-gray-400 uppercase">Min. Order</span><p class="font-medium text-gray-800">${data.moq} pcs</p></div>
            ${data.price_range ? `<div><span class="text-xs text-gray-400 uppercase">Price Range</span><p class="font-medium text-gray-800">${data.price_range}</p></div>` : ''}
          </div>
          <div class="flex gap-3">
            <a href="${data.url}" class="flex-1 text-center bg-sand-600 text-white font-semibold py-3 rounded-xl hover:bg-sand-700 transition-colors text-sm">View Full Details</a>
            <a href="/inquiry/bulk/?product=${encodeURIComponent(data.name)}" class="flex-1 text-center bg-charcoal-900 text-white font-semibold py-3 rounded-xl hover:bg-charcoal-800 transition-colors text-sm">Get Quote</a>
          </div>
        `;
      })
      .catch(() => {
        content.className = 'w-full';
        content.innerHTML = '<p class="text-center text-gray-500 py-10">Could not load product. <a href="/products/" class="text-sand-600 underline">Browse all products</a>.</p>';
      });
  };

  window.closeQuickView = function() {
    const modal = document.getElementById('quick-view-modal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      document.body.style.overflow = '';
    }
  };

  // Close modal on backdrop click
  document.getElementById('quick-view-modal')?.addEventListener('click', function(e) {
    if (e.target === this) closeQuickView();
  });

  // Close modal on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeQuickView();
  });

  // ---- Sticky CTA Visibility ----
  const stickyCta = document.getElementById('sticky-cta');
  if (stickyCta) {
    const showAfter = 400;
    window.addEventListener('scroll', () => {
      if (window.scrollY > showAfter) {
        stickyCta.classList.remove('hidden');
      } else {
        stickyCta.classList.add('hidden');
      }
    }, { passive: true });
  }

  // ---- Product Image Thumbnail Change ----
  window.changeImage = function(url, btn) {
    const mainImg = document.getElementById('main-product-image');
    if (mainImg) {
      mainImg.style.opacity = '0.6';
      mainImg.src = url;
      mainImg.onload = () => { mainImg.style.opacity = '1'; };
    }
    document.querySelectorAll('[data-thumbnail]').forEach(b => {
      b.classList.remove('border-amber-500');
      b.classList.add('border-gray-200');
    });
    btn?.classList.remove('border-gray-200');
    btn?.classList.add('border-amber-500');
  };

  // ---- Form Focus Enhancement ----
  document.querySelectorAll('input, textarea, select').forEach(el => {
    el.addEventListener('focus', () => {
      el.closest('.form-group')?.querySelector('label')?.classList.add('text-amber-700');
    });
    el.addEventListener('blur', () => {
      el.closest('.form-group')?.querySelector('label')?.classList.remove('text-amber-700');
    });
  });

  // ---- Mobile Product Filter Toggle ----
  const mobileFilterBtn = document.getElementById('mobile-filter-btn');
  const filterSidebar = document.getElementById('filter-sidebar');
  const filterBtnText = document.getElementById('filter-btn-text');

  mobileFilterBtn?.addEventListener('click', () => {
    const isHidden = filterSidebar?.classList.contains('hidden');
    filterSidebar?.classList.toggle('hidden', !isHidden);
    filterSidebar?.classList.toggle('block', isHidden);
    if (filterBtnText) {
      filterBtnText.textContent = isHidden ? 'Hide Filters' : 'Show Filters';
    }
  });

  // ---- WhatsApp Floating Button Pulse ----
  const waBtn = document.querySelector('a[aria-label="Chat on WhatsApp"]');
  if (waBtn) {
    // Subtle pulse animation every 8 seconds
    setInterval(() => {
      waBtn.classList.add('scale-125');
      setTimeout(() => waBtn.classList.remove('scale-125'), 400);
    }, 8000);
  }

  // ---- Masonry Layout (CSS Columns) – already handled by Tailwind columns-* ----

  console.log('%c TriDAV Impex ', 'background: #a87840; color: white; font-size: 14px; padding: 5px 10px; border-radius: 4px;', '| Premium Indian Home Textiles');

});
