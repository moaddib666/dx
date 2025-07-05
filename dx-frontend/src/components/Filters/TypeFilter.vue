<template>
  <div class="type-filter">
    <div
      v-for="type in actionTypes"
      :key="type.value"
      :class="['type-tag', `type-${type.value}`, { active: isSelected(type.value) }]"
      @click="toggleType(type.value)"
    >
      <i :class="'type-icon'">{{ type.icon }}</i>
      <span>{{ type.label }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "TypeFilter",
  props: {
    selectedTypes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      actionTypes: [
        { value: "attack", label: "Attack", icon: "⚔️" },
        { value: "defense", label: "Defense", icon: "🛡️" },
        { value: "heal", label: "Heal", icon: "❤️" },
        { value: "buff", label: "Buff", icon: "✨" },
        { value: "debuff", label: "Debuff", icon: "💀" },
        { value: "utility", label: "Utility", icon: "🔧" },
        { value: "special", label: "Special", icon: "🌟" }
      ]
    };
  },
  methods: {
    isSelected(type) {
      return this.selectedTypes.includes(type);
    },
    toggleType(type) {
      const updatedTypes = [...this.selectedTypes];
      const index = updatedTypes.indexOf(type);

      if (index === -1) {
        updatedTypes.push(type);
      } else {
        updatedTypes.splice(index, 1);
      }

      this.$emit('update:selectedTypes', updatedTypes);
    }
  }
};
</script>

<style scoped>
.type-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 0.5rem;
}

.type-tag {
  display: flex;
  align-items: center;
  padding: 0.3rem 0.6rem;
  border-radius: 0.3rem;
  background: rgba(0, 0, 0, 0.7);
  cursor: pointer;
  font-size: 0.8rem;
  opacity: 0.6;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.type-tag:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

.type-tag.active {
  opacity: 1;
  transform: scale(1.05);
}

.type-icon {
  margin-right: 0.3rem;
  font-style: normal;
}

/* Type-specific styling */
.type-attack {
  border-left: 3px solid #ff1744;
}
.type-attack.active {
  box-shadow: 0 0 5px #ff1744;
}

.type-defense {
  border-left: 3px solid #00e5ff;
}
.type-defense.active {
  box-shadow: 0 0 5px #00e5ff;
}

.type-heal {
  border-left: 3px solid #00ff00;
}
.type-heal.active {
  box-shadow: 0 0 5px #00ff00;
}

.type-buff {
  border-left: 3px solid #ffc107;
}
.type-buff.active {
  box-shadow: 0 0 5px #ffc107;
}

.type-debuff {
  border-left: 3px solid #b71c1c;
}
.type-debuff.active {
  box-shadow: 0 0 5px #b71c1c;
}

.type-utility {
  border-left: 3px solid #9e9e9e;
}
.type-utility.active {
  box-shadow: 0 0 5px #9e9e9e;
}

.type-special {
  border-left: 3px solid #673ab7;
}
.type-special.active {
  box-shadow: 0 0 5px #673ab7;
}
</style>