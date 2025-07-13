<script setup lang="ts">
import { computed } from 'vue';
import RPGCell from "@/components/RPGGrid/RPGCell.vue";

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
  // Pagination
  items: {
    type: Array,
    default: () => []
  },
  currentPage: {
    type: Number,
    default: 1
  },
  itemsPerPage: {
    type: Number,
    default: 0 // 0 means use rowCount * colCount
  }
});

// Emit events
const emit = defineEmits(['gridItemPicked']);

// Computed properties
const effectiveItemsPerPage = computed(() => {
  return props.itemsPerPage > 0 ? props.itemsPerPage : props.rowCount * props.colCount;
});

const currentPageItems = computed(() => {
  const startIndex = (props.currentPage - 1) * effectiveItemsPerPage.value;
  return props.items.slice(startIndex, startIndex + effectiveItemsPerPage.value);
});

const gridCells = computed(() => {
  // Create a grid with the specified number of cells
  const totalCells = props.rowCount * props.colCount;
  const cells = Array(totalCells).fill().map(() => null);

  // Fill cells with items from the current page
  currentPageItems.value.forEach((item, index) => {
    if (index < totalCells) {
      cells[index] = item;
    }
  });

  return cells;
});

const gridStyle = computed(() => {
  return {
    gridTemplateColumns: `repeat(${props.colCount}, ${props.cellSize}rem)`,
    gridTemplateRows: `repeat(${props.rowCount}, ${props.cellSize}rem)`
  };
});
</script>

<template>
  <div class="rpg-grid" :style="gridStyle">
    <RPGCell v-for="(item, index) in gridCells" :key="index">
      <slot v-if="item" :item="item" @click="$emit('gridItemPicked', item)" />
      <div v-else class="empty-cell"></div>
    </RPGCell>
  </div>
</template>

<style scoped>
.rpg-grid {
  display: grid;
  gap: 0.5rem;
  padding: 1rem;
}

.empty-cell {
  width: 100%;
  height: 100%;
}
</style>