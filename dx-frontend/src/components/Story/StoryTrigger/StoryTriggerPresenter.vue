<script setup lang="ts">
import {GameObject, Trigger, TriggerTypeEnum} from "@/api/dx-backend";
import DXCell from "@/components/DXCell.vue";
import {computed, ref} from "vue";

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
  (id: any): TriggerTarget;
}

// Character TemplateResolver - Placeholder for actual character template resolver
// TODO: implement real one useing the GMCharacterTemplateService
const characterTemplateResolver: triggerTargetResolver = (id) => {
  return {
    id,
    title: `Target ${id}`,
    image: `https://example.com/target-${id}.png`,
    name: `Target Name ${id}`,
    description: `Description for target ${id}`
  };
};

// GameObject Resolver - Placeholder for actual game object resolver
const gameObjectResolver: triggerTargetResolver = (id) => {
  // TODO: not implemented yet on backend side skip for now
  return {
    id,
    title: `GameObject ${id}`,
    image: `https://example.com/gameobject-${id}.png`,
    name: `GameObject Name ${id}`,
    description: `Description for GameObject ${id}`
  };
};

// Item Resolver - Placeholder for actual item resolver
// FIXME: implement real one using the ItemsService
const itemResolver: triggerTargetResolver = (id) => {
  return {
    id,
    title: `Item ${id}`,
    image: `https://example.com/item-${id}.png`,
    name: `Item Name ${id}`,
    description: `Description for Item ${id}`
  };
};

// Skill Resolver - Placeholder for actual skill resolver
const skillResolver: triggerTargetResolver = (id) => {
  return {
    id,
    title: `Skill ${id}`,
    image: `https://example.com/skill-${id}.png`,
    name: `Skill Name ${id}`,
    description: `Description for Skill ${id}`
  };
};

// Position Resolver - Placeholder for actual position resolver
const positionResolver: triggerTargetResolver = (id) => {
  return {
    id,
    title: `Position ${id}`,
    image: `https://example.com/position-${id}.png`,
    name: `Position Name ${id}`,
    description: `Description for Position ${id}`
  };
};

// Location Resolver - Placeholder for actual location resolver
const locationResolver: triggerTargetResolver = (id) => {
  return {
    id,
    title: `Location ${id}`,
    image: `https://example.com/location-${id}.png`,
    name: `Location Name ${id}`,
    description: `Description for Location ${id}`
  };
};

const triggerResolvers: Record<TriggerTypeEnum, triggerTargetResolver> = {
  [TriggerTypeEnum.Kill]: characterTemplateResolver,
  [TriggerTypeEnum.Search]: gameObjectResolver,
  [TriggerTypeEnum.UseItem]: itemResolver,
  [TriggerTypeEnum.UseSkill]: skillResolver,
  [TriggerTypeEnum.Position]: positionResolver,
  [TriggerTypeEnum.Interaction]: characterTemplateResolver,
  [TriggerTypeEnum.Custom]: (id) => ({
    id,
    title: `Custom Trigger ${id}`,
    image: `https://example.com/custom-${id}.png`,
    name: `Custom Name ${id}`,
    description: `Description for Custom Trigger ${id}`
  })
};


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