<template>
  <form class="register-form" @submit.prevent="handleSubmit">
    <div v-if="Object.keys(errors).length" class="error-message">
      <div v-for="(message, field) in errors" :key="field">
        <strong>{{ field }}</strong>: {{ message }}
      </div>
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
    </div>

    <div class="form-group">
      <label for="first_name">First Name (Optional)</label>
      <input type="text" id="first_name" v-model="firstName" placeholder="Enter your first name" />
    </div>

    <div class="form-group">
      <label for="last_name">Last Name (Optional)</label>
      <input type="text" id="last_name" v-model="lastName" placeholder="Enter your last name" />
    </div>

    <div class="form-actions">
      <LandingButton :action="handleSubmit">Register</LandingButton>
    </div>
  </form>
</template>

<script>
import { ref } from 'vue';
import LandingButton from "@/components/btn/LandingButton.vue";
import { useRouter } from 'vue-router';
import {ClientGameApi} from "@/api/backendService.js";

export default {
  name: 'RegisterForm',
  components: {
    LandingButton,
  },
  setup() {
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const firstName = ref('');
    const lastName = ref('');
    const errors = ref({});

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
          errors.value.general = "An unexpected error occurred. Please try again later.";
        }
      }
    };

    return {
      email,
      password,
      firstName,
      lastName,
      errors,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.register-form {
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
</style>
