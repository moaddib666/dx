<template>
  <div
      :style="{ top: room.grid_y * cellSize + 'px', left: room.grid_x * cellSize + 'px' }"
      class="room"
  >
    <div class="room-name">{{ room.name }}</div>
    <!-- Directional Arrows -->
    <div
        v-for="(offset, direction) in directions"
        :key="direction"
        :class="['arrow', direction]"
        :style="getArrowStyle(direction)"
        @click="handleAction(direction)"
    ></div>
  </div>
</template>

<script>
export default {
  props: {
    room: Object,
    cellSize: {
      type: Number,
      default: 50,
    },
  },
  data() {
    return {
      directions: {
        north: [0, -1],
        northeast: [1, -1],
        east: [1, 0],
        southeast: [1, 1],
        south: [0, 1],
        southwest: [-1, 1],
        west: [-1, 0],
        northwest: [-1, -1],
      },
    };
  },
  methods: {
    handleAction(direction) {
      const [dx, dy] = this.directions[direction];

      const targetX = this.room.grid_x + dx;
      const targetY = this.room.grid_y + dy;

      // Check if a room exists at the target location
      const existingRoom = this.$parent.mapData.rooms.find(
          (r) => r.grid_x === targetX && r.grid_y === targetY && r.floor === this.room.floor
      );

      if (existingRoom) {
        // Connect to the existing room
        this.connectToRoom(existingRoom);
      } else {
        // Create a new room in the chosen direction
        this.createRoom(targetX, targetY);
      }
    },
    createRoom(gridX, gridY) {
      const newRoom = {
        id: Date.now(),
        name: `Room ${this.$parent.mapData.rooms.length + 1}`,
        type: "normal",
        grid_x: gridX,
        grid_y: gridY,
        floor: this.room.floor,
      };

      this.$parent.mapData.addRoom(newRoom);
      this.$parent.mapData.addConnection({room_a: this.room.id, room_b: newRoom.id});
    },
    connectToRoom(targetRoom) {
      const existingConnection = this.$parent.mapData.connections.find(
          (c) =>
              (c.room_a === this.room.id && c.room_b === targetRoom.id) ||
              (c.room_b === this.room.id && c.room_a === targetRoom.id)
      );

      if (!existingConnection) {
        this.$parent.mapData.addConnection({room_a: this.room.id, room_b: targetRoom.id});
      }
    },
    getArrowStyle(direction) {
      const arrowOffset = 0.2 * this.cellSize; // Adjust for arrow placement
      const styles = {
        north: {top: `-${arrowOffset}px`, left: `${this.cellSize / 2 - 5}px`},
        northeast: {top: `-${arrowOffset}px`, left: `${this.cellSize - arrowOffset}px`},
        east: {top: `${this.cellSize / 2 - 5}px`, left: `${this.cellSize}px`},
        southeast: {top: `${this.cellSize - arrowOffset}px`, left: `${this.cellSize - arrowOffset}px`},
        south: {top: `${this.cellSize}px`, left: `${this.cellSize / 2 - 5}px`},
        southwest: {top: `${this.cellSize - arrowOffset}px`, left: `-${arrowOffset}px`},
        west: {top: `${this.cellSize / 2 - 5}px`, left: `-${arrowOffset}px`},
        northwest: {top: `-${arrowOffset}px`, left: `-${arrowOffset}px`},
      };

      return styles[direction];
    },
  },
};
</script>

<style>
.room {
  position: absolute;
  width: 50px;
  height: 50px;
  background: lightblue;
  border: 1px solid #000;
  text-align: center;
  line-height: 50px;
}

.room-name {
  position: relative;
  z-index: 1;
}

.arrow {
  position: absolute;
  width: 10px;
  height: 10px;
  background: orange;
  cursor: pointer;
  border-radius: 50%;
}

.arrow:hover {
  background: red;
}
</style>
