<template>
  <footer class="footer">
    <div class="footer-content">
      <!-- Contact Us Section -->
      <div class="contact-section">
        <div class="social-icons">
          <a
            v-for="social in socialLinks"
            :key="social.name"
            :href="social.url"
            :title="social.name"
            class="social-link"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i :class="social.icon" class="social-icon"></i>
            <span class="social-name">{{ social.name }}</span>
          </a>
        </div>
      </div>

      <!-- Copyright Section -->
      <div class="copyright-section">
        <p class="copyright-text">
          © {{ currentYear }} Dimension-X. All rights reserved.
        </p>
        <p class="creator-text">
          Created by <a href="mailto:moaddib666@gmail.com" class="creator-link">{{ t('footer.creator') }}</a>
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

export default {
  name: 'Footer',
  setup() {
    const { t } = useI18n();

    // Automatic year updating
    const currentYear = computed(() => {
      return new Date().getFullYear();
    });

    // Social media links - easily extensible
    const socialLinks = [
      {
        name: 'Facebook',
        url: 'https://www.facebook.com/groups/1290551983081540',
        icon: 'fab fa-facebook-f'
      },
      {
        name: 'Discord',
        url: 'https://discord.gg/d8Y8hN39mf',
        icon: 'fab fa-discord'
      },
      {
        name: 'Instagram',
        url: 'https://www.instagram.com/dimensionxlive/',
        icon: 'fab fa-instagram'
      },
      {
        name: 'Gmail',
        url: 'mailto:dimensionxlive@gmail.com',
        icon: 'fas fa-envelope'
      },
      {
        name: 'Patreon',
        url: 'https://www.patreon.com/c/dimension_x_live',
        icon: 'fab fa-patreon'
      },
      {
        name: 'Telegram',
        url: 'https://t.me/dimensionxlive',
        icon: 'fab fa-telegram-plane'
      },
      {
        name: 'GitHub',
        url: 'https://github.com/moaddib666/dx',
        icon: 'fab fa-github'
      },
      {
        name: 'TikTok',
        url: 'https://www.tiktok.com/@dimensionxlive',
        icon: 'fab fa-tiktok'
      },
      {
        name: 'YouTube',
        url: 'https://www.youtube.com/@moaddib666',
        icon: 'fab fa-youtube'
      }
    ];

    return {
      t,
      currentYear,
      socialLinks
    };
  }
}
</script>

<style scoped>
.footer {
  background: rgba(15, 20, 28, 0.6);
  backdrop-filter: blur(12px);
  color: rgba(255, 255, 255, 0.7);
  padding: 2rem 1rem 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  z-index: 50;
  margin-top: auto;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Contact Section */
.contact-section {
  text-align: center;
}

.section-title {
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.125rem;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
  text-shadow: 0 0 5px rgba(0, 255, 200, 0.3);
}

.social-icons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.125rem;
  flex-wrap: wrap;
}

.social-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  color: #e0e0e0;
  text-decoration: none;
  padding: 0.563rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(15, 20, 28, 0.97);
  box-shadow:
    0 6px 12px rgba(0, 0, 0, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.6),
    inset 0 -4px 8px rgba(8, 12, 18, 0.9),
    inset 0 1px 2px rgba(35, 45, 55, 0.6);
  background-image: linear-gradient(145deg, rgba(25, 32, 42, 0.95), rgba(12, 16, 22, 0.98));
  border: 2px solid rgba(35, 45, 55, 0.9);
  border-top: 2px solid rgba(45, 55, 65, 0.7);
  width: 60px;
  height: 60px;
  position: relative;
}

.social-link:hover {
  background-image: linear-gradient(145deg, rgba(30, 38, 48, 0.98), rgba(18, 24, 32, 0.99));
  transform: translateY(-3px);
  box-shadow:
    0 8px 16px rgba(0, 0, 0, 0.5),
    0 4px 8px rgba(0, 0, 0, 0.7),
    inset 0 -5px 10px rgba(6, 10, 16, 0.95),
    inset 0 2px 4px rgba(40, 50, 60, 0.7);
  border-top: 2px solid rgba(50, 60, 70, 0.8);
}

.social-link:active {
  transform: translateY(1px);
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.6),
    inset 0 4px 12px rgba(5, 8, 12, 0.95),
    inset 0 -2px 4px rgba(20, 28, 36, 0.5);
  background-image: linear-gradient(145deg, rgba(12, 16, 22, 0.99), rgba(20, 26, 34, 0.97));
  border-top: 2px solid rgba(25, 35, 45, 0.9);
}

.social-icon {
  font-size: 1.125rem;
  transition: color 0.3s ease;
}

.social-name {
  font-size: 0.6rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.375px;
}

/* Social platform specific colors on hover */
.social-link:hover .social-icon {
  color: rgba(0, 255, 200, 0.9);
}

.social-link[title="Facebook"]:hover .social-icon {
  color: #1877f2;
}

.social-link[title="Discord"]:hover .social-icon {
  color: #5865f2;
}

.social-link[title="Instagram"]:hover .social-icon {
  color: #e4405f;
}

.social-link[title="Gmail"]:hover .social-icon {
  color: #ea4335;
}

.social-link[title="Patreon"]:hover .social-icon {
  color: #ff424d;
}

.social-link[title="Telegram"]:hover .social-icon {
  color: #0088cc;
}

.social-link[title="GitHub"]:hover .social-icon {
  color: #f0f6fc;
}

/* Copyright Section */
.copyright-section {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.copyright-text {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #b0b0b0;
}

.creator-text {
  margin: 0;
  font-size: 0.85rem;
  color: #888;
}

.creator-link {
  color: rgba(0, 255, 200, 0.9);
  text-decoration: none;
  transition: color 0.3s ease;
}

.creator-link:hover {
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 0 5px rgba(0, 255, 200, 0.5);
}

/* Responsive Design */
@media (max-width: 479px) {
  .footer {
    padding: 0.563rem 0.188rem 0.375rem; /* Reduced height by more than 50% */
  }

  .contact-section {
    margin-bottom: 0.375rem; /* Reduced spacing */
  }

  .social-icons {
    gap: 0.375rem; /* Reduced gap for more compact layout */
  }

  .social-link {
    min-width: 35px; /* Square and more minimalistic */
    max-width: 35px;
    height: 35px;
    padding: 0.188rem;
    border-radius: 4px; /* More square appearance */
    justify-content: center; /* Center icon only */
  }

  .social-icon {
    font-size: 0.875rem;
  }

  .social-name {
    display: none; /* Hide text labels on mobile */
  }

  .section-title {
    font-size: 0.75rem;
    margin-bottom: 0.375rem; /* Reduced margin */
  }

  .footer-content {
    gap: 0.75rem; /* Reduced gap between sections */
  }
}

@media (min-width: 480px) and (max-width: 767px) {
  .social-icons {
    gap: 0.938rem;
  }
}

@media (min-width: 768px) {
  .footer-content {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
  }

  .contact-section {
    text-align: left;
    flex: 1;
  }

  .copyright-section {
    text-align: right;
    border-top: none;
    padding-top: 0;
    flex-shrink: 0;
  }

  .social-icons {
    justify-content: flex-start;
  }
}

@media (min-width: 1200px) {
  .footer {
    padding: 1.875rem 1.5rem 1.125rem;
  }

  .social-icons {
    gap: 1.5rem;
  }

  .social-link {
    min-width: 67.5px;
    padding: 0.75rem;
  }

  .social-icon {
    font-size: 1.313rem;
  }

  .section-title {
    font-size: 1.313rem;
  }
}
</style>
