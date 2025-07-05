<template>
  <div class="item-selector">
    <SkillIcon
        v-for="item in filteredItems"
        :key="item.id"
        :skill="item.item.skill"
        :fade="!canPerformItemAction(item)"
        @click="selectItem(item)"
        :style="{ cursor: canPerformItemAction(item) ? 'pointer' : 'not-allowed' }"
    />
  </div>
</template>

<script>

import SkillIcon from "@/components/Action/ActionIcon.vue";

export default {
  name: "ItemSelector",
  components: {SkillIcon},
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
  flex-wrap: wrap; /* Allow wrapping of icons */
  gap: 0.5rem; /* Space between icons */
  justify-content: flex-start; /* Center icons */
  align-items: flex-start; /* Align icons */
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>
