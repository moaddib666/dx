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
  padding: 8px 12px;
  background: transparent;
  border: 1px solid rgba(42, 42, 42, 0.5);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
  margin-bottom: 4px;
}

.list-item:hover {
  background: transparent;
  border-color: #00d4ff;
  transform: translateY(-2px);
  box-shadow:
      0 0 0 1px rgba(0, 212, 255, 0.1);
}

.list-item.selected {
  background: rgba(0, 212, 255, 0.05);
  border-color: #00d4ff;
  box-shadow:
      0 0 10px rgba(0, 212, 255, 0.15),
      0 0 0 1px rgba(0, 212, 255, 0.2);
}

.orb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  margin-right: 10px;
  position: relative;
  background: radial-gradient(circle at 35% 35%, #3a3a3a, #1a1a1a);
  border: 1px solid #444;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.orb::before {
  content: '';
  position: absolute;
  top: 15%;
  left: 15%;
  width: 35%;
  height: 35%;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.8), transparent 70%);
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
  background: linear-gradient(45deg, transparent, rgba(0, 212, 255, 0.0), transparent);
  opacity: 0;
  transition: all 0.4s ease;
  z-index: -1;
}

.list-item:hover .orb {
  background: radial-gradient(circle at 35% 35%, #00d4ff, #0099cc);
  border-color: #00d4ff;
  box-shadow:
      0 0 10px rgba(0, 212, 255, 0.5),
      0 0 20px rgba(0, 212, 255, 0.2);
  transform: scale(1.05);
}

.list-item:hover .orb::before {
  background: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.3) 50%, transparent 70%);
  transform: scale(1.1);
}

.list-item:hover .orb::after {
  opacity: 0.8;
  background: linear-gradient(45deg, transparent, rgba(0, 212, 255, 0.3), transparent);
}

.list-item.selected .orb {
  background: radial-gradient(circle at 35% 35%, #00d4ff, #0099cc);
  border-color: #00d4ff;
  box-shadow:
      0 0 15px rgba(0, 212, 255, 0.8),
      0 0 30px rgba(0, 212, 255, 0.4);
}

.list-item.selected .orb::before {
  background: radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.3) 50%, transparent 70%);
}

.item-text {
  color: #e5e5e5;
  font-size: 13px;
  font-weight: 400;
  letter-spacing: 0.2px;
  transition: all 0.3s ease;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.6);
  font-family: var(--font-body);
}

.list-item:hover .item-text {
  color: #ffffff;
  text-shadow:
      0 0 6px rgba(0, 212, 255, 0.3),
      0 1px 1px rgba(0, 0, 0, 0.6);
}

.list-item.selected .item-text {
  color: #ffffff;
  text-shadow:
      0 0 5px rgba(0, 212, 255, 0.4),
      0 1px 1px rgba(0, 0, 0, 0.6);
}

/* Subtle pulse animation for selected items */
.list-item.selected .orb {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
      box-shadow:
          0 0 8px rgba(0, 212, 255, 0.6),
          0 0 15px rgba(0, 212, 255, 0.3);
  }
  50% {
      box-shadow:
          0 0 10px rgba(0, 212, 255, 0.8),
          0 0 20px rgba(0, 212, 255, 0.4);
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
  background: radial-gradient(circle, rgba(0, 212, 255, 0.15) 0%, transparent 70%);
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
    padding: 6px 10px;
    margin-bottom: 3px;
  }

  .orb {
    width: 12px;
    height: 12px;
    margin-right: 8px;
  }

  .item-text {
    font-size: 12px;
  }
}
</style>