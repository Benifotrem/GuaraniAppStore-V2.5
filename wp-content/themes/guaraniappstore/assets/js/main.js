/**
 * GuaraniAppStore Theme - Main JavaScript
 *
 * @package GuaraniAppStore
 * @version 2.5
 */

(function() {
    'use strict';

    // DOM Ready
    document.addEventListener('DOMContentLoaded', function() {

        // Mobile Menu Toggle
        initMobileMenu();

        // Smooth Scroll
        initSmoothScroll();

        // Header Scroll Effect
        initHeaderScroll();

        // Animate on Scroll
        initScrollAnimations();

    });

    /**
     * Initialize Mobile Menu
     */
    function initMobileMenu() {
        const toggle = document.getElementById('mobile-menu-toggle');
        const nav = document.getElementById('main-nav');

        if (toggle && nav) {
            toggle.addEventListener('click', function() {
                nav.classList.toggle('active');

                // Change icon
                if (nav.classList.contains('active')) {
                    toggle.textContent = '✕';
                } else {
                    toggle.textContent = '☰';
                }
            });

            // Close menu when clicking on a link
            const navLinks = nav.querySelectorAll('a');
            navLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    if (window.innerWidth <= 768) {
                        nav.classList.remove('active');
                        toggle.textContent = '☰';
                    }
                });
            });

            // Close menu when clicking outside
            document.addEventListener('click', function(event) {
                if (!nav.contains(event.target) && !toggle.contains(event.target)) {
                    if (nav.classList.contains('active')) {
                        nav.classList.remove('active');
                        toggle.textContent = '☰';
                    }
                }
            });
        }
    }

    /**
     * Initialize Smooth Scroll
     */
    function initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');

        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');

                // Check if it's a valid anchor
                if (href === '#' || href === '#trial' || href === '#contact') {
                    return; // Let default behavior for these
                }

                const target = document.querySelector(href);

                if (target) {
                    e.preventDefault();

                    const headerHeight = document.querySelector('.site-header')?.offsetHeight || 80;
                    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Initialize Header Scroll Effect
     */
    function initHeaderScroll() {
        const header = document.querySelector('.site-header');

        if (header) {
            let lastScroll = 0;

            window.addEventListener('scroll', function() {
                const currentScroll = window.pageYOffset;

                // Add shadow when scrolled
                if (currentScroll > 50) {
                    header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
                } else {
                    header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
                }

                lastScroll = currentScroll;
            });
        }
    }

    /**
     * Initialize Scroll Animations
     */
    function initScrollAnimations() {
        const animatedElements = document.querySelectorAll('.service-card, .team-card, .feature-card');

        if (animatedElements.length === 0) return;

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '0';
                    entry.target.style.transform = 'translateY(30px)';

                    // Trigger animation
                    setTimeout(function() {
                        entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, 100);

                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(function(element) {
            observer.observe(element);
        });
    }

    /**
     * Video Autoplay on Mobile
     */
    const videos = document.querySelectorAll('video[autoplay]');
    videos.forEach(function(video) {
        // Ensure video plays on mobile
        video.setAttribute('playsinline', '');
        video.setAttribute('muted', '');

        // Try to play
        const playPromise = video.play();

        if (playPromise !== undefined) {
            playPromise.catch(function(error) {
                console.log('Video autoplay prevented:', error);
            });
        }
    });

})();
