<template>
  <div class="test-screen">
    <MapEditor
      :initial-data="initialMapData"
      @data-change="handleDataChange"
      @save="handleSave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MapEditor from '@/components/GlobalWorldMap/MapEditor.vue'

// Initial map data (can be null to use default sample data)
const initialMapData = ref(null)

// Event handlers
const handleDataChange = (data: any) => {
  console.log('Map data changed:', data)
  // Here you could save to localStorage, send to backend, etc.
}

const handleSave = (data: any) => {
  console.log('Map data saved:', data)
  // Handle explicit save action
}
</script>

<style scoped>
.test-screen {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>