<template>
  <div class="action-selector">
    <SkillIcon
        v-for="action in filteredActions"
        :key="action.id"
        :skill="action"
        :fade="!canPerformAction(action)"
        @click="selectAction(action)"
        :style="{ cursor: canPerformAction(action) ? 'pointer' : 'not-allowed' }"
    />
  </div>
</template>

<script>

import SkillIcon from "@/components/Action/ActionIcon.vue";

export default {
  name: "SkillSelector",
  components: {SkillIcon},
  props: {
    actions: {
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
    filteredActions() {
      // If no types are selected, show all actions
      if (this.selectedTypes.length === 0) {
        return this.actions;
      }

      // Filter actions by selected types
      return this.actions.filter(action =>
        this.selectedTypes.includes(action.type || 'utility')
      );
    }
  },
  methods: {
    selectAction(action) {
      // Only emit the event if the player has enough resources
      if (this.canPerformAction(action)) {
        this.$emit("skill-selected", action);
      }
    },
    canPerformAction(action) {
      // If playerService is not available, assume action can be performed
      if (!this.playerService) return true;

      // Check if the action has costs
      if (!action.cost || !Array.isArray(action.cost) || action.cost.length === 0) return true;

      // Check each cost type
      for (const cost of action.cost) {
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
.action-selector {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping of icons */
  gap: 0.5rem; /* Space between icons */
  justify-content: flex-start; /* Center icons */
  align-items: flex-start; /* Align icons */
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>
