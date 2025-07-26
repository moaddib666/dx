<script setup lang="ts">
import {Condition} from "@/api/dx-backend";
import StoryTriggerPresenter from "@/components/Story/StoryTrigger/StoryTriggerPresenter.vue";

interface Props {
  condition: Condition;
}
const props = defineProps<Props>();
</script>

<template>
  <div class="condition">
    <div class="condition-header">
      <div class="condition-type">{{ props.condition.type }}</div>
    </div>
    <div class="condition-content">
      <StoryTriggerPresenter v-for="trigger in props.condition.triggers"
                             :key="trigger.id"
                             :trigger="trigger">
      </StoryTriggerPresenter>
    </div>
  </div>
</template>

<style scoped>
/* Import the same fonts as in the parent components */
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Inter&family=Source+Code+Pro&display=swap');

.condition {
  position: relative;
  margin: 0.5rem 0;
  font-family: 'Cinzel', serif;
  color: #d6b97b;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}

.condition-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  width: 100%;
}

.condition-type {
  background-color: #1a1c1f;
  color: #d6b97b;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 0.9rem;
  border: 1px solid #d6b97b;
  text-shadow: 0 0 4px rgba(214, 185, 123, 0.3);
  font-weight: bold;
}

.condition-content {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  width: 100%;
  border-left: 2px solid #d6b97b;
  padding-left: 0.5rem;
}
</style>