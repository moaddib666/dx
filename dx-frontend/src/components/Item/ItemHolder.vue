<template>
  <div class="item-holder">
    <!-- Header with slot and close button -->
    <div class="header" v-if="showHeader">
      <slot name="header"></slot>
      <button class="close-btn" @click="close">✖</button>
    </div>

    <!-- 5x5 Grid for items -->
    <div class="grid">
      <div
          v-for="(item, index) in visibleItems"
          :key="index"
          class="grid-cell"
          :class="{ empty: !item }"
      >
        <ItemCell
            v-if="item"
            :itemData="item"
            @item-clicked="handleItemClick"
        />
      </div>
    </div>

    <!-- Footer with pagination -->
    <div class="footer">
      <button
          class="pagination-btn"
          @click="prevPage"
          :disabled="currentPage === 0"
      >
        Prev
      </button>
      <button
          class="pagination-btn"
          @click="nextPage"
          :disabled="!hasNextPage"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import ItemCell from "@/components/Item/ItemCell.vue";

export default {
  name: "ItemHolder",
  components: {
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
    gridSize: {
      type: Number,
      default: 15, // 5x3 grid by default
    },
  },
  data() {
    return {
      currentPage: 0,
    };
  },
  computed: {
    visibleItems() {
      const startIndex = this.currentPage * this.gridSize;
      const endIndex = startIndex + this.gridSize;
      const itemsInPage = this.items.slice(startIndex, endIndex);

      // Fill remaining cells with `null` to maintain consistent grid size
      while (itemsInPage.length < this.gridSize) {
        itemsInPage.push(null);
      }

      return itemsInPage;
    },
    hasNextPage() {
      return this.currentPage < Math.floor(this.items.length / this.gridSize);
    },
  },
  methods: {
    handleItemClick(itemId) {
      this.$emit("item-clicked", itemId); // Emit clicked item ID to parent
    },
    nextPage() {
      if (this.hasNextPage) {
        this.currentPage += 1;
      }
    },
    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage -= 1;
      }
    },
    close() {
      this.$emit("close"); // Emit close event to parent
    },
  },
};
</script>

<style scoped>
.item-holder {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 1rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  margin: auto;
  color: white;
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

.grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 columns */
  grid-template-rows: repeat(3, 1fr); /* 5 rows */
  gap: 0.5rem;
}

.grid-cell {
  width: 5rem;
  height: 5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1); /* Background for empty cells */
  border-radius: 0.5rem;
  position: relative;
}

.grid-cell.empty {
  background: rgba(255, 255, 255, 0.05);
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s ease-in-out, color 0.2s ease-in-out;
}

.pagination-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.pagination-btn:disabled {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.3);
  cursor: not-allowed;
}
</style>
