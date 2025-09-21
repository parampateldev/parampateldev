# Param Patel - Developer Portfolio

A modern, responsive portfolio website showcasing full-stack development skills and projects.

## 🌟 Features

- **Responsive Design**: Optimized for all devices and screen sizes
- **Dark/Light Theme**: Toggle between themes with persistent preference
- **Smooth Animations**: Engaging animations and transitions
- **Interactive Elements**: Hover effects, smooth scrolling, and dynamic content
- **Modern UI/UX**: Clean, professional design with excellent user experience
- **Fast Loading**: Optimized performance with lazy loading and efficient code
- **SEO Optimized**: Proper meta tags and semantic HTML structure
- **Accessible**: WCAG compliant with proper ARIA labels and keyboard navigation

## 🚀 Live Demo

Visit the live website at [parampatel.dev](https://parampatel.dev)

## 🛠️ Technologies Used

### Frontend
- **HTML5**: Semantic markup and modern structure
- **CSS3**: Custom properties, Grid, Flexbox, and animations
- **JavaScript (ES6+)**: Modern JavaScript with classes and modules
- **Font Awesome**: Icons for better visual appeal
- **Google Fonts**: Inter font family for typography

### Features
- CSS Custom Properties for theming
- Intersection Observer API for animations
- Local Storage for theme persistence
- Responsive images and lazy loading
- Smooth scrolling and navigation
- Form validation and submission handling

## 📁 Project Structure

```
parampatel-dev/
├── index.html          # Main HTML file
├── styles.css          # CSS styles with theme support
├── script.js           # JavaScript functionality
├── package.json        # Project configuration
├── README.md           # Project documentation
└── images/             # Image assets (create as needed)
    ├── profile.jpg     # Profile photo
    ├── projects/       # Project screenshots
    └── icons/          # Custom icons
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/parampatel/parampatel-dev.git
   cd parampatel-dev
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**

   ```bash
   npm run dev
   ```
   This will start a local server at `http://localhost:3000`

### Alternative Setup

If you prefer not to use npm, you can simply:
1. Download the files
2. Open `index.html` in your web browser
3. Or serve with any static file server

## 📝 Customization

### Personal Information
Update the following sections in `index.html`:
- Hero section with your name and title
- About section with your description
- Skills section with your technologies
- Projects section with your work
- Contact information

### Styling
Modify `styles.css` to customize:
- Color scheme in CSS custom properties
- Typography and spacing
- Layout and animations
- Theme colors

### Functionality
Update `script.js` to modify:
- Animation timing and effects
- Form submission handling
- Theme behavior
- Interactive features

## 🎨 Theme Customization

The website supports both light and dark themes. To customize colors:

1. **Light Theme Colors** (in `:root` selector):
   ```css
   --bg-primary: #ffffff;
   --text-primary: #1e293b;
   --accent-primary: #4f46e5;
   ```

2. **Dark Theme Colors** (in `[data-theme="dark"]` selector):
   ```css
   --bg-primary: #0f172a;
   --text-primary: #f1f5f9;
   --accent-primary: #6366f1;
   ```

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px to 1199px
- **Mobile**: Below 768px
- **Small Mobile**: Below 480px

## 🚀 Deployment

### Netlify (Recommended)
1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build` (or leave empty)
3. Set publish directory: `.` (root)
4. Deploy!

### Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project directory
3. Follow the prompts

### GitHub Pages
1. Push code to GitHub repository
2. Go to repository Settings > Pages
3. Select source branch (usually `main`)
4. Your site will be available at `username.github.io/repository-name`

### Traditional Hosting
Upload all files to your web server's public directory.

## 🔧 Available Scripts

- `npm start` - Start local server
- `npm run dev` - Start development server with live reload
- `npm run build` - Build for production (placeholder)
- `npm run lint` - Lint HTML, CSS, and JavaScript files
- `npm run validate` - Validate HTML structure

## 📊 Performance

The website is optimized for performance with:
- Minified and compressed assets
- Lazy loading for images
- Efficient CSS and JavaScript
- Optimized animations using CSS transforms
- Minimal external dependencies

## 🔍 SEO Features

- Semantic HTML structure
- Meta tags for social sharing
- Open Graph tags
- Structured data markup
- Fast loading times
- Mobile-friendly design

## ♿ Accessibility

- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- High contrast ratios
- Focus indicators
- Alt text for images

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Param Patel**
- Email: hello@parampatel.dev
- LinkedIn: [linkedin.com/in/parampatel](https://linkedin.com/in/parampatel)
- GitHub: [github.com/parampatel](https://github.com/parampatel)
- Website: [parampatel.dev](https://parampatel.dev)

## 🙏 Acknowledgments

- [Font Awesome](https://fontawesome.com/) for icons
- [Google Fonts](https://fonts.google.com/) for typography
- [Inter Font](https://rsms.me/inter/) for the beautiful typeface
- Modern CSS techniques and JavaScript APIs
- The open-source community for inspiration

---

⭐ **Star this repository if you found it helpful!**
