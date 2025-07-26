<script setup lang="ts">
import {defineProps, computed} from 'vue';
import {Quest} from '@/api/dx-backend';

interface Props {
  quest: Quest;
  selected: boolean;
  selectedItem: string;
  collapsed: boolean;
}

const props = defineProps<Props>();

// Determine if this quest is active
const isActive = computed(() => {
  return props.selectedItem === props.quest.id;
});
</script>

<template>
  <div class="list-item" :class="{ 'selected': isActive }">
    <div class="orb"></div>
    <span class="item-text">{{ props.quest.title }}</span>
  </div>
</template>

<style scoped>
.list-item {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  background: transparent;
  border: 1px solid rgba(42, 42, 42, 0.5);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
  margin-bottom: 3px;
}

.list-item:hover {
  background: transparent;
  border-color: #00e6ff;
  transform: translateY(-2px);
  box-shadow:
      0 0 0 1px rgba(0, 230, 255, 0.1);
}

.list-item.selected {
  background: rgba(0, 230, 255, 0.05);
  border-color: #00e6ff;
  box-shadow:
      0 0 10px rgba(0, 230, 255, 0.15),
      0 0 0 1px rgba(0, 230, 255, 0.2);
}

.orb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
  position: relative;
  background: radial-gradient(circle at 35% 35%, #1a2a3a, #0d1825);
  border: 1px solid rgba(0, 196, 255, 0.4);
  transition: all 0.3s ease;
  flex-shrink: 0;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3), 0 0 2px rgba(0, 196, 255, 0.2);
}

.orb::before {
  content: '';
  position: absolute;
  top: 15%;
  left: 15%;
  width: 35%;
  height: 35%;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.7), transparent 70%);
  transition: all 0.4s ease;
}

.orb::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  background:
    linear-gradient(45deg, transparent, rgba(0, 196, 255, 0.1), transparent),
    linear-gradient(135deg, transparent, rgba(0, 255, 127, 0.05), transparent);
  opacity: 0.6;
  transition: all 0.4s ease;
  z-index: -1;
}

.list-item:hover .orb {
  background: radial-gradient(circle at 35% 35%, #00e6ff, #0088aa);
  border-color: #00ff7f;
  box-shadow:
      0 0 10px rgba(0, 230, 255, 0.5),
      0 0 20px rgba(0, 230, 255, 0.2);
  transform: scale(1.05);
}

.list-item:hover .orb::before {
  background: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.3) 50%, transparent 70%);
  transform: scale(1.1);
}

.list-item:hover .orb::after {
  opacity: 0.9;
  background:
    linear-gradient(45deg, transparent, rgba(0, 230, 255, 0.4), transparent),
    linear-gradient(135deg, transparent, rgba(0, 255, 127, 0.2), transparent);
}

.list-item.selected .orb {
  background: radial-gradient(circle at 35% 35%, #00e6ff, #0088aa);
  border-color: #00e6ff;
  box-shadow:
      0 0 15px rgba(0, 230, 255, 0.8),
      0 0 30px rgba(0, 230, 255, 0.4);
}

.list-item.selected .orb::before {
  background: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.4) 50%, transparent 70%);
}

.list-item.selected .orb::after {
  opacity: 1;
  background:
    linear-gradient(45deg, transparent, rgba(0, 230, 255, 0.5), transparent),
    linear-gradient(135deg, transparent, rgba(0, 255, 127, 0.1), transparent);
}

.item-text {
  color: #e5e5e5;
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0.1px;
  transition: all 0.3s ease;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.6);
  font-family: var(--font-body);
}

.list-item:hover .item-text {
  color: #ffffff;
  text-shadow:
      0 0 6px rgba(0, 230, 255, 0.3),
      0 1px 1px rgba(0, 0, 0, 0.6);
}

.list-item.selected .item-text {
  color: #ffffff;
  text-shadow:
      0 0 5px rgba(0, 230, 255, 0.4),
      0 1px 1px rgba(0, 0, 0, 0.6);
}

/* Subtle pulse animation for selected items */
.list-item.selected .orb {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
      box-shadow:
          0 0 8px rgba(0, 230, 255, 0.6),
          0 0 15px rgba(0, 230, 255, 0.3);
  }
  50% {
      box-shadow:
          0 0 10px rgba(0, 230, 255, 0.8),
          0 0 20px rgba(0, 230, 255, 0.4),
          0 0 30px rgba(0, 230, 255, 0.2);
  }
}

/* Ripple effect on click */
.list-item::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle,
    rgba(0, 230, 255, 0.15) 0%,
    rgba(0, 255, 127, 0.05) 40%,
    transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.4s ease-out;
  pointer-events: none;
}

.list-item:active::before {
  width: 200px;
  height: 200px;
}

/* Responsive design for smaller containers */
@media (max-width: 480px), (max-width: 30vw) {
  .list-item {
    padding: 4px 8px;
    margin-bottom: 2px;
  }

  .orb {
    width: 10px;
    height: 10px;
    margin-right: 6px;
  }

  .item-text {
    font-size: 10px;
  }
}
</style>