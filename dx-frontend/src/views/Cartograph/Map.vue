<template>
  <div id="map-container">
    <!-- Canvas for Map -->
    <canvas
        ref="mapCanvas"
        @mousedown="handleCanvasMouseDown"
        @mouseleave="handleMouseUp"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @wheel="handleZoom"
    ></canvas>

    <!-- Control Panel -->
    <div id="control-panel">
      <button @click="resetMap">New Map</button>
      <button @click="toggleDragMode">{{ dragMode ? "Interaction Mode" : "Drag Mode" }}</button>
    </div>

    <!-- Cell Details -->
    <div id="details-panel">
      <h3>Selected Cells</h3>
      <div v-if="selectedCells.length === 0">No cells selected</div>
      <div v-for="cell in selectedCells" :key="cell.id">
        <p><strong>Room:</strong> {{ cell.name }}</p>
        <p><strong>Position:</strong> ({{ cell.grid_x }}, {{ cell.grid_y }})</p>
        <p><strong>Floor:</strong> {{ cell.floor }}</p>
      </div>

      <div v-if="selectedCells.length > 0">
        <button @click="deleteSelectedRooms">Delete Selected Room(s)</button>
        <button @click="deleteAllConnections">Delete All Connections</button>
      </div>

      <div v-if="selectedCells.length === 2">
        <button @click="toggleConnection">
          {{ areConnected(selectedCells[0], selectedCells[1]) ? "Disconnect" : "Connect" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import MapData from "@/utils/mapData";

export default {
  data() {
    return {
      mapData: MapData,
      currentFloor: 0,
      scale: 1, // Scale for zooming
      pan: {x: 0, y: 0}, // Pan offset
      dragMode: false, // Toggle for dragging mode
      isDragging: false, // Whether dragging is active
      lastMouse: {x: 0, y: 0}, // Last mouse position for dragging
      cellSize: 80, // Size of each grid cell
      selectedCells: [], // Currently selected cells
      lastActiveRoom: null, // Track the last created or selected room
    };
  },
  computed: {
    filteredRooms() {
      return this.mapData.rooms.filter((room) => room.floor === this.currentFloor);
    },
    filteredConnections() {
      return this.mapData.connections.filter((connection) => {
        const startRoom = this.getRoomById(connection.room_a);
        const endRoom = this.getRoomById(connection.room_b);
        return startRoom.floor === this.currentFloor && endRoom.floor === this.currentFloor;
      });
    },
  },
  methods: {
    deleteSelectedRooms() {
      // Delete all selected rooms
      this.selectedCells.forEach((room) => {
        // Remove all connections involving this room
        this.mapData.connections = this.mapData.connections.filter(
            (connection) => connection.room_a !== room.id && connection.room_b !== room.id
        );

        // Remove the room itself
        this.mapData.rooms = this.mapData.rooms.filter((r) => r.id !== room.id);
      });

      // Clear the selection
      this.selectedCells = [];

      // Redraw the canvas
      this.drawCanvas();
    },
    deleteAllConnections() {
      // Remove all connections for the selected rooms
      this.selectedCells.forEach((room) => {
        this.mapData.connections = this.mapData.connections.filter(
            (connection) => connection.room_a !== room.id && connection.room_b !== room.id
        );
      });

      // Redraw the canvas
      this.drawCanvas();
    },
    drawCanvas() {
      const canvas = this.$refs.mapCanvas;
      const ctx = canvas.getContext("2d");

      // Clear the canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Apply pan and zoom
      ctx.save();
      ctx.translate(this.pan.x, this.pan.y);
      ctx.scale(this.scale, this.scale);

      // Draw grid
      this.drawGrid(ctx);

      // Draw connections
      this.filteredConnections.forEach((connection) => {
        const startRoom = this.getRoomById(connection.room_a);
        const endRoom = this.getRoomById(connection.room_b);
        this.drawConnection(ctx, startRoom, endRoom);
      });

      // Draw rooms
      this.filteredRooms.forEach((room) => {
        this.drawRoom(ctx, room);
      });

      ctx.restore();
    },
    drawGrid(ctx) {
      const canvas = this.$refs.mapCanvas;
      const cellSize = this.cellSize;

      ctx.strokeStyle = "#b8ea7c"; // Light green grid lines
      ctx.lineWidth = 0.5;

      // Center the grid around (0, 0)
      const halfWidth = canvas.width / (2 * this.scale);
      const halfHeight = canvas.height / (2 * this.scale);

      const minX = -Math.ceil(halfWidth / cellSize) * cellSize;
      const maxX = Math.ceil(halfWidth / cellSize) * cellSize;
      const minY = -Math.ceil(halfHeight / cellSize) * cellSize;
      const maxY = Math.ceil(halfHeight / cellSize) * cellSize;

      // Draw vertical lines (X-axis)
      for (let x = minX; x <= maxX; x += cellSize) {
        ctx.beginPath();
        ctx.moveTo(x, minY);
        ctx.lineTo(x, maxY);
        ctx.stroke();
      }

      // Draw horizontal lines (Y-axis)
      for (let y = minY; y <= maxY; y += cellSize) {
        ctx.beginPath();
        ctx.moveTo(minX, y);
        ctx.lineTo(maxX, y);
        ctx.stroke();
      }

      // Draw axes (0,0 reference lines)
      ctx.strokeStyle = "#ffa500"; // Orange for axes
      ctx.lineWidth = 1;

      // X-axis
      ctx.beginPath();
      ctx.moveTo(minX, 0);
      ctx.lineTo(maxX, 0);
      ctx.stroke();

      // Y-axis
      ctx.beginPath();
      ctx.moveTo(0, minY);
      ctx.lineTo(0, maxY);
      ctx.stroke();
    },
    drawRoom(ctx, room) {
      const x = room.grid_x * this.cellSize;
      const y = room.grid_y * this.cellSize;

      // Room Rectangle
      ctx.fillStyle = this.selectedCells.includes(room) ? "yellow" : "lightblue";
      ctx.fillRect(x + 10, y + 10, this.cellSize - 20, this.cellSize - 20);

      // Room Border
      ctx.strokeStyle = "#004080";
      ctx.lineWidth = 2;
      ctx.strokeRect(x + 10, y + 10, this.cellSize - 20, this.cellSize - 20);

      // Room Name
      ctx.fillStyle = "black";
      ctx.font = "14px Arial";
      ctx.textAlign = "center";
      ctx.fillText(room.name, x + this.cellSize / 2, y + this.cellSize / 2 + 5);
    },
    drawConnection(ctx, startRoom, endRoom) {
      const startX = startRoom.grid_x * this.cellSize + this.cellSize / 2;
      const startY = startRoom.grid_y * this.cellSize + this.cellSize / 2;
      const endX = endRoom.grid_x * this.cellSize + this.cellSize / 2;
      const endY = endRoom.grid_y * this.cellSize + this.cellSize / 2;

      ctx.strokeStyle = "red";
      ctx.lineWidth = 3;

      ctx.beginPath();
      ctx.moveTo(startX, startY);
      ctx.lineTo(endX, endY);
      ctx.stroke();
    },
    isAdjacent(roomA, roomB) {
      const dx = Math.abs(roomA.grid_x - roomB.grid_x);
      const dy = Math.abs(roomA.grid_y - roomB.grid_y);

      // Rooms are adjacent if they share a side or corner (dx <= 1 and dy <= 1)
      return dx <= 1 && dy <= 1;
    },
    handleCanvasMouseDown(event) {
      const canvas = this.$refs.mapCanvas;
      const rect = canvas.getBoundingClientRect();
      const mouseX = (event.clientX - rect.left - this.pan.x) / this.scale;
      const mouseY = (event.clientY - rect.top - this.pan.y) / this.scale;

      const gridX = Math.floor(mouseX / this.cellSize);
      const gridY = Math.floor(mouseY / this.cellSize);

      if (this.dragMode || event.button === 1) {
        this.isDragging = true;
        this.lastMouse = {x: event.clientX, y: event.clientY};
      } else {
        const existingRoom = this.mapData.rooms.find(
            (room) => room.grid_x === gridX && room.grid_y === gridY && room.floor === this.currentFloor
        );

        if (existingRoom) {
          // Handle room selection
          if (event.shiftKey) {
            if (this.selectedCells.includes(existingRoom)) {
              this.selectedCells = this.selectedCells.filter((r) => r !== existingRoom);
            } else if (this.selectedCells.length < 2) {
              this.selectedCells.push(existingRoom);
            }
          } else {
            this.selectedCells = [existingRoom];
            this.lastActiveRoom = existingRoom; // Update last active room
          }
        } else {
          // Handle empty cell: create a new room
          const newRoom = {
            id: Date.now(),
            name: `Room ${this.mapData.rooms.length + 1}`,
            type: "normal",
            grid_x: gridX,
            grid_y: gridY,
            floor: this.currentFloor,
          };
          this.mapData.addRoom(newRoom);

          // Connect to the last active room if available
          if (this.lastActiveRoom && this.isAdjacent(this.lastActiveRoom, newRoom)) {
            this.mapData.addConnection({
              room_a: newRoom.id,
              room_b: this.lastActiveRoom.id,
            });
          }

          // Update last active room
          this.lastActiveRoom = newRoom;

          this.drawCanvas();
        }
      }

      this.drawCanvas();
    },
    handleMouseMove(event) {
      if (this.isDragging) {
        const dx = event.clientX - this.lastMouse.x;
        const dy = event.clientY - this.lastMouse.y;
        this.pan.x += dx;
        this.pan.y += dy;
        this.lastMouse = {x: event.clientX, y: event.clientY};
        this.drawCanvas();
      }
    },
    handleMouseUp() {
      this.isDragging = false;
    },
    handleZoom(event) {
      event.preventDefault();
      const zoomFactor = 0.1;
      if (event.deltaY < 0) {
        this.scale = Math.min(this.scale + zoomFactor, 3); // Max zoom
      } else {
        this.scale = Math.max(this.scale - zoomFactor, 0.5); // Min zoom
      }
      this.drawCanvas();
    },
    resetMap() {
      if (confirm("Are you sure you want to reset the map?")) {
        this.mapData.clear();
        this.drawCanvas();
      }
    },
    toggleDragMode() {
      this.dragMode = !this.dragMode;
    },
    areConnected(room1, room2) {
      return this.mapData.connections.some(
          (connection) =>
              (connection.room_a === room1.id && connection.room_b === room2.id) ||
              (connection.room_b === room1.id && connection.room_a === room2.id)
      );
    },
    toggleConnection() {
      const [room1, room2] = this.selectedCells;
      if (this.areConnected(room1, room2)) {
        this.mapData.connections = this.mapData.connections.filter(
            (connection) =>
                !(
                    (connection.room_a === room1.id && connection.room_b === room2.id) ||
                    (connection.room_b === room1.id && connection.room_a === room2.id)
                )
        );
      } else {
        this.mapData.addConnection({room_a: room1.id, room_b: room2.id});
      }
      this.drawCanvas();
    },
    getRoomById(id) {
      return MapData.getRoomById(id);
    },
  },
  mounted() {
    const canvas = this.$refs.mapCanvas;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    MapData.load();

    this.drawCanvas();

    // Redraw on resize
    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      this.drawCanvas();
    });
  },
};
</script>

<style>
#map-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

canvas {
  width: 100%;
  height: 100%;
  cursor: pointer;
}

#control-panel {
  position: absolute;
  top: 10px;
  left: 10px;
  background: white;
  border: 1px solid #ddd;
  padding: 5px;
  border-radius: 5px;
}

#details-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 220px;
  background: #222; /* Dark background */
  color: white; /* White text */
  border: 1px solid #444;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

#details-panel button {
  background: #444; /* Button background */
  color: white; /* Button text color */
  border: 1px solid #555;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
  margin: 5px 0;
}

#details-panel button:hover {
  background: #555;
}

</style>
