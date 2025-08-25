<script setup lang="ts">
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import { ref } from "vue";

const emit = defineEmits<{
  teleportToPosition: [positionId: string];
  teleportToCoordinates: [x: number, y: number, z: number];
}>();

// Reactive state
const inputValue = ref('');

// Validation functions
const isUUID = (input: string): boolean => {
  // Basic UUID validation regex
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(input);
};

const isCoordinates = (input: string): boolean => {
  // Matches {int}x{int}x{int}
  const coordRegex = /^\d+x\d+x\d+$/;
  return coordRegex.test(input);
};

// Main teleport handler
const handleTeleport = () => {
  const trimmedInput = inputValue.value.trim();

  // Check if input matches UUID format
  if (isUUID(trimmedInput)) {
    emit("teleportToPosition", trimmedInput);
  }
  // Check if input matches coordinates format
  else if (isCoordinates(trimmedInput)) {
    const [x, y, z] = trimmedInput.split("x").map(Number);
    emit("teleportToCoordinates", x, y, z);
  } else {
    console.error("Invalid input. Please provide a valid UUID or coordinates.");
  }
};
</script>

<template>
  <RPGContainer class="teleport-container">
    <div class="header">
      <div class="header-top">
        <h2 class="title">Teleport</h2>
      </div>
    </div>

    <div class="teleport-content">
      <input
        v-model="inputValue"
        class="teleport-input"
        type="text"
        placeholder="Enter UUID or {x}x{y}x{z}"
      />
      <button class="teleport-button" @click="handleTeleport">
        Teleport
      </button>
    </div>
  </RPGContainer>
</template>

<style scoped>
.teleport-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 120px;
  max-height: 150px;
}

.header {
  flex-shrink: 0;
  margin-bottom: 0.4rem;
}

.header-top {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.3rem;
  position: relative;
}

.title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.teleport-content {
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 0.4rem;
  justify-content: center;
  align-items: center;
  padding: 0 0.5rem;
}

.teleport-input {
  flex: 1;
  padding: 0.3rem 0.4rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
  transition: border-color 0.3s, background-color 0.3s;
  min-width: 0;
}

.teleport-input::placeholder {
  color: rgba(250, 218, 149, 0.5);
}

.teleport-input:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.teleport-button {
  padding: 0.3rem 0.6rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.teleport-button:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-1px);
  color: #7fff16;
}

.teleport-button:active {
  transform: translateY(0);
}

/* Responsive design */
@media (max-width: 640px) {
  .teleport-content {
    gap: 0.3rem;
    padding: 0 0.3rem;
  }

  .teleport-input {
    font-size: 0.8rem;
    padding: 0.25rem 0.35rem;
  }

  .teleport-button {
    font-size: 0.8rem;
    padding: 0.25rem 0.5rem;
  }
}
</style>
