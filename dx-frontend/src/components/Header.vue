<template>
  <header class="header">
    <nav class="navbar">
      <div class="nav-container">
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
        <ul class="nav-menu desktop-nav">
          <li v-for="link in links" :key="link.id" class="nav-item" :class="{ active: isActiveLink(link.url) }">
            <a :href="link.url" class="nav-link">{{ link.label || t(`navigation.${link.id}`) }}</a>
          </li>
        </ul>

        <LanguageSwitcher class="language-switcher desktop-only" />
      </div>
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
          <li v-for="link in links" :key="link.id" class="nav-item" :class="{ active: isActiveLink(link.url) }">
            <a :href="link.url" class="nav-link" @click="closeMobileMenu">{{ link.label || t(`navigation.${link.id}`) }}</a>
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
import { useRoute } from 'vue-router';

export default {
  components: {
    LanguageSwitcher
  },
  setup() {
    const { t } = useI18n();
    const route = useRoute();
    return { t, route };
  },
  data() {
    return {
      isMobileMenuOpen: false,
      links: [
        { id: 'home', url: '/' },
        { id: 'worldMap', url: '/world-map/preview' },
        { id: 'characterPreview', url: '/characters/preview', label: 'Character Preview' },
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
    },
    isActiveLink(url) {
      return this.route.path === url;
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
  background: rgba(15, 20, 28, 0.6);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  z-index: 50;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.navbar {
  position: relative;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
.nav-menu {
  display: flex;
  list-style: none;
  gap: 0;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  flex-grow: 1;
}

.nav-item {
  position: relative;
}

.nav-link {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  padding: 1.5rem 1.8rem;
  font-size: 0.95rem;
  font-weight: 400;
  transition: color 0.3s ease;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    rgba(0, 255, 200, 0.6),
    transparent
  );
  transform: translateX(-50%);
  transition: width 0.4s ease;
}

.nav-item:hover .nav-link {
  color: rgba(255, 255, 255, 0.95);
}

.nav-item:hover .nav-link::after {
  width: 100%;
}

.nav-item.active .nav-link {
  color: rgba(0, 255, 200, 0.9);
}

.nav-item.active .nav-link::after {
  width: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(0, 255, 200, 0.8),
    transparent
  );
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
  background: rgba(15, 20, 28, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 8px;
  padding: 0;
  width: 85%;
  max-width: 320px;
  max-height: 60vh;
  overflow-y: auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 200, 0.3);
}

.mobile-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(0, 255, 200, 0.2);
  background: rgba(0, 0, 0, 0.2);
}

.mobile-menu-header h3 {
  color: rgba(0, 255, 200, 0.9);
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: 1px solid rgba(0, 255, 200, 0.3);
  color: rgba(0, 255, 200, 0.9);
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
  background: rgba(0, 255, 200, 0.1);
  border-color: rgba(0, 255, 200, 0.8);
}

.mobile-nav-list {
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
}

.mobile-nav-list li {
  margin: 0;
}

.mobile-nav-list .nav-link {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  padding: 0.875rem 1.25rem;
  font-size: clamp(0.85rem, 2vw, 0.95rem);
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  line-height: 1.2;
  position: relative;
}

.mobile-nav-list .nav-link::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 2px;
  background: linear-gradient(180deg,
    transparent,
    rgba(0, 255, 200, 0.6),
    transparent
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mobile-nav-list .nav-item:hover .nav-link {
  color: rgba(255, 255, 255, 0.95);
}

.mobile-nav-list .nav-item:hover .nav-link::after {
  opacity: 1;
}

.mobile-nav-list .nav-item.active .nav-link {
  color: rgba(0, 255, 200, 0.9);
}

.mobile-nav-list .nav-item.active .nav-link::after {
  opacity: 1;
  background: linear-gradient(180deg,
    transparent,
    rgba(0, 255, 200, 0.8),
    transparent
  );
}

.mobile-menu-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(0, 255, 200, 0.2);
  background: rgba(0, 0, 0, 0.2);
}

/* Responsive breakpoints */
@media (max-width: 1200px) {
  .nav-link {
    padding: 1.5rem 1.3rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 900px) {
  .nav-link {
    padding: 1.5rem 1rem;
    font-size: 0.85rem;
  }
}

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

  .nav-container {
    padding: 0 1rem;
  }

  /* Mobile navigation styling when displayed inline */
  .nav-menu {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-link {
    padding: 1.2rem 2rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  }

  .nav-link::after {
    left: 0;
    transform: none;
    height: 100%;
    width: 2px;
    background: linear-gradient(180deg,
      transparent,
      rgba(0, 255, 200, 0.6),
      transparent
    );
  }

  .nav-item:hover .nav-link::after {
    width: 2px;
  }

  .nav-item.active .nav-link::after {
    width: 2px;
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
</style>
