<template>
  <div class="mode-toggle">
    <div class="mode-toggle__label">Mode:</div>
    <div class="mode-toggle__switch">
      <button
        class="mode-button"
        :class="{ 'mode-button--active': !modelValue }"
        @click="$emit('update:modelValue', false)"
      >
        <span class="icon">👁️</span> View
      </button>
      <button
        class="mode-button"
        :class="{ 'mode-button--active': modelValue }"
        @click="$emit('update:modelValue', true)"
      >
        <span class="icon">✏️</span> Edit
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps<{
  modelValue: boolean;
}>();

defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();
</script>

<style scoped>
.mode-toggle {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mode-toggle__label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.mode-toggle__switch {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  padding: 0.25rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.mode-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-button:hover {
  color: white;
}

.mode-button--active {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
}

.icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .mode-toggle {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .mode-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}
</style>