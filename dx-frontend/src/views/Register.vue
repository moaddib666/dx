<template>
  <div class="page-container">
    <AuthBackground @toggle-zoom="toggleZoom" />
    <ZoomModal
      :is-visible="isZoomed"
      :image-url="currentZoomedImage"
      @close="closeZoom"
    />

    <main class="auth-content">
      <TitleComponent>{{ t('auth.register') }}</TitleComponent>

      <form class="register-form" @submit.prevent="handleSubmit">
        <div v-if="Object.keys(errors).length" class="error-message">
          <div v-for="(message, field) in errors" :key="field">
            <strong>{{ field }}</strong>: {{ message }}
          </div>
        </div>

        <div class="form-group">
          <label for="email">{{ t('auth.email') }}</label>
          <input type="email" id="email" v-model="email" :placeholder="t('auth.enterEmail')" required />
        </div>

        <div class="form-group">
          <label for="password">{{ t('auth.password') }}</label>
          <input type="password" id="password" v-model="password" :placeholder="t('auth.enterPassword')" required />
        </div>

        <div class="form-group">
          <label for="first_name">{{ t('auth.firstName') }}</label>
          <input type="text" id="first_name" v-model="firstName" :placeholder="t('auth.enterFirstName')" />
        </div>

        <div class="form-group">
          <label for="last_name">{{ t('auth.lastName') }}</label>
          <input type="text" id="last_name" v-model="lastName" :placeholder="t('auth.enterLastName')" />
        </div>

        <div class="form-actions">
          <LandingButton :action="handleSubmit">{{ t('auth.register') }}</LandingButton>
        </div>

        <div class="alternative-login">
          <router-link :to="{ name: 'Login' }">{{ t('auth.haveAccount') }}</router-link>
        </div>
      </form>
    </main>
  </div>
</template>

<script>
import { ref } from 'vue';
import LandingButton from "@/components/btn/LandingButton.vue";
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {ClientGameApi} from "@/api/backendService.js";
import AuthBackground from "@/components/Auth/AuthBackground.vue";
import ZoomModal from "@/components/WhatIsIt/ZoomModal.vue";
import TitleComponent from "@/components/TitleComponent.vue";

export default {
  name: 'RegisterForm',
  components: {
    LandingButton,
    AuthBackground,
    ZoomModal,
    TitleComponent
  },
  setup() {
    const router = useRouter();
    const { t } = useI18n();
    const email = ref('');
    const password = ref('');
    const firstName = ref('');
    const lastName = ref('');
    const errors = ref({});
    const isZoomed = ref(false);
    const currentZoomedImage = ref('');
    const scrollPosition = ref(0);

    const handleSubmit = async () => {
      errors.value = {};
      try {
        const response = await ClientGameApi.clientRegisterLocalClientCreate({
          email: email.value,
          password: password.value,
          firstName: firstName.value,
          lastName: lastName.value,
        });

        if (response.status === 201) {
          router.push({ name: 'Login', query: { message: 'Registered' } });
        }
      } catch (error) {
        if (error.response && error.response.status === 400) {
          errors.value = error.response.data;
        } else {
          errors.value.general = t('auth.unexpectedError');
        }
      }
    };

    const toggleZoom = (event) => {
      // Get the image element from the event
      const imgElement = event.target.tagName === 'IMG' ? event.target : event.target.querySelector('img');

      if (imgElement) {
        // Use the actual resolved src from the DOM
        currentZoomedImage.value = imgElement.src;
        isZoomed.value = true;
        // Store current scroll position
        scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop;
        // Prevent body scrolling when modal is open
        document.body.style.overflow = 'hidden';
      } else if (event.target.classList.contains('auth-background')) {
        // Special case for auth background which is a fixed background
        // Get computed style to extract the actual URL
        const style = getComputedStyle(event.target);
        const bgImage = style.backgroundImage;
        // Extract URL from the "url('...')" format
        const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '');
        currentZoomedImage.value = url;
        isZoomed.value = true;
        // Store current scroll position
        scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop;
        // Prevent body scrolling when modal is open
        document.body.style.overflow = 'hidden';
      }
    };

    const closeZoom = () => {
      isZoomed.value = false;
      // Re-enable body scrolling
      document.body.style.overflow = '';
      // Restore scroll position
      window.scrollTo(0, scrollPosition.value);
    };

    return {
      email,
      password,
      firstName,
      lastName,
      errors,
      handleSubmit,
      isZoomed,
      currentZoomedImage,
      scrollPosition,
      toggleZoom,
      closeZoom,
      t
    };
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

.register-form {
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

.error-message div {
  margin-bottom: 0.5rem;
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

  .register-form {
    padding: 1.5rem;
  }
}
</style>
