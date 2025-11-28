// Portfolio Website JavaScript

// DOM Elements
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');
const navLinks = document.querySelectorAll('.nav-link');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const contactForm = document.getElementById('contact-form');

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.init();
    }

    init() {
        this.setTheme(this.currentTheme);
        this.bindEvents();
    }

    setTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update theme icon
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
        } else {
            themeIcon.className = 'fas fa-moon';
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    bindEvents() {
        themeToggle.addEventListener('click', () => this.toggleTheme());
    }
}

// Navigation Management
class NavigationManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.setActiveNavLink();
    }

    bindEvents() {
        // Mobile menu toggle
        navToggle.addEventListener('click', () => this.toggleMobileMenu());
        
        // Close mobile menu when clicking on links
        navLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMobileMenu());
        });

        // Scroll events
        window.addEventListener('scroll', () => {
            this.handleScroll();
            this.setActiveNavLink();
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    const navbarHeight = 64; // 4rem = 64px
                    const extraPadding = 20; // Extra space for better visibility
                    const offsetTop = target.offsetTop - navbarHeight - extraPadding;
                    window.scrollTo({
                        top: Math.max(0, offsetTop),
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    toggleMobileMenu() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    }

    closeMobileMenu() {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
    }

    handleScroll() {
        // Always show navbar with full opacity when scrolled
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    setActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
}

// Animation Manager
class AnimationManager {
    constructor() {
        this.init();
    }

    init() {
        this.observeElements();
        this.animateOnScroll();
    }

    observeElements() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observe elements that should animate
        const animatedElements = document.querySelectorAll(
            '.section-title, .section-subtitle, .about-description, .stat, .skill-category, .project-card, .contact-item'
        );

        animatedElements.forEach(el => {
            el.classList.add('fade-in');
            observer.observe(el);
        });
    }

    animateOnScroll() {
        // Stagger animation for stats
        const stats = document.querySelectorAll('.stat');
        stats.forEach((stat, index) => {
            stat.style.animationDelay = `${index * 0.1}s`;
        });

        // Stagger animation for skill items
        const skillItems = document.querySelectorAll('.skill-item');
        skillItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.05}s`;
        });
    }
}

// Contact Form Manager
class ContactFormManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Show loading state
        submitBtn.innerHTML = '<div class="loading"></div> Sending...';
        submitBtn.disabled = true;

        try {
            // Simulate form submission (replace with actual API call)
            await this.simulateFormSubmission();
            
            // Show success message
            this.showMessage('Message sent successfully! I\'ll get back to you soon.', 'success');
            contactForm.reset();
            
        } catch (error) {
            // Show error message
            this.showMessage('Sorry, there was an error sending your message. Please try again.', 'error');
        } finally {
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    async simulateFormSubmission() {
        // Simulate network delay
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simulate 90% success rate
                if (Math.random() > 0.1) {
                    resolve();
                } else {
                    reject(new Error('Simulated error'));
                }
            }, 2000);
        });
    }

    showMessage(message, type) {
        // Create message element
        const messageEl = document.createElement('div');
        messageEl.className = `message message-${type}`;
        messageEl.textContent = message;
        
        // Style the message
        Object.assign(messageEl.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            borderRadius: '0.5rem',
            color: 'white',
            backgroundColor: type === 'success' ? '#10b981' : '#ef4444',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            zIndex: '9999',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });

        document.body.appendChild(messageEl);

        // Animate in
        setTimeout(() => {
            messageEl.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 5 seconds
        setTimeout(() => {
            messageEl.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(messageEl);
            }, 300);
        }, 5000);
    }
}

// Typing Animation with Cursor
class TypingAnimation {
    constructor() {
        this.init();
    }

    init() {
        // Intro screen typing
        this.animateIntro();
        
        // Hero section typing (after main content is visible)
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                        if (mainContent.classList.contains('visible')) {
                            setTimeout(() => this.animateHero(), 500);
                            observer.disconnect();
                        }
                    }
                });
            });
            observer.observe(mainContent, { attributes: true });
        }
    }

    animateIntro() {
        const introGreeting = document.querySelector('.intro-greeting');
        const introName = document.querySelector('.intro-name-typing .typing-text');
        
        if (introName) {
            const nameText = introName.textContent;
            introName.textContent = '';
            this.typeText(introName, nameText, 100, 800);
        }
    }

    animateHero() {
        const heroName = document.querySelector('.hero-name-typing .typing-text');
        const heroRole = document.querySelector('.hero-role-typing .typing-text-role');
        
        if (heroName) {
            const nameText = heroName.textContent;
            heroName.textContent = '';
            this.typeText(heroName, nameText, 100, 500);
        }
        
        if (heroRole) {
            const roleText = heroRole.textContent;
            heroRole.textContent = '';
            this.typeText(heroRole, roleText, 100, 2000);
        }
    }

    typeText(element, text, speed, delay = 0) {
        setTimeout(() => {
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            };
            typeWriter();
        }, delay);
    }
}

// Particle Background Effect
class ParticleBackground {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.particles = [];
        this.init();
    }

    init() {
        this.createCanvas();
        this.createParticles();
        this.animate();
        this.bindEvents();
    }

    createCanvas() {
        // Use existing canvas from HTML if available, otherwise create one
        this.canvas = document.getElementById('particle-canvas');
        if (!this.canvas) {
            this.canvas = document.createElement('canvas');
            this.canvas.id = 'particle-canvas';
            this.canvas.className = 'particle-canvas';
            this.canvas.style.position = 'fixed';
            this.canvas.style.top = '0';
            this.canvas.style.left = '0';
            this.canvas.style.width = '100%';
            this.canvas.style.height = '100%';
            this.canvas.style.pointerEvents = 'none';
            this.canvas.style.zIndex = '0';
            this.canvas.style.opacity = '0.3';
            document.body.appendChild(this.canvas);
        }
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = Math.min(50, Math.floor(window.innerWidth / 20));
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            const blueColor = getComputedStyle(document.documentElement).getPropertyValue('--umich-blue').trim();
            this.ctx.fillStyle = `hsl(${blueColor})`;
            this.ctx.fill();
            
            // Draw connections
            this.particles.forEach(otherParticle => {
                if (otherParticle === particle) return;
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(otherParticle.x, otherParticle.y);
                    this.ctx.strokeStyle = `hsl(${blueColor}, ${1 - distance / 150 * 100}%)`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(() => this.animate());
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.particles = [];
            this.createParticles();
        });
    }
}

// Performance Optimization
class PerformanceOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.lazyLoadImages();
        this.optimizeScrollEvents();
    }

    lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    optimizeScrollEvents() {
        let ticking = false;
        
        const optimizedScrollHandler = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    // Scroll-dependent code here
                    ticking = false;
                });
                ticking = true;
            }
        };

        window.addEventListener('scroll', optimizedScrollHandler, { passive: true });
    }
}

// Cart Management
class CartManager {
    constructor() {
        this.cart = JSON.parse(localStorage.getItem('cart')) || [];
        this.init();
    }

    init() {
        // Only initialize if cart elements exist
        if (!document.getElementById('cart-items')) {
            return;
        }
        this.bindEvents();
        this.updateCartDisplay();
    }

    bindEvents() {
        // Add to cart buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-cart-btn')) {
                const item = e.target.closest('.quick-item');
                const name = item.querySelector('h3').textContent;
                const price = parseFloat(item.dataset.price);
                this.addToCart(name, price);
            }
        });

        // Quantity controls
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quantity-btn')) {
                const item = e.target.closest('.cart-item');
                const name = item.dataset.item;
                const isIncrease = e.target.classList.contains('increase');
                this.updateQuantity(name, isIncrease ? 1 : -1);
            }
        });

        // Remove item
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-item')) {
                const item = e.target.closest('.cart-item');
                const name = item.dataset.item;
                this.removeFromCart(name);
            }
        });
    }

    addToCart(name, price) {
        const existingItem = this.cart.find(item => item.name === name);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({
                name: name,
                price: price,
                quantity: 1
            });
        }
        
        this.saveCart();
        this.updateCartDisplay();
        this.showNotification(`${name} added to cart!`);
    }

    updateQuantity(name, change) {
        const item = this.cart.find(item => item.name === name);
        
        if (item) {
            item.quantity += change;
            
            if (item.quantity <= 0) {
                this.removeFromCart(name);
            } else {
                this.saveCart();
                this.updateCartDisplay();
            }
        }
    }

    removeFromCart(name) {
        this.cart = this.cart.filter(item => item.name !== name);
        this.saveCart();
        this.updateCartDisplay();
        this.showNotification(`${name} removed from cart!`);
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }

    updateCartDisplay() {
        const cartItems = document.getElementById('cart-items');
        const cartSummary = document.getElementById('cart-summary');
        const checkoutBtn = document.getElementById('checkout-btn');
        
        if (!cartItems) return;

        if (this.cart.length === 0) {
            cartItems.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-shopping-cart"></i>
                    <p>Your cart is empty</p>
                    <p>Add items from our menu to get started</p>
                </div>
            `;
            cartSummary.style.display = 'none';
            checkoutBtn.disabled = true;
        } else {
            cartItems.innerHTML = this.cart.map(item => `
                <div class="cart-item" data-item="${item.name}">
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <p>$${item.price.toFixed(2)} each</p>
                    </div>
                    <div class="cart-item-controls">
                        <button class="quantity-btn decrease">-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="quantity-btn increase">+</button>
                        <button class="remove-item" style="margin-left: 1rem; color: var(--accent-red); background: none; border: none; cursor: pointer;">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
                </div>
            `).join('');

            this.updateCartSummary();
            cartSummary.style.display = 'block';
            checkoutBtn.disabled = false;
        }
    }

    updateCartSummary() {
        const subtotal = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const serviceCharge = subtotal * 0.1;
        const deliveryFee = subtotal > 50 ? 0 : 10;
        const total = subtotal + serviceCharge + deliveryFee;

        document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
        document.getElementById('service-charge').textContent = `$${serviceCharge.toFixed(2)}`;
        document.getElementById('delivery-fee').textContent = `$${deliveryFee.toFixed(2)}`;
        document.getElementById('total').textContent = `$${total.toFixed(2)}`;
    }

    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-primary);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: var(--shadow-lg);
            z-index: 9999;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Menu Tab Management
