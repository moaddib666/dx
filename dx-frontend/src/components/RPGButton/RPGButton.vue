<script setup lang="ts">
import { ButtonType } from '@/types/ButtonType'

interface Props {
  type?: ButtonType
}

const props = withDefaults(defineProps<Props>(), {
  type: ButtonType.DEFAULT
})
</script>

<template>
  <div :class="['button', `button--${props.type}`]">
    <slot></slot>
  </div>
</template>

<style scoped>
.button {
  border-style: solid;
  border-image-slice: 130 120 130 120 fill;
  border-image-source: url("@/assets/textures/button.png");
  border-image-width: 1.2em 1.2em 1.2em 1.2em;
  border-image-outset: 0px 0px 0px 0px;
  border-image-repeat: stretch stretch;
  padding: 1rem 1.2rem;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', serif;
  color: #fada95;
  cursor: pointer;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  position: relative;
  overflow: hidden;
}

/* Success Button - Golden green theme */
.button--success {
  color: #90ee90;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 10px rgba(255, 215, 0, 0.6);
}

.button--success::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("@/assets/btn-effects/success.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: soft-light;
}

/* Cancel Button - Dark red theme */
.button--cancel {
  color: #ff6b6b;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9), 0 0 10px rgba(220, 20, 60, 0.7);
}

.button--cancel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("@/assets/btn-effects/cancel.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: soft-light;
}

/* Submit Button - Electric blue theme */
.button--submit {
  color: #00bfff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 10px rgba(0, 191, 255, 0.8);
}

.button--submit::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("@/assets/btn-effects/submit.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: soft-light;
}

/* Default Button - Soft white theme */
.button--default {
  color: #fada95;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 8px rgba(255, 255, 255, 0.3);
}

.button--default::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("@/assets/btn-effects/default.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: soft-light;
}

/* Ensure slot content appears above overlays */
.button > * {
  position: relative;
  z-index: 3;
  pointer-events: none;
}

.button:hover {
  scale: 1.05;
}
.button:active {
  scale: 0.95;
}
</style>