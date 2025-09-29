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
        { id: 'worldMap', url: '/world-map/preview' },
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
  background: #1e1e1e;
  border-bottom: 1px solid #fada95;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  padding: 12px 0;
  z-index: 50;
  position: relative;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
  flex-wrap: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.desktop-nav::-webkit-scrollbar {
  display: none;
}

.desktop-nav a {
  color: #ffffff;
  text-decoration: none;
  font-size: clamp(13px, 1.2vw, 16px);
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  min-width: 0;
  flex-shrink: 1;
}

.desktop-nav a:hover {
  color: #fada95;
  background: rgba(250, 218, 149, 0.1);
}

.desktop-nav li {
  margin-right: 6px;
  flex-shrink: 1;
  min-width: 0;
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
  background: #1e1e1e;
  border-radius: 8px;
  padding: 0;
  width: 85%;
  max-width: 320px;
  max-height: 60vh;
  overflow-y: auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
  border: 1px solid #fada95;
}

.mobile-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(250, 218, 149, 0.3);
  background: rgba(0, 0, 0, 0.2);
}

.mobile-menu-header h3 {
  color: #fada95;
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: 1px solid rgba(250, 218, 149, 0.3);
  color: #fada95;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(250, 218, 149, 0.1);
  border-color: #fada95;
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
  color: #ffffff;
  text-decoration: none;
  padding: 0.875rem 1.25rem;
  font-size: clamp(0.85rem, 2vw, 0.95rem);
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(250, 218, 149, 0.1);
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  line-height: 1.2;
}

.mobile-nav-list a:hover {
  background: rgba(250, 218, 149, 0.1);
  color: #fada95;
}

.mobile-menu-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(250, 218, 149, 0.3);
  background: rgba(0, 0, 0, 0.2);
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
