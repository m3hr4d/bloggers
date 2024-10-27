// Custom JavaScript for Hero Section Background Animation

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('heroCanvas');
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    // Initialize canvas size and particles
    function init() {
        resizeCanvas();
        createParticles();
        animate();
    }

    // Resize canvas to fill window
    function resizeCanvas() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    // Create particles for animation
    function createParticles() {
        particles = [];
        const numParticles = 100;
        for (let i = 0; i < numParticles; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 4 + 1,
                speedX: (Math.random() - 0.5) * 0.5,
                speedY: (Math.random() - 0.5) * 0.5,
                color: `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2})`
            });
        }
    }

    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            // Move particles
            p.x += p.speedX;
            p.y += p.speedY;

            // Wrap around edges
            if (p.x > width) p.x = 0;
            else if (p.x < 0) p.x = width;
            if (p.y > height) p.y = 0;
            else if (p.y < 0) p.y = height;

            // Draw particle
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();
        });
        requestAnimationFrame(animate);
    }

    // Listen for window resize
    window.addEventListener('resize', () => {
        resizeCanvas();
        createParticles();
    });

    // Start animation
    init();
});
