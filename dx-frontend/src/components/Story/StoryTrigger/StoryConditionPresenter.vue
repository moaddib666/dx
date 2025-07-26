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
    <div class="label">
      {{ props.condition.type }}
    </div>
    <div class="content">
      <StoryTriggerPresenter v-for="trigger in props.condition.triggers"
                             :key="trigger.id"
                             :trigger="trigger">
      </StoryTriggerPresenter>
    </div>
  </div>
</template>

<style scoped>

</style>