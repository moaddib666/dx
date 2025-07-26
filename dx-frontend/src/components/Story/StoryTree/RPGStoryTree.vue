<script setup lang="ts">
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import type {Story, Quest} from "@/api/dx-backend";
import RpgStoryTreeItem from "@/components/Story/StoryTree/RPGStoryTreeItem.vue";

interface Props {
  writtenStories: Story[];
}

const props = defineProps<Props>();
const emit = defineEmits(['select-quest']);

// Forward the select-quest event from child story items
const handleQuestSelect = (quest: Quest) => {
  emit('select-quest', quest);
};

</script>

<template>
  <RPGContainer class="rpg-story-tree">
    <h1 class="global-header">JOURNAL</h1>
    <div class="scrollable-content">
        <RpgStoryTreeItem
            v-for="story in props.writtenStories"
            :key="story.id"
            :story="story"
            :selectedItem="''"
            :selected="false"
            :collapsed="true"
            @select-quest="handleQuestSelect"
        >
        </RpgStoryTreeItem>
    </div>
  </RPGContainer>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

.rpg-story-tree {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  color: #ffffff;
}

.global-header {
  font-family: 'Cinzel', serif;
  font-size: 2.25rem;
  font-weight: 700;
  color: #fada95;
  text-transform: uppercase;
  margin-bottom: 1rem;
  text-align: center;
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 1rem;
}

/* Responsive design for smaller containers (30% width) */
@media (max-width: 480px), (max-width: 30vw) {
  .global-header {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .scrollable-content {
    padding: 0 0.5rem;
  }
}

/* Global font variables */
:root {
  --font-header: 'Cinzel', 'Trajan Pro', serif;
  --font-body: 'Inter', 'Helvetica Neue', sans-serif;

  /* Status colors */
  --color-active: #4fd1ff;
  --color-completed: #00ffaa;
  --color-locked: #ff4444;
  --color-available: #dddddd;

  /* Theme colors */
  --color-gold: #d8bb7c;
  --color-silver-gold: #99988a;
}
</style>