class MenuTabManager {
    constructor() {
        this.init();
    }

    init() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        const menuSections = document.querySelectorAll('.menu-section');

        // Only initialize if menu elements exist
        if (tabBtns.length === 0 || menuSections.length === 0) {
            return;
        }

        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                
                // Update active tab
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Show/hide sections
                menuSections.forEach(section => {
                    if (section.id === category) {
                        section.style.display = 'block';
                        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    } else {
                        section.style.display = 'none';
                    }
                });
            });
        });

        // Show first section by default
        if (menuSections.length > 0) {
            menuSections[0].style.display = 'block';
        }
    }
}

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize core managers (always needed)
    new ThemeManager();
    new NavigationManager();
    new AnimationManager();
    new ContactFormManager();
    new TypingAnimation();
    new PerformanceOptimizer();

    // Initialize optional features conditionally
    // Particle background (can be disabled for minimalist design)
    if (document.querySelector('.hero') || document.getElementById('particle-canvas')) {
        new ParticleBackground();
    }

    // Cart and menu managers (only for menu/order pages)
    if (document.getElementById('cart-items')) {
        new CartManager();
    }
    if (document.querySelector('.tab-btn')) {
        new MenuTabManager();
    }
    
    // Initialize new enhancements
    new ScrollProgress();
    new BackToTop();
    new SectionNavDots();
    new ScrollAnimations();
    new ParallaxScroll();
    new MicroInteractions();

    // Add some interactive effects
    addSkillHoverEffects();
    addProjectHoverEffects();
});

