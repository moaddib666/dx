<template>
  <div class="google-login" :style="buttonStyle" @click="handleGoogleSignIn">
    <div class="neon-border">
      <img src="@/assets/icons/google-icon.svg" alt="Google Icon" class="google-icon" />
      <span>Sign in with Google</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  layer: {
    type: Number,
    required: true,
    validator: value => value >= 0 && value <= 3
  }
});

const saturationValues = [100, 55, 35, 0];

const buttonStyle = computed(() => ({
  filter: `saturate(${saturationValues[props.layer]}%)`,
  transition: 'filter 1s ease'
}));

const handleGoogleSignIn = () => {
  // Redirect to your backend's Google OAuth endpoint
  window.location.href = 'https://your-backend.com/auth/google';
};
</script>

<style scoped>
.google-login {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  width: 250px;
  height: 50px;
  margin: 20px auto;
  transition: all 0.3s ease;
}

.google-login:hover {
  transform: scale(1.05);
}

.google-login:active {
  transform: scale(0.95);
}

.neon-border {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, #00ffcc, #ff00ff);
  border-radius: 12px;
  padding: 10px;
  width: 100%;
  height: 100%;
  box-shadow: 0 0 10px #00ffcc;
  transition: box-shadow 0.3s ease;
}

.google-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

span {
  color: white;
  font-size: 16px;
  font-family: 'Arial', sans-serif;
  text-transform: uppercase;
}
</style>
