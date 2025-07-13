<script setup lang="ts">
import { computed, ref } from 'vue';
import RPGGrid from './RPGGrid.vue';
import RPGScroll from './RPGScroll.vue';

// Props definition
const props = defineProps({
  // Grid configuration
  rowCount: {
    type: Number,
    default: 4
  },
  colCount: {
    type: Number,
    default: 6
  },
  cellSize: {
    type: Number,
    default: 6 // Size in rem
  },
  // Items and pagination
  items: {
    type: Array,
    default: () => []
  },
  itemsPerPage: {
    type: Number,
    default: 0 // 0 means use rowCount * colCount
  },
  initialPage: {
    type: Number,
    default: 1
  }
});

// Emit events
const emit = defineEmits(['gridItemPicked']);

// State
const currentPage = ref(props.initialPage);

// Computed properties
const effectiveItemsPerPage = computed(() => {
  return props.itemsPerPage > 0 ? props.itemsPerPage : props.rowCount * props.colCount;
});

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.items.length / effectiveItemsPerPage.value));
});

// Methods
const handlePageChange = (page: number) => {
  currentPage.value = page;
};

const handleGridItemPicked = (item: any) => {
  emit('gridItemPicked', item);
};
</script>

<template>
  <div class="rpg-grid-with-scroller">
    <RPGGrid
      :row-count="rowCount"
      :col-count="colCount"
      :cell-size="cellSize"
      :items="items"
      :current-page="currentPage"
      :items-per-page="itemsPerPage"
      @grid-item-picked="handleGridItemPicked"
    >
      <template #default="slotProps">
        <slot :item="slotProps.item"></slot>
      </template>
    </RPGGrid>

    <RPGScroll
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="handlePageChange"
    />
  </div>
</template>

<style scoped>
.rpg-grid-with-scroller {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>