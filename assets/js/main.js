// Contact details used by the Email buttons and social tiles.
const CONTACT = {
  email: 's923446@gmail.com',
};

document.addEventListener('DOMContentLoaded', () => {
  const ready = () => document.body.classList.add('is-ready');
  requestAnimationFrame(ready);
  setTimeout(ready, 300); // rAF is paused in background tabs

  // Project tiles: static image by default, play the loop while hovered.
  const canHover = window.matchMedia('(hover: hover)').matches;
  document.querySelectorAll('.project').forEach((tile) => {
    const video = tile.querySelector('video');
    if (!video || !canHover) return;
    tile.addEventListener('mouseenter', () => {
      if (!video.src) video.src = video.dataset.src;
      video.play().then(() => tile.classList.add('is-playing')).catch(() => {});
    });
    tile.addEventListener('mouseleave', () => {
      tile.classList.remove('is-playing');
      setTimeout(() => {
        if (!tile.classList.contains('is-playing')) {
          video.pause();
          video.currentTime = 0;
        }
      }, 500);
    });
  });

  // Email buttons copy the address and show a toast.
  const toast = document.querySelector('.toast');
  document.querySelectorAll('[data-copy-email]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(CONTACT.email);
        showToast(`已複製 ${CONTACT.email}`);
      } catch {
        window.location.href = `mailto:${CONTACT.email}`;
      }
    });
  });
  document.querySelectorAll('[data-mailto]').forEach((a) => {
    a.href = `mailto:${CONTACT.email}`;
  });

  function showToast(text) {
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add('is-on');
    clearTimeout(showToast.t);
    showToast.t = setTimeout(() => toast.classList.remove('is-on'), 2200);
  }

  // Detail pages: fade blocks in as they scroll into view.
  const blocks = document.querySelectorAll('.scroll-in');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    blocks.forEach((b) => io.observe(b));
  } else {
    blocks.forEach((b) => b.classList.add('is-in'));
  }
});
