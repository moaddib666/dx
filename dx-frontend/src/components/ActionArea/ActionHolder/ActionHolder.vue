<script setup lang="ts">

import ActionItem from "@/components/ActionArea/ActionItem/ActionItem.vue";
import {CharacterItem, LearnedSkill} from "@/api/dx-backend";

const applyAction = (action: string) => {
  console.log("Action selected:", action);
};


const props = defineProps({
  skills: {
    type: Array as () => LearnedSkill[],
    default: () => []
  },
  items: {
    type: Array as () => CharacterItem[],
    default: () => []
  }
});


const MaxSkills = 40;
const MaxItems = 20;

</script>

<template>
  <div class="action-holder">
    <div class="skills-area">
      <ActionItem
          v-for="i in MaxSkills"
          :key="`skill-${i}`"
          @select="applyAction"
      />
    </div>
    <div class="separator"></div>
    <div class="items-area">
      <ActionItem
          v-for="i in MaxItems"
          :key="`item-${i}`"
          :id="123"
          image="@/assets/images/action/anomaly.png"
          @select="applyAction"
      />
    </div>

  </div>
</template>

<style scoped>
.action-holder {
  z-index: 1000;
  position: fixed;
  bottom: 0;
  background: url("@/assets/images/action-area/Area.png");
  background-size: cover;
  display: flex;
  flex: 1;
  flex-direction: row;
  align-items: flex-end;
  justify-content: center;
  width: 50.25rem;
  height: 15rem;
}

.skills-area {
  width: 30rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-wrap: wrap;
}

.items-area {
  width: 15rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-wrap: wrap;
}

.separator {
  background: url("@/assets/images/action-area/Delimiter.png");
  background-size: cover;
  background-repeat: no-repeat;
  width: 3rem;
  height: 12.6rem;
  left: 33rem;
  z-index: 1000;
  margin: 0 -1rem;
}
</style>