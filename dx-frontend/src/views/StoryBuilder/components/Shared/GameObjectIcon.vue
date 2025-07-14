<template>
  <div
    :class="[
      'game-object-icon',
      `game-object-icon--${type}`,
      { 'game-object-icon--interactive': interactive }
    ]"
    @click="handleClick"
    @mouseenter="showTooltip = true"
    @mouseleave="showTooltip = false"
  >
    <!-- Icon based on object type -->
    <span class="icon-symbol" :class="getIconClass(type, object)">
      {{ getIconSymbol(type, object) }}
    </span>

    <!-- Object name tooltip -->
    <div class="icon-tooltip" v-if="showTooltip && tooltipEnabled">
      <h5>{{ object.name || object.title }}</h5>
      <p v-if="object.description">{{ object.description }}</p>
      <div class="object-type">{{ formatType(type) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';

interface GameObject {
  id: string;
  name?: string;
  title?: string;
  description?: string;
  type?: string;
  role?: string;
  [key: string]: any;
}

const props = defineProps<{
  type: 'character' | 'item' | 'location' | 'skill' | 'quest' | 'condition';
  object: GameObject;
  interactive?: boolean;
  tooltipEnabled?: boolean;
}>();

const emit = defineEmits<{
  (e: 'click', object: GameObject, type: string): void;
}>();

// State
const showTooltip = ref(false);

// Helper functions
const getIconSymbol = (type: string, object: GameObject): string => {
  const iconMap = {
    'character': '👤',
    'item': '📦',
    'location': '📍',
    'skill': '⚡',
    'quest': '📜',
    'condition': '✓'
  };

  // Special cases based on object properties
  if (type === 'character' && object.role) {
    const roleIcons = {
      'merchant': '💰',
      'guard': '🛡️',
      'scientist': '🔬',
      'warrior': '⚔️',
      'mage': '🔮',
      'healer': '💊'
    };
    return roleIcons[object.role] || iconMap[type];
  }

  if (type === 'item' && object.type) {
    const itemTypeIcons = {
      'weapon': '⚔️',
      'armor': '🛡️',
      'potion': '🧪',
      'scroll': '📜',
      'key': '🔑',
      'food': '🍎'
    };
    return itemTypeIcons[object.type] || iconMap[type];
  }

  return iconMap[type] || '❓';
};

const getIconClass = (type: string, object: GameObject): string => {
  const baseClass = `icon-${type}`;

  // Add additional classes based on object properties
  if (type === 'character' && object.role) {
    return `${baseClass} icon-role-${object.role}`;
  }

  if (type === 'item' && object.type) {
    return `${baseClass} icon-item-${object.type}`;
  }

  return baseClass;
};

const formatType = (type: string): string => {
  return type.charAt(0).toUpperCase() + type.slice(1);
};

// Event handlers
const handleClick = () => {
  if (props.interactive) {
    emit('click', props.object, props.type);
  }
};
</script>

<style scoped>
.game-object-icon {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.game-object-icon--interactive {
  cursor: pointer;
}

.game-object-icon--interactive:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.game-object-icon--character {
  background: rgba(65, 105, 225, 0.2);
  border: 1px solid rgba(65, 105, 225, 0.3);
}

.game-object-icon--item {
  background: rgba(50, 205, 50, 0.2);
  border: 1px solid rgba(50, 205, 50, 0.3);
}

.game-object-icon--location {
  background: rgba(255, 69, 0, 0.2);
  border: 1px solid rgba(255, 69, 0, 0.3);
}

.game-object-icon--skill {
  background: rgba(255, 215, 0, 0.2);
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.game-object-icon--quest {
  background: rgba(138, 43, 226, 0.2);
  border: 1px solid rgba(138, 43, 226, 0.3);
}

.game-object-icon--condition {
  background: rgba(0, 191, 255, 0.2);
  border: 1px solid rgba(0, 191, 255, 0.3);
}

.icon-symbol {
  font-size: 1.5rem;
}

.icon-character {
  color: rgba(65, 105, 225, 1);
}

.icon-item {
  color: rgba(50, 205, 50, 1);
}

.icon-location {
  color: rgba(255, 69, 0, 1);
}

.icon-skill {
  color: rgba(255, 215, 0, 1);
}

.icon-quest {
  color: rgba(138, 43, 226, 1);
}

.icon-condition {
  color: rgba(0, 191, 255, 1);
}

/* Role-specific styling */
.icon-role-merchant {
  color: gold;
}

.icon-role-guard {
  color: silver;
}

.icon-role-scientist {
  color: lightblue;
}

.icon-role-warrior {
  color: crimson;
}

.icon-role-mage {
  color: purple;
}

.icon-role-healer {
  color: lightgreen;
}

/* Item-specific styling */
.icon-item-weapon {
  color: crimson;
}

.icon-item-armor {
  color: silver;
}

.icon-item-potion {
  color: lightblue;
}

.icon-item-scroll {
  color: beige;
}

.icon-item-key {
  color: gold;
}

.icon-item-food {
  color: lightgreen;
}

/* Tooltip */
.icon-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 0.75rem;
  margin-bottom: 10px;
  z-index: 100;
  pointer-events: none;
  opacity: 0;
  animation: fadeIn 0.2s ease forwards;
}

.icon-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: rgba(0, 0, 0, 0.9) transparent transparent transparent;
}

.icon-tooltip h5 {
  margin: 0 0 0.5rem 0;
  color: white;
  font-size: 1rem;
}

.icon-tooltip p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.8rem;
}

.icon-tooltip .object-type {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-50%) translateY(10px); }
  to { opacity: 1; transform: translateX(-50%) translateY(0); }
}

@media (max-width: 768px) {
  .game-object-icon {
    width: 32px;
    height: 32px;
  }

  .icon-symbol {
    font-size: 1.2rem;
  }

  .icon-tooltip {
    width: 160px;
    padding: 0.5rem;
    font-size: 0.8rem;
  }
}
</style>