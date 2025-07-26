<script setup lang="ts">
import type {Chapter, Quest, Story} from '@/api/dx-backend';
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import {computed} from "vue";
import {gmStories} from "@/services/GMStories";

interface Props {
  quest: Quest;
}

const props = defineProps<Props>();

// use the provided chapter prop or fall back to gmStories
const chapter = computed<Chapter | undefined>(() => {
  return gmStories.getChapterForQuest(props.quest.id);
});

// use the provided story prop or fall back to gmStories
const story = computed<Story | undefined>(() => {
  return gmStories.getStoryForQuest(props.quest.id);
});

</script>

<template>
  <RPGContainer class="container">
    <div class="hero-section">
      <div class="background--holder">
        <img v-if="props.quest?.image" :src="props.quest.image" alt="Quest background" class="background-image"/>
        <img v-else-if="chapter?.image" :src="chapter.image" alt="Chapter background" class="background-image"/>
        <img v-else-if="story?.image" :src="story.image" alt="Story background" class="background-image"/>
      </div>
      <h2>
        {{ props.quest.title }}
      </h2>
    </div>
  </RPGContainer>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem;
  width: 100%;
  height: 100%;
}

.hero-section {
  position: relative;
  width: 100%;
  height: 40vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.background--holder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.hero-section h2 {
  position: relative;
  z-index: 1;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  background-color: rgba(0, 0, 0, 0.5);
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

</style>