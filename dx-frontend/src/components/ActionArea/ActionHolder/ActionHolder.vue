<script setup lang="ts">
import { computed } from 'vue';
import ActionItem from "@/components/ActionArea/ActionItem/ActionItem.vue";
import {OpenaiSkill, SpecialAction, TypeC27Enum, WorldItem} from "@/api/dx-backend";

interface Props {
  skills?: OpenaiSkill[];
  items?: WorldItem[];
  specials?: SpecialAction[];
}

const props = withDefaults(defineProps<Props>(), {
  skills: () => [],
  items: () => [],
  specials: () => []
});

const emit = defineEmits<{
  skillSelected: [skill: OpenaiSkill];
  itemSelected: [item: WorldItem];
  specialSelected: [special: SpecialAction];
}>();

const MAX_SKILLS = 40;
const MAX_ITEMS = 12;
const MAX_SPECIAL = 8;

const emptySkillSlots = computed(() => Math.max(0, MAX_SKILLS - props.skills.length));
const emptyItemSlots = computed(() => Math.max(0, MAX_ITEMS - props.items.length));
const emptySpecialSlots = computed(() => Math.max(0, MAX_SPECIAL - props.specials.length));

const handleSkillAction = (skillId: string) => {
  const skill = props.skills.find(s => s.id.toString() === skillId);
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
  const special = props.specials.find(s => s.action_type === specialType);
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
          :id="skill.id.toString()"
          :image="skill.icon || ''"
          :title="skill.name"
          :cta-type="skill.type || TypeC27Enum.Utility"
          :cost="skill.cost || []"
          @select="() => handleSkillAction(skill.id.toString())"
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
          :image="item.item.icon || ''"
          :title="item.item.name"
          :cta-type="item.item.skill.type || TypeC27Enum.Utility"
          :cost="item.item.skill?.cost || []"
          @select="() => handleItemAction(item.id)"
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
          v-for="specialAction in specials"
          :key="`special-${specialAction.action_type}`"
          :id="specialAction.action_type"
          :image="specialAction.icon || ''"
          :title="specialAction.name || specialAction.action_type"
          :cta-type="TypeC27Enum.Special"
          :cost="specialAction.cost || []"
          @select="() => handleSpecialAction(specialAction.action_type)"
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

.action-holder__item--empty {
  pointer-events: none;
  opacity: 0.3;
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