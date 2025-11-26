<script setup lang="ts">
import { ref } from 'vue';
import StoryTriggerPresenter from '@/components/Story/StoryTrigger/StoryTriggerPresenter.vue';
import { TriggerTypeEnum } from '@/api/dx-backend';

// Example trigger data for different trigger types
const exampleTriggers = ref([
  {
    id: '1',
    type: TriggerTypeEnum.Kill,
    description: 'Defeat the dragon to complete the quest',
    npc: 'Dragon',
    game_object: null,
    position: null,
    location: null,
    skill: null,
    item: null
  },
  {
    id: '2',
    type: TriggerTypeEnum.UseItem,
    description: 'Use the magic key to unlock the ancient door',
    npc: null,
    game_object: null,
    position: null,
    location: null,
    skill: null,
    item: 'Magic Key'
  },
  {
    id: '3',
    type: TriggerTypeEnum.UseSkill,
    description: 'Use your lockpicking skill to open the treasure chest',
    npc: null,
    game_object: null,
    position: null,
    location: null,
    skill: 'Lockpicking',
    item: null
  },
  {
    id: '4',
    type: TriggerTypeEnum.Position,
    description: 'Reach the mountain peak to discover a hidden treasure',
    npc: null,
    game_object: null,
    position: 'Mountain Peak',
    location: null,
    skill: null,
    item: null
  },
  {
    id: '5',
    type: TriggerTypeEnum.Search,
    description: 'Search the abandoned house for clues',
    npc: null,
    game_object: null,
    position: null,
    location: 'Abandoned House',
    skill: null,
    item: null
  }
]);
</script>

<template>
  <div class="example-container">
    <h1>Story Trigger Examples</h1>
    <p>Below are examples of different types of story triggers:</p>

    <div class="triggers-grid">
      <div v-for="trigger in exampleTriggers" :key="trigger.id" class="trigger-example">
        <StoryTriggerPresenter :trigger="trigger" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.example-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Cinzel', serif;
  color: #d6b97b;
}

h1 {
  text-align: center;
  margin-bottom: 1rem;
}

p {
  text-align: center;
  margin-bottom: 2rem;
}

.triggers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.trigger-example {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>