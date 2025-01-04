<template>
  <div class="end-turn-container">
    <!-- Small End Turn Button -->
    <button class="end-turn-button" @click="confirmEndTurn">
    </button>

    <!-- Confirmation Modal -->
    <div v-if="isConfirming" class="modal-overlay" @click.self="cancelConfirmation">
      <div class="modal-content">
        <h3>End Turn for All Players?</h3>
        <div class="modal-actions">
          <button class="cancel-button" @click="cancelConfirmation">No</button>
          <button class="confirm-button" @click="endTurn">Yes</button>
        </div>
      </div>
    </div>

    <!-- Success/Failure Popup -->
    <div v-if="popupMessage" :class="['popup', popupType]">
      {{ popupMessage }}
    </div>
  </div>
</template>

<script>
import { ActionGameApi } from "@/api/backendService.js";

export default {
  name: "EndTurnComponent",
  data() {
    return {
      isConfirming: false, // Tracks if confirmation modal is open
      popupMessage: null, // Message to display in the popup
      popupType: "", // Type of popup: success or error
    };
  },
  methods: {
    confirmEndTurn() {
      this.isConfirming = true; // Show the confirmation modal
    },
    cancelConfirmation() {
      this.isConfirming = false; // Hide the confirmation modal
    },
    async endTurn() {
      this.isConfirming = false; // Hide the confirmation modal

      try {
        // API call to end the turn
        await ActionGameApi.actionNextCycleCreate(); // Replace with actual API call
        this.showPopup("Turn ended successfully!", "success");
      } catch (error) {
        this.showPopup("Failed to end turn. Please try again.", "error");
      }
    },
    showPopup(message, type) {
      this.popupMessage = message;
      this.popupType = type;
      setTimeout(() => {
        this.popupMessage = null; // Clear popup after 3 seconds
      }, 3000);
    },
  },
};
</script>

<style scoped>
/* Main Container */
.end-turn-container {
  display: flex;
  color: white;
}
/* Small End Turn Button */
.end-turn-button {
  height: 60px;
  width: 60px;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  background: url("@/assets/images/action/end-turn.webp") center center / cover;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.7), 0 0 30px rgba(138, 43, 226, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
}

.end-turn-button:hover {
  transform: scale(1.1);
  box-shadow: 0 0 25px rgba(138, 43, 226, 1), 0 0 35px rgba(138, 43, 226, 0.8);
}

.end-turn-button:active {
  transform: scale(0.95);
  box-shadow: 0 0 15px rgba(138, 43, 226, 0.8), 0 0 25px rgba(138, 43, 226, 0.6);
}


/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Modal Content */
.modal-content {
  background: #2e2e2e;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  color: white;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.8);
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.confirm-button,
.cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.confirm-button {
  background: #28a745;
  color: white;
}

.confirm-button:hover {
  background: #218838;
}

.cancel-button {
  background: #dc3545;
  color: white;
}

.cancel-button:hover {
  background: #c82333;
}

/* Popup Styles */
.popup {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  z-index: 2000;
  animation: fadeInOut 3s ease;
}

.popup.success {
  background: #28a745;
}

.popup.error {
  background: #dc3545;
}

/* Popup Animation */
@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  10%,
  90% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
}
</style>
