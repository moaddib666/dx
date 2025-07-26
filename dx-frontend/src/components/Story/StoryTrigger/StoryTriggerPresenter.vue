<script setup lang="ts">
import {Trigger} from "@/api/dx-backend";
import DXCell from "@/components/DXCell.vue";
import {itemsService} from '@/services/ItemsService';
import {characterTemplatesService} from '@/services/CharacterTemplatesService';

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
    description: itemInstance.description,
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
  return {
    id: trigger.npc,
    title: npcInstance.name,
    image: npcInstance.bio.avatar,
    description: npcInstance.bio.background,
  } as TriggerTarget;
}

</script>

<template>
  <div class="trigger-item">
    <div class="trigger-type-label">{{ formattedTriggerType }}</div>
    <div class="trigger-content">
      <DXCell
          :image="triggerImage"
          :title="triggerTitle"
          :subtitle="triggerSubtitle"
      />
    </div>
  </div>
</template>

<style scoped>
.trigger-item {
  position: relative;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.trigger-type-label {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #1a1c1f;
  color: #d6b97b;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  z-index: 2;
  border: 1px solid #d6b97b;
}

.trigger-content {
  width: 100%;
  height: 100%;
  min-height: 120px;
}
</style>