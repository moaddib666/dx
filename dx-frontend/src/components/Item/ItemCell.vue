<template>
  <div class="item-cell" @click="handleClick" :title="itemDetailsTooltip">
    <!-- Item Icon -->
    <img :src="item.icon" alt="Item Icon" class="item-icon"/>

    <!-- Type Indicator -->
    <div class="type-indicator" :class="typeClass">{{ item.type }}</div>

    <!-- Additional Info Overlay -->
    <div class="overlay">
      <div v-if="chargesLeft !== null" class="charges">Charges: {{ chargesLeft }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ItemCell",
  props: {
    itemData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    item() {
      return this.itemData.item || {};
    },
    chargesLeft() {
      return this.itemData.charges_left || null;
    },
    typeClass() {
      // Assign color class based on type
      const typeColors = {
        weapon: "type-weapon",
        armor: "type-armor",
        artifact: "type-artifact",
        amulet: "type-amulet",
        material: "type-material",
        quest: "type-quest",
        misc: "type-misc",
        food: "type-food",
        rune: "type-rune",
        default: "type-default",
      };
      return typeColors[this.item.type] || typeColors.default;
    },
    itemDetailsTooltip() {
      return `${this.item.name}\n${this.item.description}\nCharges Left: ${this.chargesLeft}`;
    },
  },
  methods: {
    handleClick() {
      this.$emit("item-clicked", this.itemData.id);
    },
  },
};
</script>

<style scoped>
.item-cell {
  position: relative;
  width: 5rem;
  height: 5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.item-cell:hover {
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.item-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.type-indicator {
  position: absolute;
  top: 0.1rem;
  left: 0.1rem;
  padding: 0.2rem 0.5rem;
  font-size: 0.5rem;
  font-weight: bold;
  border-radius: 1rem;
  color: white;
  text-transform: uppercase;
}

/* Colors for Different Types */
.type-weapon {
  background-color: #f44336;
}

.type-armor {
  background-color: #4caf50;
}

.type-artifact {
  background-color: #9c27b0;
}

.type-amulet {
  background-color: #ff9800;
}

.type-material {
  background-color: #8bc34a;
}

.type-quest {
  background-color: #3f51b5;
}

.type-misc {
  background-color: #607d8b;
}

.type-food {
  background-color: #ff5722;
}

.type-rune {
  background-color: #2196f3;
}

.type-default {
  background-color: #9e9e9e;
}

.overlay {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.8);
  padding: 0.3rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  font-size: 0.7rem;
  gap: 0.2rem;
}

.item-name {
  font-weight: bold;
  text-align: center;
}

.charges {
  font-size: 0.6rem;
  color: #ffeb3b;
}
</style>
