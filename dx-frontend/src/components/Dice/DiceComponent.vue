<template>
  <div class="dice-container">
    <!-- Dice button content -->
    <div class="dice-btn" @click="openModal"></div>
    <!-- Modal Overlay -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <DiceVisualizer @selectedDice="selectedDice" :result="result"/>
        <button class="modal-close-button" @click="closeModal">X</button>
      </div>
    </div>
  </div>

</template>

<script>
import DiceVisualizer from "@/components/Dice/DiceVisualizer.vue";

export default {
  name: "DiceComponent",
  components: {DiceVisualizer},
  props: {
    result: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      isModalOpen: false, // State to track if the modal is open
    };
  },
  methods: {
    selectedDice({dice, index}) {
      this.$emit("selectedDice", {dice, index});
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
      this.$emit("reset");
    },
  },
};
</script>

<style scoped>
/* Container for the dice button */
.dice-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-image: url('@/assets/images/dice/dice.png'); /* Your dice image */
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;

  /* Dimensions */
  min-height: 50px;
  min-width: 50px;
  max-height: 1vh;
  max-width: 1vh;

  /* Rounded corners and smooth transition */
  border-radius: 8px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dice-btn:hover {
  cursor: pointer;
  transform: scale(1.1); /* Slightly enlarge the dice container */
}

/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 10, 10, 0.9); /* Dark background with slight transparency */
  backdrop-filter: blur(5px); /* Adds a cool blur effect for a modern look */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000; /* Ensures the modal is above all other content */
}

/* Modal content */
.modal-content {
  background: #1e1e1e; /* Dark modal content background */
  color: #ffffff; /* Text color for content */
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8); /* Cool shadow for the modal */
  animation: slide-in 0.3s ease-out; /* Smooth entrance animation */
}

/* Close button */
.modal-close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: 2px solid #ffffff;
  border-radius: 50%;
  color: #ffffff;
  font-size: 18px;
  cursor: pointer;
  width: 35px;
  height: 35px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background 0.2s ease, transform 0.2s ease;
}

.modal-close-button:hover {
  background: #ff4545; /* Highlight close button on hover */
  transform: scale(1.1); /* Slightly enlarge button on hover */
}

/* Entrance animation for modal */
@keyframes slide-in {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
