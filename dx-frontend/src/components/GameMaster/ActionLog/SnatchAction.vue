<template>
  <div class="snatch-action" v-if="!loading">
    <span class="snatch-status" :class="{ success: data.success, failure: !data.success }">
      {{ data.success ? "Done" : "Fail" }}
    </span>

    <div v-if="data.success && data.snatched && data.snatched.length > 0" class="items-container">
      <ItemIconWithHover
          v-for="itemId in data.snatched"
          :key="itemId"
          :itemData="itemsService.getCachedWorldItem(itemId)"
          class="icon__image"
      />
      <ItemIconWithHover
          v-if="data.snatched && data.snatched.length > 0"
          :itemData="itemsService.getCachedWorldItem(data.snatched[0])"
          class="background__image"
      />
    </div>
  </div>

  <div class="loading-state" v-else>
    <span>Loading items...</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import WorldItemsGameMasterService from "@/services/worldItemsService.js";
import ItemIconWithHover from "@/components/GameMaster/ActionLog/ItemIconWithHover.vue";

interface SnatchData {
  success: boolean;
  snatched?: string[];
  discovered?: string[];
}

interface Props {
  data: SnatchData;
}

// Props definition
const props = defineProps<Props>();

// Reactive data
const loading = ref(true);
const itemsService = WorldItemsGameMasterService;

// Methods
const refreshItemsCache = async () => {
  try {
    if (props.data.discovered) {
      await Promise.all(
          props.data.discovered.map((id) => itemsService.getWorldItem(id))
      );
    }
    if (props.data.snatched) {
      await Promise.all(
          props.data.snatched.map((id) => itemsService.getWorldItem(id))
      );
    }
  } catch (error) {
    console.error("Error refreshing items cache:", error);
  } finally {
    loading.value = false;
  }
};

// Lifecycle
onMounted(async () => {
  await refreshItemsCache();
});
</script>

<style scoped>
.snatch-action {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 4px;
  gap: 0.25rem;
  padding: 0.1rem 0.3rem;
  font-size: 0.8rem;
  margin: 0.25rem 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
}

.items-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.background__image {
  position: absolute;
  width: 60%;
  height: 100%;
  object-fit: cover;
  right: 0;
  top: 0;
  mask: radial-gradient(circle at top, rgba(0, 0, 0, 0.2) 30%, rgba(0, 0, 0, 0) 90%);
}

.icon__image {
  width: 1.6rem;
  height: 1.6rem;
  object-fit: cover;
  border-radius: 0.2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.snatch-status {
  font-weight: bold;
  margin-right: auto;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
  font-size: 1.7rem;
  line-height: 1;
}

.snatch-status.success {
  color: #4caf50;
}

.snatch-status.failure {
  color: #f44336;
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