// Additional Interactive Effects
function addSkillHoverEffects() {
    const skillItems = document.querySelectorAll('.skill-item');
    
    skillItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'translateY(-5px) scale(1.05)';
            item.style.boxShadow = '0 10px 25px rgba(79, 70, 229, 0.2)';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateY(0) scale(1)';
            item.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        });
    });
}

function addProjectHoverEffects() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Intro Screen Animation
class IntroAnimation {
    constructor() {
        this.introScreen = document.getElementById('intro-screen');
        this.mainContent = document.getElementById('main-content');
        this.init();
    }

    init() {
        if (!this.introScreen || !this.mainContent) return;

        // Ensure navbar is always visible from the start
        const navbar = document.getElementById('navbar');
        if (navbar) {
            navbar.style.visibility = 'visible';
            navbar.style.opacity = '1';
            navbar.style.position = 'fixed';
            navbar.style.zIndex = '10000';
        }

        // Ensure page is at top
        window.scrollTo(0, 0);

        // Wait for intro typing animation to complete (greeting at 0.3s, name typing ~2s)
        setTimeout(() => {
            // Hide intro screen - fade out completely first
            this.introScreen.classList.add('hidden');
            
            // Wait for intro to fully fade out (1.2s transition) before showing main content
            setTimeout(() => {
                // Then show main content
                this.mainContent.classList.add('visible');
                // Ensure page stays at top when content appears
                window.scrollTo(0, 0);
            }, 1200); // Wait for intro fade-out to complete
        }, 3000); // Total intro duration (typing animation complete)
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const introScreen = document.getElementById('intro-screen');
    const mainContent = document.getElementById('main-content');
    
    // If no intro screen, show main content immediately
    if (!introScreen || introScreen.classList.contains('hidden')) {
        if (mainContent) {
            mainContent.classList.add('visible');
        }
    } else {
        new IntroAnimation();
    }
    
    // Fallback: ensure main content is visible after a delay
    setTimeout(() => {
        if (mainContent && !mainContent.classList.contains('visible')) {
            mainContent.classList.add('visible');
        }
    }, 5000);
});

