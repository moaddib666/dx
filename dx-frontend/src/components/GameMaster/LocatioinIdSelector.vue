<template>
  <div class="location-selector">
    <!-- Input field for UUID -->
    <label for="locationId" class="selector-label">Location ID</label>
    <input
        type="text"
        id="locationId"
        v-model="locationId"
        class="selector-input"
        placeholder="Enter Location UUID"
    />
    <!-- Button to confirm selection -->
    <button class="select-button" @click="confirmSelection">Select</button>
  </div>
</template>

<script>
export default {
  name: "LocationIdSelector",
  data() {
    return {
      locationId: "", // Holds the entered UUID
    };
  },
  methods: {
    confirmSelection() {
      if (this.locationId.trim() === "") {
        alert("Please enter a valid UUID.");
        return;
      }
      this.$emit("locationSelected", this.locationId);
    },
  },
};
</script>

<style scoped>
/* Container Styles */
.location-selector {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  padding: 15px;
  background: #1e1e1e;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  font-family: "Arial", sans-serif;
  color: white;
}

/* Label Styles */
.selector-label {
  font-size: 1rem;
  font-weight: bold;
  color: #cccccc;
}

/* Input Styles */
.selector-input {
  width: 100%;
  padding: 10px 12px;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  background: #2e2e2e;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: background 0.2s ease, box-shadow 0.2s ease;
}

.selector-input::placeholder {
  color: #777777;
}

.selector-input:focus {
  background: #3e3e3e;
  box-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
  outline: none;
}

/* Button Styles */
.select-button {
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  background: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease, box-shadow 0.3s ease;
}

.select-button:hover {
  background: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.5);
}
</style>
