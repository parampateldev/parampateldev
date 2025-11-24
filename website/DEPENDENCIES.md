# Portfolio Website Dependencies

## External CDN Dependencies

### 1. Google Fonts - Inter
- **URL**: `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap`
- **Purpose**: Primary font family for the website
- **Status**: ✅ Required
- **Fallback**: System fonts (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto`)

### 2. Font Awesome 6.4.0
- **URL**: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`
- **Purpose**: Icon library for navigation, skills, projects, and contact sections
- **Status**: ✅ Required
- **Usage**: Icons throughout the site (moon/sun, chevron, external links, GitHub, LinkedIn, etc.)

### 3. Unsplash Images
- **URLs**: External Unsplash image URLs for project cards
- **Purpose**: Project card background images
- **Status**: ⚠️ External dependency (may fail if Unsplash is down)
- **Recommendation**: Consider hosting images locally for better reliability

## Local File Dependencies

### 1. styles.css
- **Path**: `/website/styles.css`
- **Purpose**: All styling, theme variables, responsive design
- **Status**: ✅ Required
- **Features**: 
  - shadcn/ui-inspired design system
  - Light/dark theme support
  - CSS custom properties (HSL color system)
  - Responsive breakpoints

### 2. script.js
- **Path**: `/website/script.js`
- **Purpose**: Interactive functionality
- **Status**: ✅ Required
- **Features**:
  - Theme management (localStorage)
  - Navigation (smooth scroll, active links)
  - Animations (IntersectionObserver)
  - Contact form handling
  - Mobile menu toggle

## Browser APIs Used (No External Libraries)

- **localStorage**: Theme persistence
- **IntersectionObserver**: Scroll animations
- **Canvas API**: Particle background (optional)
- **Fetch API**: Not currently used (form submission is simulated)

## Package.json Dependencies

All dependencies are **devDependencies** (development tools only):

- `htmlhint`: HTML linting
- `stylelint`: CSS linting
- `eslint`: JavaScript linting
- `html-validate`: HTML validation
- `http-server`: Local development server
- `live-server`: Live reload development server
- `imagemin`: Image optimization

**No runtime dependencies required** - the site is fully static.

## Issues Found

### 1. JavaScript Class Mismatches
- ❌ `TypingAnimation` looks for `.hero-title` but HTML uses `.hero-name`
- ⚠️ `CartManager` and `MenuTabManager` initialized but not needed for portfolio (used in menu.html/order.html)
- ⚠️ `ParticleBackground` creates canvas - may not be needed for minimalist design

### 2. Missing Elements
- `CartManager` expects `#cart-items`, `#cart-summary`, `#checkout-btn` (not in index.html)
- `MenuTabManager` expects `.tab-btn`, `.menu-section` (not in index.html)

## Recommendations

1. **Fix JavaScript**: Update `TypingAnimation` to use `.hero-name` or remove if not needed
2. **Conditional Initialization**: Only initialize `CartManager` and `MenuTabManager` on pages that need them
3. **Image Hosting**: Consider hosting project images locally instead of using Unsplash
4. **Remove Unused Code**: Remove or conditionally load `ParticleBackground` if not desired

## Network Requirements

- Internet connection required for:
  - Google Fonts (can be self-hosted)
  - Font Awesome (can be self-hosted)
  - Unsplash images (should be self-hosted)

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires ES6+ JavaScript support
- CSS Grid and Flexbox support
- CSS Custom Properties (CSS Variables)

