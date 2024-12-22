document.addEventListener('DOMContentLoaded', function() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    // Find existing particles container or create a new one
    let particlesContainer = heroSection.querySelector('.binary-particles');
    if (!particlesContainer) {
        particlesContainer = document.createElement('div');
        particlesContainer.className = 'binary-particles';
        heroSection.insertBefore(particlesContainer, heroSection.firstChild);
    }

    // Function to create a single particle
    function createParticle() {
        const particle = document.createElement('span');
        particle.className = 'particle';
        
        // Randomly choose between 0 and 1, with some variation in size
        const isLarge = Math.random() < 0.2;  // 20% chance of larger particle
        particle.style.fontSize = isLarge ? '20px' : '14px';  // Slightly smaller sizes
        particle.textContent = Math.random() < 0.5 ? '0' : '1';
        
        // Random position
        const startX = Math.random() * 100;
        particle.style.left = `${startX}%`;
        
        // Slower fall speed
        const duration = 8 + Math.random() * 7;  // Between 8 and 15 seconds
        particle.style.setProperty('--fall-duration', `${duration}s`);
        
        // Apply random starting position
        particle.style.transform = `translateY(-10vh)`;
        
        particlesContainer.appendChild(particle);
        
        // Force a reflow to ensure animation starts properly
        particle.offsetHeight;
        
        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode === particlesContainer) {
                particlesContainer.removeChild(particle);
            }
        }, duration * 1000);
    }

    // Create particles periodically
    function startParticles() {
        // Create particles less frequently
        const particleInterval = setInterval(createParticle, 500);  // Create a new particle every 500ms
        
        // Initial particles
        for(let i = 0; i < 10; i++) {  // Start with fewer particles
            setTimeout(createParticle, Math.random() * 2000);
        }

        // Store interval ID on the container
        particlesContainer.dataset.intervalId = particleInterval;
    }

    // Clean up any existing animation before starting new one
    const existingInterval = particlesContainer.dataset.intervalId;
    if (existingInterval) {
        clearInterval(existingInterval);
    }

    // Start the animation
    startParticles();

    // Log to confirm script is running
    console.log('Particles animation initialized - Slow falling effect');
});
