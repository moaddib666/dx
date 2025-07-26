<script setup lang="ts">
import type {Chapter, Quest, Story} from '@/api/dx-backend';
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import {computed} from "vue";
import {gmStories} from "@/services/GMStories";
import StoryConditionPresenter from "@/components/Story/StoryTrigger/StoryConditionPresenter.vue";

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
      <h3 v-if="chapter?.title"> {{ chapter.title }}</h3>
      <h2>
        {{ props.quest.title }}
      </h2>
    </div>
    <div class="content">
      <div class="main-content">
        <p v-if="props.quest.description">{{ props.quest.description }}</p>
      </div>
      <div class="quest-starters">
        <h4 v-if="props.quest.starters && props.quest.starters.length > 0">Quest Starters:</h4>
        <StoryConditionPresenter v-for="starter in props.quest.starters"
                                 :key="starter.id"
                                 :condition="starter">
        </StoryConditionPresenter>
      </div>
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
  height: 25vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 2rem;
  flex-direction: column;
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
  filter: shadow(0 0 10px rgba(0, 0, 0, 0.5));
}

.hero-section h2 {
  position: relative;
  z-index: 1;
  font-family: 'Cinzel', serif;
  font-size: 2.25rem;
  font-weight: 700;
  color: #fada95;
  text-transform: uppercase;
  margin-bottom: 1rem;
  text-align: center;
  text-shadow: 0 0 8px rgba(216, 187, 124, 0.5);
  filter: drop-shadow(0 0.2rem rgba(0, 0, 0, 0.6)) drop-shadow(0 0.1rem rgba(0, 0, 0, 0.4));
  transition: text-shadow 0.3s ease;
}

.hero-section h3,
.hero-section h4 {
  position: relative;
  z-index: 1;
  font-family: 'Inter', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0.5rem 0;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.3);
  filter: drop-shadow(0 0.1rem rgba(0, 0, 0, 0.6)) drop-shadow(0 0.05rem rgba(0, 0, 0, 0.4));
}

.content {
  padding: 1.5rem;
  color: #bcbbbb;
  font-family: 'Inter', sans-serif;
  font-size: 1.2rem;
}

</style>