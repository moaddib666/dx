<script setup lang="ts">
import { computed } from 'vue';
import ActionItem from "@/components/ActionArea/ActionItem/ActionItem.vue";
import { CharacterItem, LearnedSkill, SpecialAction, TypeC27Enum } from "@/api/dx-backend";

interface Props {
  skills?: LearnedSkill[];
  items?: CharacterItem[];
  special?: SpecialAction[];
}

const props = withDefaults(defineProps<Props>(), {
  skills: () => [],
  items: () => [],
  special: () => []
});

const emit = defineEmits<{
  skillSelected: [skill: LearnedSkill];
  itemSelected: [item: CharacterItem];
  specialSelected: [special: SpecialAction];
}>();

const MAX_SKILLS = 40;
const MAX_ITEMS = 12;
const MAX_SPECIAL = 8;

const emptySkillSlots = computed(() => Math.max(0, MAX_SKILLS - props.skills.length));
const emptyItemSlots = computed(() => Math.max(0, MAX_ITEMS - props.items.length));
const emptySpecialSlots = computed(() => Math.max(0, MAX_SPECIAL - props.special.length));

const handleSkillAction = (skillId: string) => {
  const skill = props.skills.find(s => s.id === skillId);
  if (skill) {
    emit('skillSelected', skill);
  }
};

const handleItemAction = (itemId: string) => {
  const item = props.items.find(i => i.id === itemId);
  if (item) {
    emit('itemSelected', item);
  }
};

const handleSpecialAction = (specialType: string) => {
  const special = props.special.find(s => s.action_type === specialType);
  if (special) {
    emit('specialSelected', special);
  }
};

</script>

<template>
  <div class="action-holder">
    <div class="action-holder__skills">
      <ActionItem
          v-for="skill in skills"
          :key="`skill-${skill.id}`"
          :id="skill.id"
          :image="skill.skill.icon || ''"
          :title="skill.skill.name"
          :cta-type="skill.skill.type || TypeC27Enum.Utility"
          @select="() => handleSkillAction(skill.id)"
          class="action-holder__item"
      />
      <ActionItem
          v-for="i in emptySkillSlots"
          :key="`empty-skill-${i}`"
          :id="''"
          class="action-holder__item action-holder__item--empty"
      />
    </div>

    <div class="action-holder__separator"></div>

    <div class="action-holder__items">
      <ActionItem
          v-for="item in items"
          :key="`item-${item.id}`"
          :id="item.id"
          :image="item.world_item.item.icon || ''"
          :title="item.world_item.item.name"
          :cta-type="item.world_item.item.type || TypeC27Enum.Utility"
          @select="() => handleItemAction(item.id)"
          class="action-holder__item"
      />
      <ActionItem
          v-for="i in emptyItemSlots"
          :key="`empty-item-${i}`"
          :id="''"
          class="action-holder__item action-holder__item--empty"
      />
    </div>

    <div class="action-holder__separator"></div>

    <div class="action-holder__special">
      <ActionItem
          v-for="specialAction in special"
          :key="`special-${specialAction.action_type}`"
          :id="specialAction.action_type"
          :image="specialAction.icon || ''"
          :title="specialAction.name || specialAction.action_type"
          :cta-type="TypeC27Enum.Special"
          @select="() => handleSpecialAction(specialAction.action_type)"
          class="action-holder__item"
      />
      <ActionItem
          v-for="i in emptySpecialSlots"
          :key="`empty-special-${i}`"
          :id="''"
          class="action-holder__item action-holder__item--empty"
      />
    </div>
  </div>
</template>

<style scoped>
.action-holder {
  z-index: 1000;
  position: fixed;
  bottom: 0;
  background: url("@/assets/images/action-area/Area.png") no-repeat center center;
  background-size: cover;
  display: flex;
  flex: 1;
  flex-direction: row;
  align-items: flex-end;
  justify-content: center;
  width: 51.75rem;
  height: 15.7rem;
  padding-bottom: 0.5rem;
}

.action-holder__item {
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

.action-holder__item--empty {
  pointer-events: none;
}

.action-holder__skills {
  width: 30rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-wrap: wrap;
}

.action-holder__items {
  width: 9rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-wrap: wrap;
}

.action-holder__special {
  width: 6rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-wrap: wrap;
}

.action-holder__separator {
  background: url("@/assets/images/action-area/Delimiter.png") no-repeat center center;
  background-size: cover;
  width: 3rem;
  height: 12.6rem;
  z-index: 10;
  margin: 0 -1rem;
}
</style>