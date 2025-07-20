<script setup lang="ts">
import { defineProps, computed, ref, onMounted } from 'vue';
import itemsIcon from '@/assets/icons/items.png';
import { itemsService } from '@/services/ItemsService.js';

// Define props for the component
const props = defineProps<{
  id?: string | number; // Optional ID of the item
  alt?: string; // Optional alt text for the image
}>();

// State for the item data
const item = ref(null);
const loading = ref(false);
const error = ref(null);

// Compute the icon source based on whether an ID is provided
const iconSrc = computed(() => {
  if (!props.id || !item.value) {
    return itemsIcon; // Use placeholder icon if no ID or item not found
  }

  // If item has an image, use it
  if (item.value.image) {
    return item.value.image;
  }

  // Fallback to placeholder icon
  return itemsIcon;
});

// Compute the alt text based on the alt prop or default to a descriptive text
const altText = computed(() => {
  if (props.alt) {
    return props.alt;
  }

  if (item.value && item.value.name) {
    return `Item: ${item.value.name}`;
  }

  return 'Item';
});

// Fetch item data when the component is mounted or when the ID changes
const fetchItem = async () => {
  if (!props.id) {
    item.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Get item by ID
    const itemData = itemsService.getItemById(props.id);
    item.value = itemData;

    if (!itemData) {
      console.warn(`Item with ID ${props.id} not found`);
    }
  } catch (err) {
    console.error('Error fetching item:', err);
    error.value = err;
    item.value = null;
  } finally {
    loading.value = false;
  }
};

// Watch for changes to the ID prop
onMounted(() => {
  fetchItem();
});
</script>

<template>
  <div class="item-select-icon">
    <img :src="iconSrc" class="icon" :alt="altText" :class="{ 'is-loading': loading }"/>
    <div v-if="error" class="error-message">!</div>
  </div>
</template>

<style scoped>
.item-select-icon {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon {
  width: 90%;
  height: 90%;
  padding: 0;
  margin: 0;
  object-fit: contain;
}

.is-loading {
  opacity: 0.7;
}

.error-message {
  position: absolute;
  bottom: 5px;
  right: 5px;
  background-color: red;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}
</style>