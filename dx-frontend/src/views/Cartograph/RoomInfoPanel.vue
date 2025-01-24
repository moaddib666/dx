<template>
  <div v-if="selectedRoom" class="room-info-panel">
    <button class="unset-button" title="Reset selection" @click="unsetRoom">x</button>

    <h3>Room Info</h3>

    <!-- Coordinates -->
    <p class="coordinates">
      <strong>Location:</strong>
      {{ selectedRoom.position.grid_x }}x{{ selectedRoom.position.grid_y }}, Floor={{ selectedRoom.position.grid_z }}
    </p>

    <!-- Room Type -->
    <div class="field-row">
      <label>Type:</label>
      <select v-model="editingType" @change="applyChanges">
        <option v-for="type in roomTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
    </div>

    <!-- Room Label -->
    <div class="field-row">
      <label>Label:</label>
      <select v-model="editingLabel" @change="applyChanges">
        <option v-for="label in roomLabels" :key="label.value" :value="label.value">
          {{ label.label }}
        </option>
      </select>
    </div>
    <!-- Delete Button -->
    <button class="" title="Delete Room" @click="deleteRoom">delete</button>
  </div>
</template>

<script>
export default {
  name: "RoomInfoPanel",
  props: {
    selectedRoom: {
      type: Object,
      default: null,
    },
    roomTypes: {
      type: Array,
      default: () => [],
    },
    roomLabels: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      editingType: "",
      editingLabel: "",
    };
  },
  watch: {
    selectedRoom: {
      immediate: true,
      handler(newRoom) {
        if (newRoom) {
          this.editingType = newRoom.labels?.[0] || "default";
          this.editingLabel = newRoom.labels?.[1] || "default";
        } else {
          this.editingType = "";
          this.editingLabel = "";
        }
      },
    },
  },
  methods: {
    applyChanges() {
      if (!this.selectedRoom) return;

      const updatedRoom = {
        ...this.selectedRoom,
        labels: [this.editingType, this.editingLabel],
      };
      this.$emit("update-room", updatedRoom);
    },
    unsetRoom() {
      this.$emit("unset-room");
    },
    deleteRoom() {
      if (confirm("Are you sure you want to delete this room?")) {
        this.$emit("delete-room", this.selectedRoom.position.id);
      }
    },
  },
};
</script>

<style scoped>
.room-info-panel {
  background: #2a2a2a;
  color: #f1f1f1;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  width: 300px;
  position: relative;
  font-family: Arial, sans-serif;
}

.room-info-panel h3 {
  margin: 0 0 15px;
  font-size: 18px;
  color: #ffa500;
}

.coordinates {
  margin: 10px 0;
  font-size: 14px;
  color: #ccc;
}

.field-row {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.field-row label {
  width: 70px;
  margin-right: 10px;
  font-weight: bold;
  color: #ddd;
}

.field-row select {
  flex: 1;
  padding: 5px;
  background: #3a3a3a;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
}

.field-row select:focus {
  outline: none;
  border-color: #ffa500;
}

.unset-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  color: #ff4444;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: color 0.3s;
}

.unset-button:hover {
  color: #ff6666;
}

.unset-button:active {
  color: #ff2222;
}
</style>
