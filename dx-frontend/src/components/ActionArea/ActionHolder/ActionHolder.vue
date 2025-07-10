<script setup lang="ts">
import { computed } from 'vue';
import ActionItem from "@/components/ActionArea/ActionItem/ActionItem.vue";
import {OpenaiSkill, SpecialAction, TypeC27Enum, WorldItem} from "@/api/dx-backend";

interface Props {
  skills?: OpenaiSkill[];
  items?: WorldItem[];
  specials?: SpecialAction[];
  playerService?: any;
}

const props = withDefaults(defineProps<Props>(), {
  skills: () => [],
  items: () => [],
  specials: () => [],
  playerService: null
});

const emit = defineEmits<{
  skillSelected: [skill: OpenaiSkill];
  itemSelected: [item: WorldItem];
  specialSelected: [special: SpecialAction];
}>();

const MAX_SKILLS = 40;
const MAX_ITEMS = 12;
const MAX_SPECIAL = 8;

// Cost validation function for skills
const canPerformSkillAction = (skill: OpenaiSkill): boolean => {
  if (!props.playerService) return true;
  if (!skill.cost || !Array.isArray(skill.cost) || skill.cost.length === 0) return true;

  for (const cost of skill.cost) {
    const currentValue = props.playerService.getCurrentAttributeValue(cost.kind);
    if (currentValue === null || currentValue < cost.value) {
      return false;
    }
  }
  return true;
};

// Cost validation function for items
const canPerformItemAction = (item: WorldItem): boolean => {
  if (!props.playerService || !item.item || !item.item.skill) return true;

  const skill = item.item.skill;
  if (!skill.cost || !Array.isArray(skill.cost) || skill.cost.length === 0) return true;

  for (const cost of skill.cost) {
    const currentValue = props.playerService.getCurrentAttributeValue(cost.kind);
    if (currentValue === null || currentValue < cost.value) {
      return false;
    }
  }
  return true;
};

// Cost validation function for special actions
const canPerformSpecialAction = (special: SpecialAction): boolean => {
  if (!props.playerService) return true;
  if (!special.cost || !Array.isArray(special.cost) || special.cost.length === 0) return true;

  for (const cost of special.cost) {
    const currentValue = props.playerService.getCurrentAttributeValue(cost.kind);
    if (currentValue === null || currentValue < cost.value) {
      return false;
    }
  }
  return true;
};

// Filter items to only show those with charges > 0
const filteredItems = computed(() => {
  return props.items.filter(item => {
    // Check if item has charges_left property and it's > 0
    return item.charges_left > 0;
  });
});

const emptySkillSlots = computed(() => Math.max(0, MAX_SKILLS - props.skills.length));
const emptyItemSlots = computed(() => Math.max(0, MAX_ITEMS - filteredItems.value.length));
const emptySpecialSlots = computed(() => Math.max(0, MAX_SPECIAL - props.specials.length));

const handleSkillAction = (skillId: string) => {
  const skill = props.skills.find(s => s.id.toString() === skillId);
  if (skill && canPerformSkillAction(skill)) {
    emit('skillSelected', skill);
  }
};

const handleItemAction = (itemId: string) => {
  const item = filteredItems.value.find(i => i.id === itemId);
  if (item && canPerformItemAction(item)) {
    emit('itemSelected', item);
  }
};

const handleSpecialAction = (specialType: string) => {
  const special = props.specials.find(s => s.action_type === specialType);
  if (special && canPerformSpecialAction(special)) {
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
          :disabled="!canPerformSkillAction(skill)"
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
          v-for="item in filteredItems"
          :key="`item-${item.id}`"
          :id="item.id"
          :image="item.item.icon || ''"
          :title="item.item.name"
          :cta-type="item.item.skill.type || TypeC27Enum.Utility"
          :cost="item.item.skill?.cost || []"
          :disabled="!canPerformItemAction(item)"
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
          :disabled="!canPerformSpecialAction(specialAction)"
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
  align-items: flex-start;
  justify-content: flex-start;
  position: relative;
  flex-wrap: wrap;
}

.action-holder__items {
  width: 9rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  position: relative;
  flex-wrap: wrap;
}

.action-holder__special {
  width: 6rem;
  height: 12.6rem;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
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