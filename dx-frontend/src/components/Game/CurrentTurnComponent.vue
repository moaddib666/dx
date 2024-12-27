<template>
  <div class="current-turn">
    <!-- Display the current turn number -->
    <div class="turn-number">
      {{ currentTurn?.id || "..." }}
    </div>
  </div>
</template>

<script>
import { ActionGameApi } from "@/api/backendService.js";

export default {
  name: "CurrentTurnComponent",
  data() {
    return {
      currentTurn: null, // Holds the current turn information
      previousTurnId: null, // Tracks the previous turn ID to detect changes
      intervalId: null, // Interval ID for periodic API calls
    };
  },
  methods: {
    async fetchCurrentTurn() {
      try {
        const newTurn = (await ActionGameApi.actionCurrentCycleRetrieve()).data;
        if (this.previousTurnId !== newTurn.id) {
          this.previousTurnId = newTurn.id;
          this.currentTurn = newTurn;
          this.$emit("turnChanged", newTurn); // Emit event when the turn changes
        }
      } catch (error) {
        console.error("Failed to fetch the current turn:", error);
      }
    },
  },
  mounted() {
    this.fetchCurrentTurn(); // Initial fetch
    this.intervalId = setInterval(this.fetchCurrentTurn, 5000); // Fetch every 5 seconds
  },
  beforeUnmount() {
    clearInterval(this.intervalId); // Clean up interval on unmount
  },
};
</script>

<style scoped>
.current-turn {
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 3rem;
  width: 3rem;
  background: radial-gradient(circle, #0d0d0d, #1a1a1a);
  color: #00ffff;
  font-family: "Orbitron", sans-serif; /* Futuristic font for DX World */
  font-size: 1rem;
  font-weight: bold;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.3);
  border: 2px solid rgba(0, 255, 255, 0.7);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.current-turn:hover {
  transform: scale(1.1);
  box-shadow: 0 0 30px rgba(0, 255, 255, 1), 0 0 60px rgba(0, 255, 255, 0.8);
}

.turn-number {
  animation: pulse 1.5s infinite;
}

/* Subtle pulsing animation for the turn number */
@keyframes pulse {
  0%,
  100% {
    color: rgba(0, 255, 255, 0.8);
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5), 0 0 20px rgba(0, 255, 255, 0.4);
  }
  50% {
    color: rgba(0, 255, 255, 1);
    text-shadow: 0 0 15px rgba(0, 255, 255, 1), 0 0 30px rgba(0, 255, 255, 0.8);
  }
}
</style>
