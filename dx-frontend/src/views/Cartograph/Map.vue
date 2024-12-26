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
      <button @click="exportMap">Export</button>
      <input ref="importInput" style="display:none" type="file" @change="importMap">
      <button @click="$refs.importInput.click()">Import</button>
      <div>
        <label for="floor-select">Floor:</label>
        <span>{{ currentFloor }}</span>
        <button @click="switchFloor(currentFloor +1)">Up</button>
        <button @click="switchFloor(currentFloor -1)">Down</button>
      </div>
      <button @click="syncAdminMapData">Sync</button>
    </div>

    <div id="loader" v-if="loading">
      <h2>Loading...</h2>
    </div>

    <!-- Characters Panel -->
    <div id="character-panel" v-if="selectedCells.length === 1 && charactersInRoom.length > 0">
      <div>
        <h3>Players:</h3>
        <div v-if="playersInRoom.length > 0">
          <div
              v-for="player in playersInRoom"
              :key="player.id"
              class="character-row"
              @click="onCharacterClick(player.id)"
          >
            <div class="avatar-placeholder">
              <img :src="player.avatar" :alt="player.name + ' avatar'" />
            </div>
            <span class="character-name">{{ player.name }}</span>
          </div>
        </div>
        <div v-else>
          <p>No players in this room</p>
        </div>
      </div>

      <div>
        <h3>NPCs:</h3>
        <div v-if="npcsInRoom.length > 0">
          <div
              v-for="npc in npcsInRoom"
              :key="npc.id"
              class="character-row"
              @click="onCharacterClick(npc.id)"
          >
            <div class="avatar-placeholder"></div>
            <span class="character-name">{{ npc.name }}</span>
          </div>
        </div>
        <div v-else>
          <p>No NPCs in this room</p>
        </div>
      </div>
    </div>

    <!-- Cell Details -->
    <div id="details-panel">
      <h3>Selected Cells</h3>
      <div v-if="selectedCells.length === 0">No cells selected</div>
      <div v-for="cell in selectedCells" :key="cell.id">
        <p><strong>Id:</strong> {{ cell.id }}</p>
        <p><strong>Room:</strong> {{ cell.name }}</p>
        <p><strong>Position:</strong> ({{ cell.grid_x }}, {{ cell.grid_y }})</p>
        <p><strong>Floor:</strong> {{ cell.grid_z }}</p>
      </div>

      <div v-if="selectedCells.length > 0">
        <button @click="deleteSelectedRooms">Delete Selected Room(s)</button>
        <button @click="deleteAllConnections">Delete All Connections</button>
      </div>

      <div v-if="selectedCells.length === 1">
        <label for="room-type">Room Type:</label>
        <select id="room-type" v-model="selectedCells[0].type" @change="updateRoom">
          <option v-for="type in Object.values(RoomType)" :key="type" :value="type.value">{{ type.label }}</option>
        </select>
        <label for="room-label">Room Label:</label>
        <select id="room-label" v-model="selectedCells[0].label" @change="updateRoom">
          <option v-for="label in Object.values(RoomLabel)" :key="label" :value="label.value">{{ label.label }}</option>
        </select>
        <button @click="makeStairs(true)">Add Stairs Down</button>
        <button @click="makeStairs(false)">Add Stairs Up</button>
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
import MapData, {RoomLabel, RoomType} from "@/utils/mapData";
import {WorldGameApi} from "@/api/backendService.js";

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
      loading: false,
    };
  },
  computed: {
    charactersInRoom() {
      if (this.selectedCells.length !== 1) return [];
      return this.mapData.getCharactersInRoom(this.selectedCells[0]);
    },
    playersInRoom() {
      return this.charactersInRoom.filter((character) => !character.npc);
    },
    npcsInRoom() {
      return this.charactersInRoom.filter((character) => character.npc);
    },
    RoomLabel() {
      return RoomLabel
    },
    RoomType() {
      return RoomType
    },
    filteredRooms() {
      return this.mapData.rooms.filter((room) => room.grid_z === this.currentFloor);
    },
    filteredConnections() {
      return this.mapData.getValidConnections(this.currentFloor);
    },
    filteredVerticalConnections() {
      return this.mapData.getValidVerticalConnections(this.currentFloor);
    },
  },
  methods: {
    onCharacterClick(characterId) {
      console.log("Character clicked:", characterId);
      // Replace with your action logic
      alert(`Character ID: ${characterId}`);
    },
    async syncAdminMapData() {
      try {
        this.loading = true;
        const data = (await (WorldGameApi.worldPositionMapRetrieve())).data;
        console.log({data});
        this.mapData.clear();
        this.mapData.fromJSON(data);
        this.drawCanvas();
      } catch (err) {
        console.error("Error parsing JSON file", err);
        alert("Error parsing JSON file");
      } finally {
        this.loading = false;
      }

    },
    updateRoom() {
      const updatedRoom = this.selectedCells[0];
      this.mapData.updateRoom(updatedRoom);
      this.drawCanvas();
    },
    switchFloor(floor) {
      this.currentFloor = floor;
      this.drawCanvas();
    },
    makeStairs(down) {
      if (this.selectedCells.length !== 1) {
        alert("Select a single room to add stairs");
        return;
      }

      const updatedRoom = this.selectedCells[0];
      const currentFloor = updatedRoom.grid_z;
      const targetFloor = down ? currentFloor - 1 : currentFloor + 1;

      const targetRoom = this.mapData.createRoomIfNotExists(updatedRoom.name, updatedRoom.grid_x, updatedRoom.grid_y, targetFloor);
      console.log("Adding stairs between", updatedRoom, targetRoom);
      const connection = {room_a: updatedRoom.id, room_b: targetRoom.id};
      this.mapData.addVerticalConnection(connection);
      this.drawCanvas();
    },
    exportMap() {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(this.mapData.toJSON());
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute('href', dataStr);
      dlAnchor.setAttribute('download', 'map_export.json');
      dlAnchor.click();
    },
    importMap(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        console.log(e.target);
        try {
          const data = JSON.parse(e.target.result);
          this.mapData.clear();
          this.mapData.fromJSON(data);
          this.drawCanvas();
        } catch (err) {
          console.error("Error parsing JSON file", err);
          alert("Error parsing JSON file");
        }
      };
      reader.readAsText(file);
      // empty the input value to allow the same file to be selected again
      event.target.value = "";
    },
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
        this.drawRoomCharacters(ctx, room);
      });

      // Draw vertical connections
      this.filteredVerticalConnections.forEach((connection) => {
        const startRoom = this.getRoomById(connection.room_a);
        const endRoom = this.getRoomById(connection.room_b);
        const visibleRoom = startRoom.grid_z === this.currentFloor ? startRoom : endRoom;
        const invisibleRoom = startRoom.grid_z === this.currentFloor ? endRoom : startRoom;
        this.drawStairs(ctx, visibleRoom, visibleRoom.grid_z > invisibleRoom.grid_z);
      });


      ctx.restore();
      this.drawCompass(ctx);
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

      // Room Dimensions and Rounded Corners
      const rectX = x + 10;
      const rectY = y + 10;
      const rectWidth = this.cellSize - 20;
      const rectHeight = this.cellSize - 20;
      const cornerRadius = 10;

      // Check if an icon is set for the room
      const icon = RoomLabel.getIcon(room.label);

      if (icon !== undefined && icon.complete) {
        // Use the icon as the background
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(rectX + cornerRadius, rectY);
        ctx.lineTo(rectX + rectWidth - cornerRadius, rectY);
        ctx.quadraticCurveTo(rectX + rectWidth, rectY, rectX + rectWidth, rectY + cornerRadius);
        ctx.lineTo(rectX + rectWidth, rectY + rectHeight - cornerRadius);
        ctx.quadraticCurveTo(rectX + rectWidth, rectY + rectHeight, rectX + rectWidth - cornerRadius, rectY + rectHeight);
        ctx.lineTo(rectX + cornerRadius, rectY + rectHeight);
        ctx.quadraticCurveTo(rectX, rectY + rectHeight, rectX, rectY + rectHeight - cornerRadius);
        ctx.lineTo(rectX, rectY + cornerRadius);
        ctx.quadraticCurveTo(rectX, rectY, rectX + cornerRadius, rectY);
        ctx.closePath();
        ctx.clip();

        // Draw the icon scaled to fit the room
        ctx.drawImage(icon, rectX, rectY, rectWidth, rectHeight);
        ctx.restore();
      } else {
        // Gradient Fill if no icon is set
        const gradient = ctx.createLinearGradient(rectX, rectY, rectX + rectWidth, rectY + rectHeight);

        if (this.selectedCells.includes(room)) {
          gradient.addColorStop(0, "#FFD700"); // Gold
          gradient.addColorStop(1, "#FF8C00"); // Dark Orange
        } else {
          switch (room.type) {
            case RoomType.DEFAULT.value:
              gradient.addColorStop(0, "#333333"); // Dark Gray
              gradient.addColorStop(1, "#555555"); // Slightly Lighter Gray
              break;

            case RoomType.START.value:
              gradient.addColorStop(0, "#228B22"); // Forest Green
              gradient.addColorStop(1, "#32CD32"); // Lime Green
              break;

            case RoomType.END.value:
              gradient.addColorStop(0, "#1E90FF"); // Dodger Blue
              gradient.addColorStop(1, "#87CEFA"); // Light Sky Blue
              break;

            case RoomType.BOSS.value:
              gradient.addColorStop(0, "#8B0000"); // Dark Red
              gradient.addColorStop(1, "#FF6347"); // Tomato Red
              break;

            case RoomType.HUB.value:
              gradient.addColorStop(0, "#8B008B"); // Dark Magenta
              gradient.addColorStop(1, "#DA70D6"); // Orchid
              break;

            default:
              gradient.addColorStop(0, "#444"); // Dark Gray
              gradient.addColorStop(1, "#666"); // Medium Gray
              break;
          }
        }

        ctx.fillStyle = gradient;

        // Draw Rounded Rectangle
        ctx.beginPath();
        ctx.moveTo(rectX + cornerRadius, rectY);
        ctx.lineTo(rectX + rectWidth - cornerRadius, rectY);
        ctx.quadraticCurveTo(rectX + rectWidth, rectY, rectX + rectWidth, rectY + cornerRadius);
        ctx.lineTo(rectX + rectWidth, rectY + rectHeight - cornerRadius);
        ctx.quadraticCurveTo(rectX + rectWidth, rectY + rectHeight, rectX + rectWidth - cornerRadius, rectY + rectHeight);
        ctx.lineTo(rectX + cornerRadius, rectY + rectHeight);
        ctx.quadraticCurveTo(rectX, rectY + rectHeight, rectX, rectY + rectHeight - cornerRadius);
        ctx.lineTo(rectX, rectY + cornerRadius);
        ctx.quadraticCurveTo(rectX, rectY, rectX + cornerRadius, rectY);
        ctx.closePath();
        ctx.fill();
      }

      // Room Border
      ctx.strokeStyle = this.selectedCells.includes(room) ? "#FF4500" : "#666"; // Orange for selected, gray otherwise
      ctx.lineWidth = 3;
      ctx.stroke();

      // Room Name
      ctx.fillStyle = "#FFF"; // White text for contrast
      ctx.font = "bold 10px Arial";
      ctx.textAlign = "center";
      ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
      ctx.shadowBlur = 4;
      ctx.fillText(room.name, x + this.cellSize / 2, y + this.cellSize * 0.9);

      // Reset shadow
      ctx.shadowBlur = 0;
    },
    drawRoomCharacters(ctx, room) {
      const characters = this.mapData.getCharactersInRoom(room);

      const npcCount = characters.filter((character) => character.npc).length;
      const playerCount = characters.length - npcCount; // Total characters minus NPCs

      if (npcCount === 0 && playerCount === 0) return; // Nothing to draw if no characters

      const x = room.grid_x * this.cellSize + this.cellSize / 2; // Center X of the room
      const y = room.grid_y * this.cellSize + this.cellSize / 2; // Center Y of the room

      const circleRadius = 15; // Base radius for both indicators
      const spacing = 25; // Spacing between the two indicators

      // NPC Indicator
      if (npcCount > 0) {
        const npcX = x - spacing; // Left position for NPC indicator
        ctx.fillStyle = "rgb(255, 127, 80)"; // Coral color for NPCs
        ctx.beginPath();
        ctx.arc(npcX, y, circleRadius, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();

        // NPC Count Text
        ctx.fillStyle = "#FFF"; // White text
        ctx.font = "bold 14px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(npcCount, npcX, y);
      }

      // Player Indicator
      if (playerCount > 0) {
        const playerX = x + spacing; // Right position for Player indicator
        ctx.fillStyle = "rgb(50, 205, 50)"; // Lime green color for Players
        ctx.beginPath();
        ctx.arc(playerX, y, circleRadius, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();

        // Player Count Text
        ctx.fillStyle = "#FFF"; // White text
        ctx.font = "bold 14px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(playerCount, playerX, y);
      }
    },
    drawStairs(ctx, room, down) {
      console.log("Drawing stairs", {room, down});
      const x = room.grid_x * this.cellSize;
      const y = room.grid_y * this.cellSize;

      const radius = 10; // Radius of the circle
      const circleX = x + this.cellSize - radius - 10; // Align to right with padding
      const circleY = down
          ? y + this.cellSize - radius - 10 // Bottom-right corner for down
          : y + radius + 10; // Top-right corner for up

      // Draw circle
      ctx.fillStyle = down ? "#FF4500" : "#32CD32"; // Bright red for down, green for up
      ctx.beginPath();
      ctx.arc(circleX, circleY, radius, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fill();

      // Add arrow indicator
      ctx.fillStyle = "#FFF"; // White arrow for contrast
      ctx.beginPath();
      if (down) {
        // Downward arrow inside the circle
        ctx.moveTo(circleX - 5, circleY - 3); // Top left
        ctx.lineTo(circleX + 5, circleY - 3); // Top right
        ctx.lineTo(circleX, circleY + 5); // Bottom center
      } else {
        // Upward arrow inside the circle
        ctx.moveTo(circleX - 5, circleY + 3); // Bottom left
        ctx.lineTo(circleX + 5, circleY + 3); // Bottom right
        ctx.lineTo(circleX, circleY - 5); // Top center
      }
      ctx.closePath();
      ctx.fill();
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
        const existingRoom = this.mapData.getRoomByCoords(gridX, gridY, this.currentFloor);
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
          const newRoom = this.mapData.createRoomIfNotExists(`Room ${this.mapData.rooms.length + 1}`, gridX, gridY, this.currentFloor);
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
    drawCompass(ctx) {
      const canvas = this.$refs.mapCanvas;

      const compassRadius = 60; // Larger compass radius for clarity
      const padding = 30; // Padding from edges

      // Compass center position (fixed bottom-right corner)
      const centerX = canvas.width - compassRadius - padding;
      const centerY = canvas.height - compassRadius - padding;

      // Draw compass outer circle
      ctx.beginPath();
      ctx.arc(centerX, centerY, compassRadius, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fillStyle = "#1E1E2E"; // Dark background
      ctx.fill();
      ctx.lineWidth = 3;
      ctx.strokeStyle = "#FFF"; // White border
      ctx.stroke();

      // Compass star (4 main points)
      ctx.fillStyle = "#000"; // Black star
      ctx.beginPath();
      ctx.moveTo(centerX, centerY - compassRadius + 10); // Top point
      ctx.lineTo(centerX + 8, centerY); // Center-right
      ctx.lineTo(centerX, centerY + compassRadius - 10); // Bottom point
      ctx.lineTo(centerX - 8, centerY); // Center-left
      ctx.closePath();
      ctx.fill();

      // Compass star (intermediate diagonal points)
      ctx.beginPath();
      ctx.moveTo(centerX - compassRadius / 2, centerY); // Left middle
      ctx.lineTo(centerX, centerY - 8); // Top middle
      ctx.lineTo(centerX + compassRadius / 2, centerY); // Right middle
      ctx.lineTo(centerX, centerY + 8); // Bottom middle
      ctx.closePath();
      ctx.fill();

      // Draw cardinal directions (N, E, S, W)
      ctx.fillStyle = "#FFF"; // White text for visibility
      ctx.font = "bold 18px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      // North
      ctx.fillText("N", centerX, centerY - compassRadius + 20);
      // East
      ctx.fillText("E", centerX + compassRadius - 20, centerY);
      // South
      ctx.fillText("S", centerX, centerY + compassRadius - 20);
      // West
      ctx.fillText("W", centerX - compassRadius + 20, centerY);

      // Add smaller inner circle for aesthetics
      ctx.beginPath();
      ctx.arc(centerX, centerY, compassRadius / 3, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fillStyle = "#333"; // Dark gray for inner circle
      ctx.fill();
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
#character-panel {
  position: absolute;
  bottom: 40px;
  left: 10px;
  width: 250px;
  background: #222; /* Dark background */
  color: white;
  border: 1px solid #444;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-height: calc(100% - 300px); /* Make it fit the screen */
  overflow-y: auto; /* Enable scrolling */
}

h3 {
  margin-bottom: 10px;
}

.character-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.character-row:hover {
  background: #444; /* Highlight on hover */
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  background: #666; /* Placeholder color */
  border-radius: 50%;
  margin-right: 10px;
}

.character-name {
  font-size: 16px;
  font-weight: bold;
}

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
  background: #222; /* Dark background */
  border: 1px solid #444;
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

#loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #222; /* Dark background */
  color: white; /* White text */
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
