<template>
  <div>
    <div class="login-container">
      <div class="login-form">
        <form @submit.prevent="login">
          <input v-model="email" placeholder="E-mail" type="email" />
          <input v-model="password" type="password" placeholder="Password" />
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HeroSection from '@/components/HeroSection.vue';

export default {
  name: 'Login',
  components: {},
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const loginUrl = `${import.meta.env.VITE_API_BASE_URL}${import.meta.env.VITE_LOGIN_URL}`;
        const response = await axios.post(loginUrl, { email: this.email, password: this.password });
        const { access, refresh } = response.data;

        // Dispatch login action to Vuex store
        this.$store.dispatch('login', { token: access });
        // Redirect to the game route
        this.$router.push('/game');
      } catch (error) {
        console.error('Login failed', error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
}

.login-form {
  background: rgba(0, 0, 0, 0.8);
  padding: 20px 30px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form input {
  width: 100%;
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.login-form input::placeholder {
  color: #ccc;
}

.login-form button {
  width: 100%;
  padding: 10px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 5px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.3s;
}

.login-form button:hover {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}
</style>
