<template>
  <div class="selector">
    <!-- Input field for UUID -->
    <label for="gameObjectId" class="selector-label">{{itemName}} Selector</label>
    <input
        type="text"
        id="gameObjectId"
        v-model="gameObjectId"
        class="selector-input"
        :placeholder="placeholder"
    />
    <!-- Button to confirm selection -->
    <LandingButton :action="confirmSelection" class="selector-btm"> Select </LandingButton>
  </div>
</template>

<script>
import LandingButton from "@/components/btn/LandingButton.vue";

export default {
  name: "GameObjectRawSelector",
  components: {LandingButton},
  props: {
    itemName: {
      type: String,
      default: "Location", // Name of the item being selected
    },
    placeholder: {
      type: String,
      default: "Enter UUID", // Placeholder text for the input field
    },
  },
  data() {
    return {
      gameObjectId: "", // Holds the entered UUID
    };
  },
  methods: {
    confirmSelection() {
      if (this.gameObjectId.trim() === "") {
        alert("Please enter a valid UUID.");
        return;
      }
      this.$emit("gameObjectSelected", this.gameObjectId);
    },
  },
};
</script>

<style scoped>
/* Container Styles */
.selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-start;
  padding: 1rem;
  background: #1e1e1e;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  margin: 0 auto;
  font-family: "Arial", sans-serif;
  color: white;
}

/* Label Styles */
.selector-label {
  font-size: 0.7rem;
  font-weight: bold;
  color: #cccccc;
}

/* Input Styles */
.selector-input {
  padding: 0.5rem;
  font-size: 0.8rem;
  flex: 1;
  border: none;
  border-radius: 4px;
  background: #2e2e2e;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: background 0.2s ease, box-shadow 0.2s ease;
  width: 100%;
}

.selector-input::placeholder {
  color: #777777;
}

.selector-input:focus {
  background: #3e3e3e;
  box-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
  outline: none;
}

.selector-btm {
  font-size: 0.6rem;
  padding: 0.5rem 1rem;
  align-self: flex-end;
  margin: 0;
}
</style>
