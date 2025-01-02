<template>
  <div class="action-selector">
    <SkillIcon
        v-for="action in actions"
        :key="action.id"
        :skill="action"
        @click="selectAction(action)"
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
  },
  methods: {
    selectAction(action) {
      this.$emit("skill-selected", action); // Emit event with selected action ID
    },
  },
};
</script>

<style scoped>
.action-selector {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping of icons */
  gap: 0.5rem; /* Space between icons */
  justify-content: center; /* Center icons */
  align-items: center; /* Align icons */
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>
