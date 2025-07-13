<script setup lang="ts">
import { computed } from 'vue';

// Props definition
const props = defineProps({
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 1
  },
  showFirstLast: {
    type: Boolean,
    default: true
  }
});

// Emit events
const emit = defineEmits(['pageChange']);

// Methods
const goToPage = (page: number) => {
  if (page >= 1 && page <= props.totalPages) {
    emit('pageChange', page);
  }
};

const goToFirstPage = () => goToPage(1);
const goToPrevPage = () => goToPage(props.currentPage - 1);
const goToNextPage = () => goToPage(props.currentPage + 1);
const goToLastPage = () => goToPage(props.totalPages);

// Computed properties
const isFirstPage = computed(() => props.currentPage === 1);
const isLastPage = computed(() => props.currentPage === props.totalPages);
</script>

<template>
  <div class="rpg-scroll">
    <button
      v-if="showFirstLast"
      class="scroll-button first-button"
      :disabled="isFirstPage"
      @click="goToFirstPage"
      title="First Page"
    >
      «
    </button>

    <button
      class="scroll-button prev-button"
      :disabled="isFirstPage"
      @click="goToPrevPage"
      title="Previous Page"
    >
      ‹
    </button>

    <span class="page-indicator">{{ currentPage }} / {{ totalPages }}</span>

    <button
      class="scroll-button next-button"
      :disabled="isLastPage"
      @click="goToNextPage"
      title="Next Page"
    >
      ›
    </button>

    <button
      v-if="showFirstLast"
      class="scroll-button last-button"
      :disabled="isLastPage"
      @click="goToLastPage"
      title="Last Page"
    >
      »
    </button>
  </div>
</template>

<style scoped>
.rpg-scroll {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
}

.scroll-button {
  background-color: #4a4a4a;
  color: white;
  border: 1px solid #6a6a6a;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  min-width: 2rem;
  text-align: center;
}

.scroll-button:hover:not(:disabled) {
  background-color: #5a5a5a;
}

.scroll-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 0.9rem;
  margin: 0 0.5rem;
  min-width: 4rem;
  text-align: center;
}
</style>