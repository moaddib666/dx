<template>
  <div class="item-selector">
    <SkillIcon
        v-for="item in characterItems"
        :key="item.id"
        :skill="item.item.skill"
        @click="selectItem(item)"
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
  },
  methods: {
    selectItem(item) {
      this.$emit("item-selected", item); // Emit event with selected item ID
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
