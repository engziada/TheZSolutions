document.addEventListener('DOMContentLoaded', function() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    // Add loading class initially
    heroSection.classList.add('loading');

    // Create new image to preload
    const img = new Image();
    img.src = heroSection.style.getPropertyValue('--hero-bg-url') || '/static/img/hero-bg.webp';

    // When high quality image is loaded
    img.onload = function() {
        // Remove loading class and add loaded class
        heroSection.classList.remove('loading');
        heroSection.classList.add('loaded');
    };

    // If image fails to load, keep the placeholder
    img.onerror = function() {
        console.error('Failed to load hero background image');
        heroSection.classList.remove('loading');
    };
});
