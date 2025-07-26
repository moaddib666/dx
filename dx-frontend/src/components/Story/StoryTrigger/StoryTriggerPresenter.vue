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

</script>

<template>
  <div class="trigger-item">
    <div class="trigger-type-label">{{ props.trigger.type }}</div>
    <div class="trigger-description"> {{ props.trigger.description }} </div>
    <div class="trigger-content">
      <DXCell  v-if="triggerTarget !== null"
          :image="triggerTarget.image"
          :title="triggerTarget.title"
          :subtitle="triggerTarget.description"

      />
      <div v-else class="trigger-content-placeholder">
<!--          FIXME: represent trigger targets in text if they exists byt we just can't resolve it well -->
      </div>
    </div>
  </div>
</template>

<style scoped>
.trigger-item {
  position: relative;
  margin: 0 auto;
}

.trigger-type-label {
  position: absolute;
  top: -10px;
  background-color: #1a1c1f;
  color: #d6b97b;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  z-index: 2;
  border: 1px solid #d6b97b;
}

.trigger-content {
  width: 5rem;
  height: 5rem;
}
</style>