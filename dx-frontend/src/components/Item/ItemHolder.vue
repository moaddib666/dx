<template>
  <RPGContainer class="item-holder">
    <!-- Header with slot and close button -->
    <div class="header" v-if="showHeader">
      <slot name="header"></slot>
      <button class="close-btn" @click="close">✖</button>
    </div>

    <!-- Grid with pagination -->
    <RPGGridWithScroller
      :row-count="3"
      :col-count="5"
      :cell-size="6"
      :items="items"
      :initial-page="currentPage + 1"
      @grid-item-picked="handleItemClick"
      class="item-grid"
    >
      <template #default="{ item }">
        <ItemCell
          class="item-cell"
          v-if="item"
          :itemData="item"
        />
      </template>
    </RPGGridWithScroller>
  </RPGContainer>
</template>

<script>
import ItemCell from "@/components/Item/ItemCell.vue";
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import RPGGridWithScroller from "@/components/RPGGrid/RPGGridWithScroller.vue";

export default {
  name: "ItemHolder",
  components: {
    RPGGridWithScroller,
    RPGContainer,
    ItemCell,
  },
  props: {
    showHeader: {
      type: Boolean,
      default: true, // Show the UI by default
    },
    items: {
      type: Array,
      required: true, // List of items to display
    },
  },
  data() {
    return {
      currentPage: 0, // Keep for compatibility with initial-page prop
    };
  },
  methods: {
    handleItemClick(item) {
      this.$emit("item-clicked", item.id || item); // Emit clicked item ID to parent
    },
    close() {
      this.$emit("close"); // Emit close event to parent
    },
  },
};
</script>

<style scoped>
.item-holder {
  gap: 1rem;
  margin: auto;
  color: white;
  flex-direction: column;
  z-index: 1000; /* Ensure it appears above other elements */
}

.item-cell {
  /* Custom styling for item cells */
  width: 90%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2rem;
  font-weight: bold;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 0.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
}

.close-btn:hover {
  color: red;
}

.item-grid {
  /* Custom styling for the grid component */
  margin: 0 auto;
}
</style>
