<script setup lang="ts">

import CharacterSelectorCircle from "@/components/Character/CharacterSelectorCircle.vue";
import RPGCell from "@/components/RPGGrid/RPGCell.vue";
import ActionPlaceholder from "@/assets/images/action/placeholder.png"
import {computed} from "vue";
import skillService from "@/services/skillService.ts";
import {itemsService} from "@/services/ItemsService.ts";
interface Action {
  skillId?: string;
  itemId?: string;
}

interface Participant {
  id: string;
  name?: string;
  imageUrl?: string;
}

interface Props {
  initiator?: Participant;
  target?: Participant;
  action?: Action;
}

const emit = defineEmits(
    {
      selectInitiator: (participant: Participant | undefined) => true,
      selectTarget: (participant: Participant | undefined) => true,
      selectAction: (action: Action | undefined) => true,
    }
);

const props = withDefaults(defineProps<Props>(), {
  initiatorId: undefined,
  targetId: undefined,
  action: undefined,
});

const skill = computed(() => {
  if (props.action?.skillId) {
    return skillService.getSkill(parseInt(props.action.skillId));
  }
  return null;
});

const item = computed(() => {
  if (props.action?.itemId) {
    return itemsService.getItemById(props.action.itemId);
  }
  return null;
});

const actionImageUrl = computed(() => {
  // If we have a skill, use its icon
  if (skill.value?.icon) {
    return skill.value.icon;
  }

  // If we have an item, use its icon
  if (item.value?.icon) {
    return item.value.icon;
  }

  // If we have an action but no icon, use default skill icon
  if (props.action) {
    return "@/assets/images/skill/default.webp";
  }

  // No action, use placeholder
  return ActionPlaceholder;
});
</script>

<template>
  <div class="container">
    <CharacterSelectorCircle
        :participant="props.initiator"
        @select="emit('selectInitiator', $event)"/>
    <RPGCell
        class="action-cell"
        :class="{'placeholder': !props.action}"
        @click="emit('selectAction', props.action)">
      <img :src="actionImageUrl" class="action-image"  alt="Action"/>
    </RPGCell>
    <CharacterSelectorCircle
        :participant="props.target"
        @select="emit('selectTarget', $event)"
    />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  gap: 2rem;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  min-height: 7rem;
}

.action-cell {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.3rem;
  aspect-ratio: 1 / 1;
  text-align: center;
  cursor: pointer;
}
.action-image {
  height: 3em;
  object-fit: contain;
  mask: radial-gradient(circle, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0) 100%);
  mask-repeat: no-repeat;
  mask-size: contain;
  transform: scale(0.9);
  filter: brightness(0.8);
}
.action-image:hover {
  transform: scale(1);
  transition: transform 0.2s ease;
  filter: brightness(1);
}
.action-image:active {
  transform: scale(0.95);
  transition: transform 0.1s ease;
  filter: brightness(0.9);
}

.action-cell.placeholder {
  filter: grayscale(100%);
}
.action-cell:hover {
  filter: grayscale(0.5);
}
</style>