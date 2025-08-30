<template>
  <div class="snatch-action" v-if="!loading">
    <!-- Success Status -->
    <div class="success-section" :class="{ success: data.success, failure: !data.success }">
      {{ data.success ? "Done" : "Fail" }}
    </div>

      <div class="items-section" v-if="data.success">
        <span class="items-label">Snatched:</span>
        <div class="item-icons">
          <ItemIconWithHover
              v-for="itemId in data.snatched"
              :key="itemId"
              :itemData="itemsService.getCachedWorldItem(itemId)"
          />
        </div>
      </div>
  </div>

  <div class="loading-state" v-else>
    <span>Loading items...</span>
  </div>
</template>

<script>
import SmallCharPreview from "@/components/GameMaster/ActionLog/SmallCharPreview.vue";
import WorldItemsGameMasterService from "@/services/worldItemsService.js";
import ItemIconWithHover from "@/components/GameMaster/ActionLog/ItemIconWithHover.vue";

export default {
  name: "SnatchAction",
  components: { ItemIconWithHover, SmallCharPreview },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  async mounted() {
    await this.refreshItemsCache();
  },
  data() {
    return {
      loading: true,
      itemsService: WorldItemsGameMasterService,
    };
  },
  methods: {
    async refreshItemsCache() {
      try {
        if (this.data.discovered) {
          await Promise.all(
              this.data.discovered.map((id) => this.itemsService.getWorldItem(id))
          );
        }
        if (this.data.snatched) {
          await Promise.all(
              this.data.snatched.map((id) => this.itemsService.getWorldItem(id))
          );
        }
      } catch (error) {
        console.error("Error refreshing items cache:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Snatch Action Container */
.snatch-action {
  display: flex;
  align-items: center;
  gap: 1.5em;
  font-size: 0.85em;
  padding: 0.5em;
  border: 1px solid rgb(68, 68, 68);
  border-radius: 0.5em;
  background: rgb(32, 32, 32);
}

/* Character Preview */
.char-preview {
  flex-shrink: 0;
}

/* Success Section */
.success-section {
  font-weight: bold;
  border-radius: 0.3em;
  text-align: center;
  font-size: 0.7rem;
  display: none;
}

.success-section.success {
  color: #4caf50;
  border-color: #4caf50;
}

.success-section.failure {
  background: #f44336;
  border-color: #f44336;
  border-radius: 0.3em;
  padding: 0.2em 0.5em;
  display: flex;
}

/* Items Container */
.items-container {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}

/* Items Section */
.items-section {
  display: flex;
  align-items: center;
  font-size: 0.6rem;
}

.items-label {
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
}

.item-icons {
  display: flex;
  flex-wrap: wrap;
}

.item-icons .item-icon {
  width: 2.5em;
  height: 2.5em;
}

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1em;
  color: rgba(255, 255, 255, 0.8);
  height: 5em;
}
</style>
