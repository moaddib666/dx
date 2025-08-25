<script setup lang="ts">

import CharacterSelectorCircle from "@/components/Character/CharacterSelectorCircle.vue";
import RPGCell from "@/components/RPGGrid/RPGCell.vue";

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
  initiatorId?: Participant;
  targetId?: Participant;
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
</script>

<template>
  <div class="container">
    <CharacterSelectorCircle
        :selected-character-id="props.initiatorId"
        @select="emit('selectInitiator', props.initiatorId)"/>
    <RPGCell class="action-cell" @click="emit('selectAction', props.action)">
      <p>Select</p>
    </RPGCell>
    <CharacterSelectorCircle
        :selected-character-id="props.targetId"
        @select="emit('selectTarget', props.targetId)"
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
  padding: 1rem;
  height: 90%;
  aspect-ratio: 1 / 1;
  text-align: center;
  cursor: pointer;
}
</style>