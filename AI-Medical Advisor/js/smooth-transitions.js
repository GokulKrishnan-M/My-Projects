/**
 * Smooth Transitions & Scroll Animations
 * Keeps the existing UI and only reveals elements that opt into motion classes.
 */

document.documentElement.classList.add('js-enabled');

document.addEventListener('DOMContentLoaded', function() {
    const animatedSelector = [
        '.text-animate',
        '.section-animate',
        '.animate-on-scroll',
        '.animate-float',
        '.card-animate',
        '.feature-card'
    ].join(', ');

    const animatedElements = document.querySelectorAll(animatedSelector);

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (!entry.isIntersecting) {
                    return;
                }

                const delay = (index % 4) * 0.12;
                entry.target.style.animationDelay = `${delay}s`;
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -80px 0px'
        });

        animatedElements.forEach((element) => observer.observe(element));
    } else {
        animatedElements.forEach((element) => element.classList.add('animated'));
    }

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') {
                return;
            }

            const target = document.querySelector(href);
            if (!target) {
                return;
            }

            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });

    const heroSections = document.querySelectorAll('[class*="hero"]');
    window.addEventListener('scroll', () => {
        const scrollPosition = window.pageYOffset;
        heroSections.forEach((hero) => {
            hero.style.backgroundPosition = `center ${scrollPosition * 0.5}px`;
        });
    });

    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 50);
});
