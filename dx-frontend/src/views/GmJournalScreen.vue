<script setup lang="ts">
import RPGTrigger from "@/components/RPGTrigger/RPGTrigger.vue";
import GMRPGItems from "@/components/GameMaster/RPGItems/GMRPGItems.vue";
import GMRPGCharacterTemplate from "@/components/GameMaster/RPGCharacterTempaltes/GMRPGCharacterTemplate.vue";
import GMRPGSkills from "@/components/GameMaster/RPGSkills/GMRPGSkills.vue";
import RPGStoryTree from "@/components/Story/StoryTree/RPGStoryTree.vue";
import {computed, onMounted, ref} from "vue";
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue";
import RPGStoryQuestView from "@/components/Story/StoryTeller/RPGStoryQuestView.vue";
import {gmStories} from "@/services/GMStories";
import {Quest} from "@/api/dx-backend";
import characterTemplatesService from "@/services/CharacterTemplatesService";
import skillService from "@/services/skillService";
import {itemsService} from "@/services/ItemsService";

// Add a loading state to track initialization
const isLoading = ref(true);

// Initialize the stories service before rendering
onMounted(async () => {
    try {
        await gmStories.ensureInitialized();
        await characterTemplatesService.initialize();
        await skillService.updateAllCaches();
        await itemsService.refresh();
        isLoading.value = false;
    } catch (error) {
        console.error('Failed to initialize stories:', error);
        isLoading.value = false;
    }
});

const stories = computed(
    () => gmStories.getStories()
)

// State for the selected quest
const selectedQuest = ref<Quest | null>(null);

// Take first quest for the first story first chapter as default
// This will be used if no quest is selected
const defaultQuest = computed(() => {
  if (stories.value.length > 0 && stories.value[0].chapters.length > 0 && stories.value[0].chapters[0].quests.length > 0) {
    return stories.value[0].chapters[0].quests[0];
  }
  return null;
});

// Use the selected quest or fall back to the default quest
const quest = computed(() => {
  return selectedQuest.value || defaultQuest.value;
});

// Get the chapter for the selected quest
const chapter = computed(() => {
  if (quest.value) {
    return gmStories.getChapterForQuest(quest.value.id);
  }
  return null;
});

// Get the story for the selected quest
const story = computed(() => {
  if (quest.value) {
    return gmStories.getStoryForQuest(quest.value.id);
  }
  return null;
});

// Handle quest selection
const handleQuestSelect = (quest: Quest) => {
  selectedQuest.value = quest;
  console.log('Selected quest:', quest.title);
};

</script>

<template>
  <HeroBackground id="story-trailer"></HeroBackground>

  <!-- Loading indicator while stories are being initialized -->
  <div v-if="isLoading" class="loading-container">
    <div class="loading-spinner"></div>
    <p>Loading stories...</p>
  </div>

  <!-- Main content only shown after initialization is complete -->
  <div v-else class="test-screen">
    <div class="right-bar">
      <RPGStoryTree
        :written-stories="stories"
        :selected-quest-id="selectedQuest?.id"
        @select-quest="handleQuestSelect"
      ></RPGStoryTree>
    </div>
    <div class="left-container">
      <div v-if="quest" class="quest-container">
        <RPGStoryQuestView
            :quest="quest"
            :chapter="chapter"
            :story="story"
        ></RPGStoryQuestView>
      </div>
      <div v-else class="no-quest-message">
        <h2>No Quest Selected</h2>
        <p>Please select a quest from the journal to view its details.</p>
      </div>
    </div>
    <!--    <div class="triggers-container">-->
    <!--      <RPGTrigger v-for="i in 4" :key="i" />-->
    <!--      <GMRPGItems :isDraggable="true" v-if="false" />-->
    <!--      <GMRPGCharacterTemplate :isDraggable="true" v-if="false"  />-->
    <!--      <GMRPGSkills :isDraggable="true" v-if="false"  />-->
    <!--    </div>-->
  </div>
</template>

<style scoped>
.test-screen {
  padding: 2em;
  display: flex;
  flex-direction: row;
  width: 100%;
  height: calc(100vh - 4em);
}

.right-bar {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 4em);
  overflow-y: auto;
  flex: 1; /* Changed from 1 to 3 to make it exactly 30% (3/10) */
}

.left-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 4em);
  overflow-y: auto;
  padding-left: 2em;
  flex: 3; /* Changed from 3 to 7 to make right-bar exactly 30% (3/10) */
}

.triggers-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6em 4em;
  width: fit-content;
  margin: 0 auto;
}

/* Loading indicator styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 4em);
  width: 100%;
  padding: 2em;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1em;
}

/* No quest message styles */
.no-quest-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 2em;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 1px solid rgba(216, 187, 124, 0.3);
}

.no-quest-message h2 {
  font-family: 'Cinzel', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #fada95;
  margin-bottom: 1rem;
}

.no-quest-message p {
  font-family: 'Inter', sans-serif;
  font-size: 1.2rem;
  color: #ffffff;
  max-width: 500px;
}

.quest-container {
  width: 100%;
  height: 100%;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

#story-trailer {
  background-image: url('@/assets/images/backgrounds/library.png');
}

</style>