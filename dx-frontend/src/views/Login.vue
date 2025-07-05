<template>
  <div class="page-container">
    <AuthBackground @toggle-zoom="toggleZoom" />
    <ZoomModal
      :is-visible="isZoomed"
      :image-url="currentZoomedImage"
      @close="closeZoom"
    />

    <main class="auth-content">
      <TitleComponent>{{ t('auth.login') }}</TitleComponent>

      <form class="login-form" @submit.prevent="login">
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <div class="form-group">
          <label for="email">{{ t('auth.email') }}</label>
          <input id="email" v-model="email" :placeholder="t('auth.enterEmail')" type="email" required />
        </div>

        <div class="form-group">
          <label for="password">{{ t('auth.password') }}</label>
          <input id="password" v-model="password" type="password" :placeholder="t('auth.enterPassword')" required />
        </div>

        <div class="form-actions">
          <button type="submit">{{ t('auth.login') }}</button>
        </div>

        <div class="alternative-login">
          <router-link :to="{ name: 'Register' }">{{ t('auth.needAccount') }}</router-link>
        </div>
      </form>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import { useI18n } from "vue-i18n";
import AuthBackground from "@/components/Auth/AuthBackground.vue";
import ZoomModal from "@/components/WhatIsIt/ZoomModal.vue";
import TitleComponent from "@/components/TitleComponent.vue";

export default {
  name: "Login",
  components: {
    AuthBackground,
    ZoomModal,
    TitleComponent
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      email: "",
      password: "",
      errorMessage: null,
      isZoomed: false,
      currentZoomedImage: '',
      scrollPosition: 0
    };
  },
  methods: {
    async login() {
      try {
        const loginUrl = `${import.meta.env.VITE_API_BASE_URL}${import.meta.env.VITE_LOGIN_URL}`;
        const response = await axios.post(loginUrl, {
          email: this.email,
          password: this.password,
        });

        const { access, refresh } = response.data;
        this.$store.dispatch("login", { token: access });
        this.$router.push({ name: "PlayerHomeDashboard" });
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = this.t('auth.invalidCredentials');
        } else {
          this.errorMessage = this.t('auth.unexpectedError');
        }
      }
    },
    toggleZoom(event) {
      // Get the image element from the event
      const imgElement = event.target.tagName === 'IMG' ? event.target : event.target.querySelector('img');

      if (imgElement) {
        // Use the actual resolved src from the DOM
        this.currentZoomedImage = imgElement.src;
        this.isZoomed = true;
        // Store current scroll position
        this.scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        // Prevent body scrolling when modal is open
        document.body.style.overflow = 'hidden';
      } else if (event.target.classList.contains('auth-background')) {
        // Special case for auth background which is a fixed background
        // Get computed style to extract the actual URL
        const style = getComputedStyle(event.target);
        const bgImage = style.backgroundImage;
        // Extract URL from the "url('...')" format
        const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '');
        this.currentZoomedImage = url;
        this.isZoomed = true;
        // Store current scroll position
        this.scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        // Prevent body scrolling when modal is open
        document.body.style.overflow = 'hidden';
      }
    },
    closeZoom() {
      this.isZoomed = false;
      // Re-enable body scrolling
      document.body.style.overflow = '';
      // Restore scroll position
      window.scrollTo(0, this.scrollPosition);
    }
  },
};
</script>

<style scoped>
:root {
  --cyber-yellow: #ffd700;
  --cyber-cyan: #00ffff;
  --light-steel-blue: #b0c4de;
  --dark-overlay: rgba(0, 0, 0, 0.7);
}

.page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.auth-content {
  padding: 1rem;
  color: white;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: rgba(28, 28, 28, 0.8);
  border: 2px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  margin: 2rem auto;
  backdrop-filter: blur(5px);
  width: 100%;
}

.error-message {
  color: #ff4d4d;
  background: rgba(46, 46, 46, 0.8);
  padding: 1rem;
  border-radius: 4px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-size: 1rem;
  font-weight: bold;
  color: #e0e0e0;
}

.form-group input {
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background: rgba(41, 41, 41, 0.8);
  color: #e0e0e0;
  font-size: 1rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
}

.form-group input:focus {
  outline: 2px solid var(--cyber-cyan);
}

.form-actions {
  display: flex;
  justify-content: center;
}

.form-actions button {
  padding: 0.75rem 1.5rem;
  background: #444;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.form-actions button:hover {
  background: #555;
  border-color: var(--cyber-cyan);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.alternative-login {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.alternative-login a {
  color: var(--cyber-cyan);
  text-decoration: none;
  transition: color 0.3s ease;
}

.alternative-login a:hover {
  color: var(--cyber-yellow);
  text-decoration: underline;
}

@media (max-width: 768px) {
  .auth-content {
    padding: 30px;
    padding-top: 80px;
  }
}

@media (max-width: 480px) {
  .auth-content {
    padding: 20px;
    padding-top: 60px;
  }

  .login-form {
    padding: 1.5rem;
  }
}
</style>
