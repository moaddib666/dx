<template>
  <div class="item-selector">
    <div class="header-top">
      <h3 class="title">Items</h3>
      <button @click="$emit('close')" class="close-btn" title="Close Item Selector">
        ×
      </button>
    </div>
    <div class="items-grid">
      <SkillIcon
        v-for="item in filteredItems"
        :key="item.id"
        :skill="item.item.skill"
        :fade="!canPerformItemAction(item)"
        @click="selectItem(item)"
        :style="{ cursor: canPerformItemAction(item) ? 'pointer' : 'not-allowed' }"
      />
    </div>
  </div>
</template>

<script>

import SkillIcon from "@/components/Action/ActionIcon.vue";

export default {
  name: "ItemSelector",
  components: {SkillIcon},
  emits: ['item-selected', 'close'],
  props: {
    characterItems: {
      type: Array,
      required: true,
    },
    playerService: {
      type: Object,
      default: null,
    },
    selectedTypes: {
      type: Array,
      default: () => []
    },
  },
  computed: {
    filteredItems() {
      // If no types are selected, show all items
      if (this.selectedTypes.length === 0) {
        return this.characterItems;
      }

      // Filter items by selected types
      return this.characterItems.filter(item =>
        item.item && item.item.skill && this.selectedTypes.includes(item.item.skill.type || 'utility')
      );
    }
  },
  methods: {
    selectItem(item) {
      // Only emit the event if the player has enough resources
      if (this.canPerformItemAction(item)) {
        this.$emit("item-selected", item);
      }
    },
    canPerformItemAction(item) {
      // If playerService is not available or item has no skill, assume action can be performed
      if (!this.playerService || !item.item || !item.item.skill) return true;

      const skill = item.item.skill;

      // Check if the skill has costs
      if (!skill.cost || !Array.isArray(skill.cost) || skill.cost.length === 0) return true;

      // Check each cost type
      for (const cost of skill.cost) {
        const currentValue = this.playerService.getCurrentAttributeValue(cost.kind);
        // If we can't get the current value or it's less than the cost, return false
        if (currentValue === null || currentValue < cost.value) {
          return false;
        }
      }

      return true;
    },
  },
};
</script>

<style scoped>
.item-selector {
  display: flex;
  flex-direction: column;
  padding: 0.5rem;
  box-sizing: border-box;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  position: relative;
}

.title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-50%) scale(1.1);
  color: #7fff16;
}

.close-btn:active {
  transform: translateY(-50%) scale(0.95);
}

.items-grid {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping of icons */
  gap: 0.5rem; /* Space between icons */
  justify-content: flex-start; /* Center icons */
  align-items: flex-start; /* Align icons */
}
</style>
