document.addEventListener('DOMContentLoaded', function() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('.marketing-content > section').forEach(section => {
        section.classList.add('animate-on-scroll');
        observer.observe(section);
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            hero.style.backgroundPosition = `center ${rate}px`;
        });
    }

    // Add hover effects for interactive elements
    const addHoverEffect = (elements, className) => {
        elements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.classList.add(className);
            });
            element.addEventListener('mouseleave', () => {
                element.classList.remove(className);
            });
        });
    };

    // Add hover effects to cards and buttons
    addHoverEffect(document.querySelectorAll('.feature-item'), 'hover');
    addHoverEffect(document.querySelectorAll('.audience-group'), 'hover');
    addHoverEffect(document.querySelectorAll('.btn'), 'hover');
});
