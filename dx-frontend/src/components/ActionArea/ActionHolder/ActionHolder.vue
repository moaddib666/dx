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
  },
  special: {
    type: Array as () => CharacterItem[],
    default: () => []
  }
});


const MaxSkills = 40;
const MaxItems = 12;
const MaxSpecial = 8;

</script>

<template>
  <div class="action-holder">
    <div class="skills-area">
      <ActionItem
          v-for="skill in skills"
          :key="`skill-${skill.id}`"
          :id="skill.id"
          :image="skill.skill.icon"
          :title="skill.skill.name"
          :ctaType="skill.skill.type"
          @select="applyAction"
          class="cta"
      />
      <ActionItem
          v-for="i in (MaxSkills - skills.length)"
          :key="`empty-skill-${i}`"
          :id="''"
          @select="applyAction"
          class="cta"
      />
    </div>
    <div class="separator"></div>
    <div class="items-area">
      <ActionItem
          v-for="item in items"
          :key="`item-${item.id}`"
          :id="item.id"
          :image="item.world_item.item.icon"
          :title="item.world_item.item.name"
          :ctaType="item.world_item.item.type"
          @select="applyAction"
          class="cta"
      />
      <ActionItem
          v-for="i in (MaxItems - items.length)"
          :key="`empty-item-${i}`"
          :id="''"
          @select="applyAction"
          class="cta"
      />
    </div>
    <div class="separator"></div>
    <div class="items-area-2">
      <ActionItem
          v-for="item in items"
          :key="`item-${item.id}`"
          :id="item.id"
          :image="item.world_item.item.icon"
          :title="item.world_item.item.name"
          :ctaType="item.world_item.item.type"
          @select="applyAction"
          class="cta"
      />
      <ActionItem
          v-for="i in (MaxSpecial - items.length)"
          :key="`empty-item-${i}`"
          :id="''"
          @select="applyAction"
          class="cta"
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
  width: 51.55rem;
  height: 15rem;
}

.cta {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: url("@/assets/images/action-area/Cell.png") no-repeat center center;
  background-size: cover;
  transition: transform 0.2s ease-in-out;
  position: relative;
  color: white;
  margin: 0;
  padding: 0;

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
  width: 9rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-wrap: wrap;
}

.items-area-2 {
  width: 6rem;
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
  z-index: 10;
  margin: 0 -1rem;
}
</style>