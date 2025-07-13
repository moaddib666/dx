<!-- src/components/BargainComponent.vue -->
<template>
  <div class="bargain-container" :class="{ submitted: submitted }">
    <!-- Left Column: Your Inventory -->
    <div class="column inventory-column">
      <h2>Your Inventory</h2>
      <!-- Clicking an item immediately offers it, unless already submitted -->
      <ItemHolder :items="itemsAvailableToSubmit" @item-clicked="handleItemClicked" :disabled="submitted" :show-header="false"
                  :row-count="4"
                  :col-count="3"
      />
    </div>

    <!-- Center Column: Your Offer -->
    <div class="column offer-column">
      <h2>Your Offer</h2>
      <ItemHolder :items="yourOffer" @item-clicked="removeOfferItem" :disabled="submitted" :show-header="false"
                  :row-count="4"
                  :col-count="3"
      />
    </div>

    <!-- Right Column: Target's Offer -->
    <div class="column target-offer-column">
      <h2>Target's Offer</h2>
      <ItemHolder :items="targetOffer" @item-clicked="removeOfferItem" :disabled="submitted" :show-header="false"
                  :row-count="4"
                  :col-count="3"
      />
    </div>

    <div class="action">
      <!-- Submit button is shown only if there is at least one offered item and not yet submitted -->
      <button
          v-if="yourOffer.length && !submitted"
          class="submit-btn"
          @click="submitOffers"
      >
        Submit Offers
      </button>
      <!-- Reject offer if not fit -->
      <button
          class="reject-btn"
          @click="rejectOffers"
      >
        Reject Offers
      </button>
    </div>
  </div>
</template>

<script>
import ItemHolder from "@/components/Item/ItemHolder.vue";
import ItemCell from "@/components/Item/ItemCell.vue";
import bargainService from "@/services/bargainService.js";

export default {
  name: "BargainComponent",
  components: {
    ItemHolder,
    ItemCell,
  },
  props: {
    // Your inventory is passed as a prop.
    inventory: {
      type: Array,
      required: true,
    },
    // Optionally, an active bargain ID may be passed in.
    bargainId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      // The active bargain ID.
      currentBargainId: this.bargainId,
      // For this example, assume current user is side A.
      // 'yourOffer' holds side A's offered items.
      yourOffer: [],
      // 'targetOffer' holds side B's offered items.
      targetOffer: [],
      // Once submitted, no further modifications are allowed.
      submitted: false,
    };
  },
  mounted() {
    // Load the bargain details if a bargain is active.
    if (this.currentBargainId) {
      this.loadBargainDetails();
    }
  },
  computed: {
    // return filtered inventory items that are not yet offered
    itemsAvailableToSubmit() {
      // this.inventory.id === this.yourOffer.id;
      return this.inventory.filter(item => !this.yourOffer.some(offer => offer.id === item.id));
    },
  },
  methods: {
    /**
     * Automatically offer an inventory item when clicked.
     * If the bargain is not submitted, the item is immediately added via the API.
     *
     * @param {Object} item - The clicked inventory item.
     */
    async handleItemClicked(item) {
      if (this.submitted) return;
      try {
        // Add the item to the bargain using its unique ID.
        console.debug("Offering item:", {item});
        await bargainService.addItemToBargain(this.currentBargainId, item);
        // Refresh bargain details to update both sides’ offered items.
        await this.loadBargainDetails();
      } catch (error) {
        console.error("Error offering item:", error);
      }
    },

    /**
     * Remove an offered item.
     * Allowed only if the bargain has not been submitted.
     *
     * @param {Object} item - The offered item to remove.
     */
    async removeOfferItem(item) {
      if (this.submitted) return;
      try {
        console.debug("Removing offered item:", {item});
        await bargainService.removeItemFromBargain(this.currentBargainId, item);
        await this.loadBargainDetails();
      } catch (error) {
        console.error("Error removing offered item:", error);
      }
    },

    /**
     * Load the bargain details from the API.
     * Expects a response in the following format:
     * {
     *   id: string,
     *   side_a_offered_items: Array,
     *   side_b_offered_items: Array,
     *   side_a_accepted: boolean,
     *   side_b_accepted: boolean,
     *   cancelled: boolean,
     *   completed: boolean,
     *   side_a: string,
     *   side_b: string
     * }
     * Assumes current user is side A.
     */
    async loadBargainDetails() {
      if (!this.currentBargainId) return;
      try {
        const data = await bargainService.getBargainDetails(this.currentBargainId);
        console.debug("Loaded bargain details:", {data});
        // Set the offered items based on the current side.
        this.yourOffer = data.side_a_offered_items.map(i => i.item) || [];
        this.targetOffer = data.side_b_offered_items.map(i => i.item) || [];
      } catch (error) {
        console.error("Error loading bargain details:", error);
      }
    },

    /**
     * Finalize your offers. Once submitted, the UI becomes non-interactive.
     */
    async submitOffers() {
      this.submitted = true;
      console.debug("Offers submitted!");
      await bargainService.acceptBargain(this.currentBargainId);
      this.$emit("bargain-submitted");
      this.$emit("bargain-completed");
    },
    async rejectOffers() {
      this.submitted = true;
      console.debug("Offers rejected!");
      await bargainService.rejectBargain(this.currentBargainId);
      this.$emit("bargain-rejected");
      this.$emit("bargain-completed");
    },
  },
};
</script>

<style scoped>
/* Reduce the overall font size by 0.6 rem */
.bargain-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 200;
  font-size: calc(1rem - 0.6rem);
  display: flex;
  flex-direction: row;
  justify-items: center;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  backdrop-filter: blur(5px);
}

/* When submitted, gray out the container and disable interactions */
.bargain-container.submitted {
  opacity: 0.5;
  pointer-events: none;
}

/* Ensure all three columns are of equal size */
.column {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 1rem;
  padding: 1rem;
  color: white;
}

/* Force each column to take up one-third of the container */
.inventory-column,
.offer-column,
.target-offer-column {
  flex-basis: 33.33%;
}

.offer-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 0.5rem;
}

.remove-btn {
  margin-left: 0.5rem;
  padding: 0.2rem 0.5rem;
  background: rgba(255, 0, 0, 0.7);
  border: none;
  color: white;
  border-radius: 0.3rem;
  cursor: pointer;
  transition: background 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 0, 0, 0.9);
}

.submit-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 255, 0, 0.7);
  border: none;
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background: rgba(0, 255, 0, 0.9);
}

.reject-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 0, 0, 0.7);
  border: none;
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.action {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
}

.reject-btn:hover {
  background: rgba(255, 0, 0, 0.9);
}


</style>
