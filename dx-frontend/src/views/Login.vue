<template>
  <div>
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

    </form>
  </div>
</template>

<script>
import axios from "axios";
import { useI18n } from "vue-i18n";

export default {
  name: "Login",
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      email: "",
      password: "",
      errorMessage: null,
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
  },
};
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: #1c1c1c;
  border: 2px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  margin: 2rem auto;
}

.error-message {
  color: #ff4d4d;
  background: #2e2e2e;
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
  background: #292929;
  color: #e0e0e0;
  font-size: 1rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
}

.form-group input:focus {
  outline: 2px solid #e0e0e0;
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
  transition: background 0.3s ease;
}

.form-actions button:hover {
  background: #555;
}

.alternative-login {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.alternative-login a {
  color: #66aaff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.alternative-login a:hover {
  color: #99ccff;
  text-decoration: underline;
}
</style>
