<script setup lang="ts">
import {Trigger} from "@/api/dx-backend";
import DXCell from "@/components/DXCell.vue";
import {itemsService} from '@/services/ItemsService';
import {characterTemplatesService} from '@/services/CharacterTemplatesService';
import skillService from "@/services/skillService";
import {computed} from "vue";

// Import trigger icons
interface Props {
  trigger: Trigger;
}

interface TriggerTarget {
  id: string | number;
  title?: string;
  image?: string;
  name?: string;
  description?: string;
}

const props = defineProps<Props>();

interface triggerTargetResolver {
  (t: Trigger): TriggerTarget | null;
}

const itemTargetResolver: triggerTargetResolver = (trigger: Trigger) => {
  if (!trigger.item) {
    return null;
  }

  const itemInstance = itemsService.getItemById(trigger.item);
  if (!itemInstance) {
    return null;
  }
  return {
    id: trigger.item,
    title: itemInstance.name,
    image: itemInstance.icon,
    description: "",
  } as TriggerTarget;
}

const npcTargetResolver: triggerTargetResolver = (trigger: Trigger) => {
  if (!trigger.npc) {
    return null;
  }

  const npcInstance = characterTemplatesService.getTemplateById(trigger.npc);
  if (!npcInstance) {
    return null;
  }

  console.warn('NPC Trigger Target Resolver', {npcInstance});
  return {
    id: trigger.npc,
    title: npcInstance.name,
    image: npcInstance.avatar || "",
    description: "",
  } as TriggerTarget;
}

const skillTargetResolver: triggerTargetResolver = (trigger: Trigger) => {
  if (!trigger.skill) {
    return null;
  }

  const skillInstance = skillService.getSkill(trigger.skill);
  if (!skillInstance) {
    console.warn('Skill Trigger Target Resolver: Skill not found', {skillId: trigger.skill});
    return null;
  }
  console.debug('Skill Trigger Target Resolver', {skillInstance});
  return {
    id: trigger.skill,
    title: skillInstance.name,
    image: skillInstance.icon,
    description: skillInstance.description,
  } as TriggerTarget;
}

const resolvers: triggerTargetResolver[] = [
  itemTargetResolver,
  npcTargetResolver,
  skillTargetResolver,
];

const triggerTarget = computed((): TriggerTarget | null => {
  for (const resolver of resolvers) {
    const target = resolver(props.trigger);
    if (target) {
      return target;
    }
  }
  return null;
});

// Determine if we have a trigger ID but couldn't resolve it
const hasUnresolvedTrigger = computed((): boolean => {
  return triggerTarget.value === null &&
    (props.trigger.item !== undefined ||
     props.trigger.npc !== undefined ||
     props.trigger.skill !== undefined);
});

// Get text representation for unresolved trigger
const unresolvedTriggerText = computed((): string => {
  if (props.trigger.item) {
    return `Item ID: ${props.trigger.item}`;
  }
  if (props.trigger.npc) {
    return `NPC ID: ${props.trigger.npc}`;
  }
  if (props.trigger.skill) {
    return `Skill ID: ${props.trigger.skill}`;
  }
  return "Unknown trigger";
});

</script>

<template>
  <div class="trigger-item">
    <div class="trigger-header">
      <span class="trigger-type-label">{{ props.trigger.type }}</span>
      <span class="trigger-description">{{ props.trigger.description }}</span>
    </div>
    <div class="trigger-content">
      <DXCell v-if="triggerTarget !== null"
          :image="triggerTarget.image"
          :title="triggerTarget.title"
          :subtitle="triggerTarget.description"
      />
      <div v-else-if="hasUnresolvedTrigger" class="trigger-content-placeholder">
        <div class="placeholder-icon">?</div>
        <div class="placeholder-text">{{ unresolvedTriggerText }}</div>
      </div>
      <div v-else class="trigger-content-placeholder">
        <div class="placeholder-icon">!</div>
        <div class="placeholder-text">No target</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Import the same fonts as in the parent components */
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Inter&family=Source+Code+Pro&display=swap');

.trigger-item {
  position: relative;
  font-family: 'Cinzel', serif;
  color: #d6b97b;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.trigger-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.2rem;
  width: 100%;
}

.trigger-type-label {
  background-color: #1a1c1f;
  color: #d6b97b;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 0.75rem;
  border: 1px solid #d6b97b;
  text-shadow: 0 0 4px rgba(214, 185, 123, 0.3);
  font-weight: bold;
  margin-right: 0.5rem;
}

.trigger-description {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  color: #bcbbbb;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.trigger-content {
  width: 5rem;
  height: 5rem;
  border: 0.15rem solid transparent;
  border-image-slice: 60 60 60 60;
  border-image-width: 10px 10px 10px 10px;
  border-image-outset: 0px 0px 0px 0px;
  border-image-repeat: stretch stretch;
  border-image-source: url("@/assets/images/border/borderassets.png");
  position: relative;
  align-self: flex-start;
}

.trigger-content-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #1a1c1f;
  color: #d6b97b;
  text-align: center;
  padding: 0.15rem;
}

.placeholder-icon {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.15rem;
  font-family: 'Cinzel', serif;
  text-shadow: 0 0 4px rgba(214, 185, 123, 0.5);
}

.placeholder-text {
  font-family: 'Source Code Pro', monospace;
  font-size: 0.6rem;
  opacity: 0.9;
  word-break: break-word;
  max-width: 100%;
}
</style>