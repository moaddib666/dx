<script setup lang="ts">
import {defineProps, withDefaults} from 'vue';
import {CharacterActionLog} from '@/api/dx-backend/api';

const props = withDefaults(defineProps<{
  actions: Array<CharacterActionLog>
}>(), {
  actions: () => ([])
});

</script>

<template>
  <div class="action-log--container">
    <div class="action-log--content">
      <ul>
        <li v-for="(action, index) in actions" :key="index">
          {{ action.timestamp }} - {{ action.description }}
        </li>
      </ul>
      <p v-if="actions.length === 0">No actions logged.</p>
    </div>
  </div>
</template>

<style scoped>
.action-log--container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-image-source: url("@/assets/rpg/bordertemplate.png");
  border-image-slice: 120 150 120 150 fill;
  border-image-width: 40px 40px 40px 40px;
  border-image-outset: 0px 0px 0px 0px;
  border-image-repeat: stretch stretch;
}
</style>