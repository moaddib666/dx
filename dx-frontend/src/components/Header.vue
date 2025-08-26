<template>
  <header class="header">
    <nav class="navbar container">
      <!-- Mobile hamburger menu button -->
      <button
        class="mobile-menu-toggle"
        @click="toggleMobileMenu"
        :class="{ active: isMobileMenuOpen }"
        aria-label="Toggle navigation menu"
      >
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>

      <!-- Desktop navigation -->
      <ul class="desktop-nav">
        <li v-for="link in links" :key="link.id">
          <a :href="link.url">{{ t(`navigation.${link.id}`) }}</a>
        </li>
      </ul>

      <LanguageSwitcher class="language-switcher desktop-only" />
    </nav>

    <!-- Mobile menu modal -->
    <div
      class="mobile-menu-overlay"
      :class="{ active: isMobileMenuOpen }"
      @click="closeMobileMenu"
    >
      <div class="mobile-menu" @click.stop>
        <div class="mobile-menu-header">
          <h3>Navigation</h3>
          <button class="close-btn" @click="closeMobileMenu" aria-label="Close menu">×</button>
        </div>
        <ul class="mobile-nav-list">
          <li v-for="link in links" :key="link.id">
            <a :href="link.url" @click="closeMobileMenu">{{ t(`navigation.${link.id}`) }}</a>
          </li>
        </ul>
        <div class="mobile-menu-footer">
          <LanguageSwitcher />
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import LanguageSwitcher from './LanguageSwitcher.vue';
import { useI18n } from 'vue-i18n';

export default {
  components: {
    LanguageSwitcher
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      isMobileMenuOpen: false,
      links: [
        { id: 'home', url: '/' },
        // { id: 'story', url: '/story' },
        // { id: 'characters', url: '/characters' },
        // { id: 'gameplay', url: '/gameplay' },
        // { id: 'community', url: '/community' },
        // { id: 'shop', url: '/shop' },
        // { id: 'support', url: '/support' },
        { id: 'whatIsIt', url: '/faq/what-is-it' },
        { id: 'newcomersGuide', url: '/faq/newcomers-guide' },
        { id: 'playerCheatSheet', url: '/faq/player-cheatsheet' },
        { id: 'faq', url: '/faq' },
        { id: 'artGallery', url: '/art-gallery/' }
      ]
    };
  },
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
      // Prevent body scroll when menu is open
      if (this.isMobileMenuOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
      document.body.style.overflow = '';
    }
  },
  beforeUnmount() {
    // Clean up body overflow style
    document.body.style.overflow = '';
  }
};
</script>

<style scoped>
.header {
  background-color: var(--dark-slate-gray);
  padding: 10px 0;
  z-index: 50;
  position: relative;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

/* Mobile hamburger menu button */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  z-index: 1001;
}

.hamburger-line {
  width: 25px;
  height: 3px;
  background-color: #FFFFFF;
  margin: 3px 0;
  transition: 0.3s;
  border-radius: 2px;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(1) {
  transform: rotate(-45deg) translate(-5px, 6px);
}

.mobile-menu-toggle.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(3) {
  transform: rotate(45deg) translate(-5px, -6px);
}

/* Desktop navigation */
.desktop-nav {
  display: flex;
  justify-content: flex-start;
  list-style: none;
  margin: 0;
  padding: 0;
  flex-grow: 1;
}

.desktop-nav a {
  color: #FFFFFF;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.desktop-nav a:hover {
  color: var(--cyber-yellow);
}

.desktop-nav li {
  margin-right: 20px;
}

.language-switcher {
  margin-right: 20px;
}

/* Mobile menu overlay */
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.mobile-menu-overlay.active {
  opacity: 1;
  visibility: visible;
}

.mobile-menu {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--dark-slate-gray, #2c3e50);
  border-radius: 8px;
  padding: 0;
  width: 85%;
  max-width: 320px;
  max-height: 60vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border: 2px solid #444;
}

.mobile-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #444;
  background-color: rgba(0, 0, 0, 0.2);
}

.mobile-menu-header h3 {
  color: #FFFFFF;
  margin: 0;
  font-size: 1rem;
}

.close-btn {
  background: none;
  border: none;
  color: #FFFFFF;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.mobile-nav-list {
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
}

.mobile-nav-list li {
  margin: 0;
}

.mobile-nav-list a {
  display: block;
  color: #FFFFFF;
  text-decoration: none;
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  transition: background-color 0.3s ease, color 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-nav-list a:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--cyber-yellow, #ffd700);
}

.mobile-menu-footer {
  padding: 0.75rem 1rem;
  border-top: 1px solid #444;
  background-color: rgba(0, 0, 0, 0.2);
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }

  .desktop-nav {
    display: none;
  }

  .desktop-only {
    display: none;
  }
}

@media (min-width: 769px) {
  .mobile-menu-toggle {
    display: none;
  }

  .mobile-menu-overlay {
    display: none;
  }
}

/* Container class for responsive layout */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }
}
</style>
