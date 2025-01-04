<template>
  <div class="special-selector">
    <SkillIcon
        :useSlotIcon="true"
        @click="selectItem(
            {
             id: 'LONG_REST',
             actionType: 'LONG_REST',
             actionData: {},
             skill: {
               name: 'Long Rest',
               type: 'special',
               icon: null,
               cost: [],
             },
            },
        )"
        v-if="isSafe"
        :skill="
    {
      id: 'longRest',
      name: 'Long Rest',
      type: 'special',
      icon: null,
      cost: [],
    }
    "
    >
      <img src="@/assets/images/action/long-rest.webp" alt="long rest"
            style="width: 100%; height: 100%; object-fit: contain;"/>
    </SkillIcon>
  </div>
</template>

<script>

import SkillIcon from "@/components/Action/ActionIcon.vue";

export default {
  name: "SpecialSelector",
  components: {SkillIcon},
  props: {
    isSafe: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    selectItem(special) {
      this.$emit("special-selected", special); // Emit event with selected special ID
    },
  },
};
</script>

<style scoped>
.special-selector {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping of icons */
  gap: 0.5rem; /* Space between icons */
  justify-content: flex-start; /* Center icons */
  align-items: flex-start; /* Align icons */
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>
