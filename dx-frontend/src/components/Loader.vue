<template>
  <div class="loading-overlay">
    <div class="loading-spinner"></div>
    <div class="loading-text">{{ text || t('common.loading') }}</div>
    <div class="loading-message">{{ message || t('common.preparingAdventure') }}</div>
  </div>
</template>

<script>
import { useI18n } from "vue-i18n";

export default {
  name: "Loader",
  props: {
    text: {
      type: String,
      default: null
    },
    message: {
      type: String,
      default: null
    }
  },
  setup() {
    const { t } = useI18n();
    return { t };
  }
};
</script>

<style scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(42, 43, 43, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid transparent;
  border-top: 3px solid var(--cyber-yellow, #ffd700);
  border-right: 3px solid #00ffff;
  border-bottom: 3px solid var(--cyber-yellow, #ffd700);
  border-left: 3px solid #00ffff;
  animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
  box-shadow:
    0 0 15px rgba(255, 215, 0, 0.5),
    0 0 30px rgba(0, 255, 255, 0.3),
    inset 0 0 15px rgba(255, 215, 0, 0.3);
  position: relative;
}

.loading-spinner::before {
  content: '';
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border-radius: 50%;
  border: 1px solid rgba(255, 215, 0, 0.3);
  animation: pulse 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(255, 215, 0, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 215, 0, 0);
  }
}

.loading-text {
  margin-top: 20px;
  font-size: 18px;
  font-weight: 600;
  color: var(--cyber-yellow, #ffd700);
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  letter-spacing: 1px;
  animation: fadeInOut 2s ease-in-out infinite;
}

.loading-message {
  margin-top: 10px;
  font-size: 14px;
  color: #00ffff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
  opacity: 0.8;
  letter-spacing: 0.5px;
  animation: typewriter 4s steps(30, end) infinite;
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid #00ffff;
  max-width: 0;
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

@keyframes typewriter {
  0% { max-width: 0; }
  20% { max-width: 230px; }
  80% { max-width: 230px; }
  100% { max-width: 0; }
}
</style>