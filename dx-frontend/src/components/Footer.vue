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
        url: 'https://facebook.com/dimensionx', // Replace with actual URL
        icon: 'fab fa-facebook-f'
      },
      {
        name: 'Discord',
        url: 'https://discord.gg/dimensionx', // Replace with actual URL
        icon: 'fab fa-discord'
      },
      {
        name: 'Instagram',
        url: 'https://instagram.com/dimensionx', // Replace with actual URL
        icon: 'fab fa-instagram'
      },
      {
        name: 'Gmail',
        url: 'mailto:moaddib666@gmail.com',
        icon: 'fas fa-envelope'
      },
      {
        name: 'Patreon',
        url: 'https://patreon.com/dimensionx', // Replace with actual URL
        icon: 'fab fa-patreon'
      },
      {
        name: 'Telegram',
        url: 'https://t.me/dimensionx', // Replace with actual URL
        icon: 'fab fa-telegram-plane'
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
  background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
  color: #e0e0e0;
  padding: 2rem 1rem 1rem;
  border-top: 2px solid #444;
  z-index: 50;
  margin-top: auto;
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
  color: #FFFFFF;
  font-size: 1.125rem;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
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
  gap: 0.375rem;
  color: #e0e0e0;
  text-decoration: none;
  padding: 0.563rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-width: 60px;
}

.social-link:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0, 255, 255, 0.2);
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
  color: #00ffff;
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
  color: #00ffff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.creator-link:hover {
  color: #ffffff;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
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