// ============================================
// ENHANCEMENTS - New Features JavaScript
// ============================================

// Scroll Progress Indicator
class ScrollProgress {
    constructor() {
        this.progressBar = document.getElementById('scroll-progress');
        this.init();
    }

    init() {
        if (!this.progressBar) return;
        
        window.addEventListener('scroll', () => {
            const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (window.scrollY / windowHeight) * 100;
            this.progressBar.style.width = scrolled + '%';
        });
    }
}

// Back to Top Button
class BackToTop {
    constructor() {
        this.button = document.getElementById('back-to-top');
        this.init();
    }

    init() {
        if (!this.button) return;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                this.button.classList.add('visible');
            } else {
                this.button.classList.remove('visible');
            }
        });

        this.button.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Section Navigation Dots
class SectionNavDots {
    constructor() {
        this.dots = document.querySelectorAll('.nav-dot');
        this.sections = document.querySelectorAll('section[id]');
        this.init();
    }

    init() {
        if (!this.dots.length) return;

        window.addEventListener('scroll', () => {
            this.updateActiveDot();
        });

        this.dots.forEach(dot => {
            dot.addEventListener('click', (e) => {
                e.preventDefault();
                const sectionId = dot.getAttribute('data-section');
                const section = document.getElementById(sectionId);
                if (section) {
                    const navbarHeight = 64;
                    const offsetTop = section.offsetTop - navbarHeight;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    updateActiveDot() {
        const scrollPos = window.scrollY + 200;
        
        this.sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                this.dots.forEach(dot => {
                    dot.classList.remove('active');
                    if (dot.getAttribute('data-section') === sectionId) {
                        dot.classList.add('active');
                    }
                });
            }
        });
    }
}

// Scroll Animations (AOS-like)
class ScrollAnimations {
    constructor() {
        this.elements = document.querySelectorAll('[data-aos]');
        this.init();
    }

    init() {
        if (!this.elements.length) return;

        // Add js-enabled class to html
        document.documentElement.classList.add('js-enabled');

        // Make all elements visible immediately, then animate on scroll
        this.elements.forEach(el => {
            el.classList.add('aos-animate');
        });

        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            return;
        }

        // Reset for animation
        this.elements.forEach(el => {
            el.classList.remove('aos-animate');
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const delay = entry.target.getAttribute('data-aos-delay') || 0;
                    setTimeout(() => {
                        entry.target.classList.add('aos-animate');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        this.elements.forEach(el => {
            // Check if element is already in viewport
            const rect = el.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                // Already visible, animate immediately
                el.classList.add('aos-animate');
            } else {
                // Not visible, observe for scroll
                observer.observe(el);
            }
        });
    }
}

// Parallax Scrolling
class ParallaxScroll {
    constructor() {
        this.elements = document.querySelectorAll('.graph-background');
        this.init();
    }

    init() {
        if (!this.elements.length) return;
        
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) return;

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            this.elements.forEach(element => {
                const speed = 0.5;
                element.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });
    }
}

// Micro-interactions
class MicroInteractions {
    constructor() {
        this.init();
    }

    init() {
        const buttons = document.querySelectorAll('button, .btn-about-me, .project-link, .social-icon');
        buttons.forEach(button => {
            button.addEventListener('mousedown', () => {
                button.style.transform = 'scale(0.95)';
            });
            button.addEventListener('mouseup', () => {
                button.style.transform = '';
            });
            button.addEventListener('mouseleave', () => {
                button.style.transform = '';
            });
        });

        const icons = document.querySelectorAll('.social-icon i, .project-link i');
        icons.forEach(icon => {
            icon.parentElement.addEventListener('mouseenter', () => {
                icon.style.transform = 'scale(1.2) rotate(5deg)';
            });
            icon.parentElement.addEventListener('mouseleave', () => {
                icon.style.transform = '';
            });
        });
    }
}

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ThemeManager,
        NavigationManager,
        AnimationManager,
        ContactFormManager,
        TypingAnimation,
        ParticleBackground,
        PerformanceOptimizer,
        IntroAnimation,
        ScrollProgress,
        BackToTop,
        SectionNavDots,
        ScrollAnimations,
        ParallaxScroll,
        MicroInteractions
    };
}
