<template>
  <div class="teleport-container">
    <input
        v-model="inputValue"
        class="teleport-input"
        type="text"
        placeholder="Enter UUID or {x}x{y}x{z}"
    />
    <button class="teleport-button" @click="handleTeleport">Teleport</button>
  </div>
</template>

<script>
export default {
  name: "TeleportComponent",
  data() {
    return {
      inputValue: "", // Stores the user's input
    };
  },
  methods: {
    handleTeleport() {
      const trimmedInput = this.inputValue.trim();

      // Check if input matches UUID format
      if (this.isUUID(trimmedInput)) {
        this.$emit("teleportToPosition", trimmedInput);
      }
      // Check if input matches coordinates format
      else if (this.isCoordinates(trimmedInput)) {
        const [x, y, z] = trimmedInput.split("x").map(Number);
        this.$emit("teleportToCoordinates", x, y, z);
      } else {
        console.error("Invalid input. Please provide a valid UUID or coordinates.");
      }
    },
    isUUID(input) {
      // Basic UUID validation regex
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      return uuidRegex.test(input);
    },
    isCoordinates(input) {
      // Matches {int}x{int}x{int}
      const coordRegex = /^\d+x\d+x\d+$/;
      return coordRegex.test(input);
    },
  },
};
</script>

<style scoped>
.teleport-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  margin: auto;
}

.teleport-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-family: "Roboto", sans-serif;
}

.teleport-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.teleport-button {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #0f0, #0a0);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.teleport-button:hover {
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.8);
}
</style>
