<script setup lang="ts">
import type {Story} from "@/api/dx-backend";
import RPGStoryTreeChapterItem from "@/components/Story/RPGStoryTreeChapterItem.vue";
import { ref } from 'vue';

interface Props {
  story: Story | null;
  selectedItem: string;
  selected: boolean;
  collapsed: boolean;
}

const props = defineProps<Props>();
const isCollapsed = ref(props.collapsed);

// Toggle collapse state
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

</script>

<template>
  <div class="story-item">
    <div class="story-header" @click="toggleCollapse">
      <div class="story-header-content">
        <img v-if="props.story.image" :src="props.story.image" alt="Story image" class="story-image" />
        <h2 class="story-title">{{ props.story.title }}</h2>
      </div>
    </div>

    <div class="story-chapters" v-if="!isCollapsed">
      <RPGStoryTreeChapterItem
          v-for="chapter in props.story.chapters"
          :key="chapter.id"
          :chapter="chapter"
          :selected="props.selected"
          :collapsed="props.collapsed"
          :selectedItem="props.selectedItem"
      >
      </RPGStoryTreeChapterItem>
    </div>
  </div>
</template>

<style scoped>
.story-item {
  margin-bottom: 1rem;
  border-radius: 6px;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 0.75rem;
  border: 1px solid rgba(216, 187, 124, 0.3);
}

.story-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  cursor: pointer;
}

.story-header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.story-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid rgba(216, 187, 124, 0.5);
  box-shadow: 0 0 8px rgba(216, 187, 124, 0.3);
}

.story-title {
  font-family: var(--font-header);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-gold);
  margin: 0;
  text-shadow: 0 0 8px rgba(216, 187, 124, 0.5);
  transition: text-shadow 0.3s ease;
}

/* Responsive design for smaller containers (30% width) */
@media (max-width: 480px), (max-width: 30vw) {
  .story-item {
    margin-bottom: 0.5rem;
    padding: 0.5rem;
  }

  .story-header {
    margin-bottom: 0.25rem;
  }

  .story-header-content {
    gap: 0.25rem;
  }

  .story-image {
    width: 30px;
    height: 30px;
  }

  .story-title {
    font-size: 1rem;
  }
}

.story-header:hover .story-title {
  text-shadow: 0 0 12px rgba(216, 187, 124, 0.8);
}

.story-status {
  font-family: var(--font-body);
  font-size: 0.75rem;
  font-weight: 400;
  color: #f1c96a;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  background-color: rgba(241, 201, 106, 0.1);
}

.story-progress {
  margin-bottom: 0.75rem;
}

.progress-bar {
  height: 4px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.progress-fill {
  height: 100%;
  background-color: var(--color-gold);
  border-radius: 2px;
}

.progress-label {
  font-family: var(--font-body);
  font-size: 0.65rem;
  color: #ccc;
  text-align: right;
}

.story-chapters {
  margin-top: 0.5rem;
}
</style>