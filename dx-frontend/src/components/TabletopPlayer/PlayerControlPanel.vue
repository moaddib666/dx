<template>
  <div class="player-control-panel">
    <h3 class="panel-title">Player Control</h3>

    <!-- Spawn Player Section -->
    <div class="control-section">
      <h4 class="section-title">Spawn Player/NPC</h4>
      <div class="form-group">
        <label>Name:</label>
        <input
          v-model="newPlayerName"
          type="text"
          class="form-input"
          placeholder="Player name"
        />
      </div>
      <div class="form-group">
        <label>Action Points:</label>
        <input
          v-model.number="newPlayerActionPoints"
          type="number"
          class="form-input"
          min="1"
          max="100"
        />
      </div>
      <div class="form-group">
        <label>Character Image URL (optional):</label>
        <input
          v-model="newPlayerImage"
          type="text"
          class="form-input"
          placeholder="https://example.com/character.png"
        />
      </div>
      <div class="spawner-info">
        <p class="info-text">
          <span class="info-icon">ℹ️</span>
          Players spawn randomly on Player Spawners ({{ playerSpawnerCount }})
        </p>
        <p class="info-text">
          <span class="info-icon">ℹ️</span>
          NPCs spawn randomly on NPC Spawners ({{ npcSpawnerCount }})
        </p>
      </div>
      <div class="button-group">
        <button
          class="action-btn spawn-btn player-spawn-btn"
          @click="handleSpawnPlayer"
          :disabled="playerSpawnerCount === 0"
        >
          <span class="btn-icon">👤</span>
          Spawn Player
        </button>
        <button
          class="action-btn spawn-btn npc-spawn-btn"
          @click="handleSpawnNPC"
          :disabled="npcSpawnerCount === 0"
        >
          <span class="btn-icon">👹</span>
          Spawn NPC
        </button>
      </div>
    </div>

    <!-- Players List -->
    <div class="control-section">
      <h4 class="section-title">Spawned Players ({{ players.length }})</h4>
      <div v-if="players.length === 0" class="no-players">
        <p>No players spawned yet</p>
      </div>
      <div v-else class="players-list">
        <div
          v-for="player in players"
          :key="player.id"
          class="player-item"
          :class="{ selected: selectedPlayer && selectedPlayer.id === player.id }"
          @click="handleSelectPlayer(player.id)"
        >
          <div class="player-info">
            <div class="player-name">{{ player.name }}</div>
            <div class="player-position">
              Position: ({{ player.x }}, {{ player.y }}, L{{ player.layer }})
            </div>
            <div class="player-ap">
              AP: {{ player.currentActionPoints }} / {{ player.maxActionPoints }}
            </div>
          </div>
          <div class="player-actions">
            <button
              class="icon-btn refill-btn"
              @click.stop="handleRefillActionPoints(player.id)"
              title="Refill Action Points"
            >
              🔋
            </button>
            <button
              class="icon-btn remove-btn"
              @click.stop="handleRemovePlayer(player.id)"
              title="Remove Player"
            >
              ❌
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Player Details -->
    <div v-if="selectedPlayer" class="control-section">
      <h4 class="section-title">Selected Player</h4>
      <div class="player-details">
        <div class="detail-row">
          <span class="detail-label">Name:</span>
          <span class="detail-value">{{ selectedPlayer.name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Position:</span>
          <span class="detail-value">
            ({{ selectedPlayer.x }}, {{ selectedPlayer.y }}, Layer {{ selectedPlayer.layer }})
          </span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Action Points:</span>
          <span class="detail-value">
            {{ selectedPlayer.currentActionPoints }} / {{ selectedPlayer.maxActionPoints }}
          </span>
        </div>
        <div class="action-buttons">
          <button class="action-btn" @click="handleRefillActionPoints(selectedPlayer.id)">
            <span class="btn-icon">🔋</span>
            Refill AP
          </button>
          <button class="action-btn danger-btn" @click="handleRemovePlayer(selectedPlayer.id)">
            <span class="btn-icon">🗑️</span>
            Remove
          </button>
        </div>
      </div>
    </div>

    <!-- Grid Controls -->
    <div class="control-section">
      <h4 class="section-title">Display Options</h4>
      <div class="toggle-group">
        <label class="toggle-label">
          <input
            type="checkbox"
            :checked="gridVisible"
            @change="toggleGridVisibility"
          />
          <span>Show Grid</span>
        </label>
        <label class="toggle-label">
          <input
            type="checkbox"
            :checked="backgroundVisible"
            @change="toggleBackgroundVisibility"
          />
          <span>Show Background</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'PlayerControlPanel',
  data() {
    return {
      newPlayerName: '',
      newPlayerActionPoints: 10,
      newPlayerImage: ''
    };
  },
  computed: {
    ...mapGetters('tabletopPlayer', [
      'currentMap',
      'players',
      'selectedPlayer',
      'gridVisible',
      'backgroundVisible',
      'gridConfig',
      'currentLayer'
    ]),
    playerSpawnerCells() {
      if (!this.currentMap || !this.currentMap.cells) return [];
      return this.currentMap.cells.filter(cell =>
        cell.spawner &&
        cell.spawner.type === 'player' &&
        cell.layer === this.currentLayer
      );
    },
    npcSpawnerCells() {
      if (!this.currentMap || !this.currentMap.cells) return [];
      return this.currentMap.cells.filter(cell =>
        cell.spawner &&
        cell.spawner.type === 'npc' &&
        cell.layer === this.currentLayer
      );
    },
    playerSpawnerCount() {
      return this.playerSpawnerCells.length;
    },
    npcSpawnerCount() {
      return this.npcSpawnerCells.length;
    }
  },
  methods: {
    ...mapActions('tabletopPlayer', [
      'spawnPlayer',
      'removePlayer',
      'selectPlayer',
      'refillActionPoints',
      'toggleGridVisibility',
      'toggleBackgroundVisibility'
    ]),

    getRandomSpawner(spawnerCells) {
      if (!spawnerCells || spawnerCells.length === 0) return null;
      const randomIndex = Math.floor(Math.random() * spawnerCells.length);
      return spawnerCells[randomIndex];
    },

    handleSpawnPlayer() {
      if (!this.newPlayerName.trim()) {
        alert('Please enter a player name');
        return;
      }

      if (!this.currentMap) {
        alert('No map loaded');
        return;
      }

      if (this.playerSpawnerCount === 0) {
        alert('No player spawners found on current layer. Please add player spawners in the Map Editor.');
        return;
      }

      // Get random player spawner
      const spawner = this.getRandomSpawner(this.playerSpawnerCells);
      if (!spawner) {
        alert('Failed to find player spawner');
        return;
      }

      this.spawnPlayer({
        x: spawner.x,
        y: spawner.y,
        layer: spawner.layer,
        name: this.newPlayerName.trim(),
        image: this.newPlayerImage.trim() || null,
        actionPoints: this.newPlayerActionPoints
      });

      // Reset form
      this.newPlayerName = '';
      this.newPlayerActionPoints = 10;
      this.newPlayerImage = '';
    },

    handleSpawnNPC() {
      if (!this.newPlayerName.trim()) {
        alert('Please enter an NPC name');
        return;
      }

      if (!this.currentMap) {
        alert('No map loaded');
        return;
      }

      if (this.npcSpawnerCount === 0) {
        alert('No NPC spawners found on current layer. Please add NPC spawners in the Map Editor.');
        return;
      }

      // Get random NPC spawner
      const spawner = this.getRandomSpawner(this.npcSpawnerCells);
      if (!spawner) {
        alert('Failed to find NPC spawner');
        return;
      }

      this.spawnPlayer({
        x: spawner.x,
        y: spawner.y,
        layer: spawner.layer,
        name: this.newPlayerName.trim(),
        image: this.newPlayerImage.trim() || null,
        actionPoints: this.newPlayerActionPoints
      });

      // Reset form
      this.newPlayerName = '';
      this.newPlayerActionPoints = 10;
      this.newPlayerImage = '';
    },

    handleSelectPlayer(playerId) {
      this.selectPlayer(playerId);
    },

    handleRefillActionPoints(playerId) {
      this.refillActionPoints(playerId);
    },

    handleRemovePlayer(playerId) {
      if (confirm('Are you sure you want to remove this player?')) {
        this.removePlayer(playerId);
      }
    }
  }
};
</script>

<style scoped>
.player-control-panel {
  background: rgba(20, 20, 30, 0.95);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  padding: 15px;
  color: #e0e0e0;
  max-height: 600px;
  overflow-y: auto;
}

.panel-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.control-section {
  background: rgba(40, 40, 60, 0.4);
  border: 1px solid rgba(100, 100, 150, 0.2);
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 15px;
}

.section-title {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group {
  margin-bottom: 10px;
}

.form-group label {
  display: block;
  font-size: 12px;
  color: #aaa;
  margin-bottom: 4px;
}

.form-input {
  width: 100%;
  background: rgba(40, 40, 60, 0.8);
  border: 1px solid rgba(100, 100, 150, 0.5);
  border-radius: 4px;
  padding: 6px 8px;
  color: #fff;
  font-size: 13px;
}

.form-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

.action-btn {
  width: 100%;
  background: rgba(0, 212, 255, 0.2);
  border: 2px solid #00d4ff;
  border-radius: 4px;
  padding: 8px;
  color: #00d4ff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 10px;
}

.action-btn:hover {
  background: rgba(0, 212, 255, 0.3);
  transform: scale(1.02);
}

.spawner-info {
  background: rgba(60, 60, 80, 0.5);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.info-text {
  font-size: 12px;
  color: #aaa;
  margin: 4px 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-icon {
  font-size: 14px;
}

.button-group {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.button-group .action-btn {
  flex: 1;
  margin-top: 0;
}

.spawn-btn {
  background: rgba(0, 255, 0, 0.2);
  border-color: #00ff00;
  color: #00ff00;
}

.spawn-btn:hover:not(:disabled) {
  background: rgba(0, 255, 0, 0.3);
}

.spawn-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.player-spawn-btn {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  color: #00d4ff;
}

.player-spawn-btn:hover:not(:disabled) {
  background: rgba(0, 212, 255, 0.3);
}

.npc-spawn-btn {
  background: rgba(255, 100, 0, 0.2);
  border-color: #ff6400;
  color: #ff6400;
}

.npc-spawn-btn:hover:not(:disabled) {
  background: rgba(255, 100, 0, 0.3);
}

.danger-btn {
  background: rgba(255, 0, 0, 0.2);
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.danger-btn:hover {
  background: rgba(255, 0, 0, 0.3);
}

.btn-icon {
  font-size: 16px;
}

.no-players {
  text-align: center;
  padding: 20px;
  color: #888;
  font-size: 13px;
}

.players-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.player-item {
  background: rgba(60, 60, 80, 0.5);
  border: 2px solid rgba(100, 100, 150, 0.3);
  border-radius: 4px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.player-item:hover {
  background: rgba(80, 80, 100, 0.6);
  border-color: rgba(0, 212, 255, 0.5);
}

.player-item.selected {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
}

.player-info {
  flex: 1;
}

.player-name {
  font-size: 14px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 4px;
}

.player-position,
.player-ap {
  font-size: 11px;
  color: #aaa;
  margin-bottom: 2px;
}

.player-actions {
  display: flex;
  gap: 6px;
}

.icon-btn {
  background: rgba(60, 60, 80, 0.8);
  border: 1px solid rgba(100, 100, 150, 0.5);
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.icon-btn:hover {
  transform: scale(1.1);
}

.refill-btn:hover {
  background: rgba(0, 255, 0, 0.3);
  border-color: #00ff00;
}

.remove-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  border-color: #ff6b6b;
}

.player-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid rgba(100, 100, 150, 0.1);
}

.detail-label {
  font-size: 12px;
  color: #aaa;
}

.detail-value {
  font-size: 12px;
  color: #fff;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.action-buttons .action-btn {
  flex: 1;
  margin-top: 0;
}

.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #e0e0e0;
}

.toggle-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* Scrollbar styling */
.player-control-panel::-webkit-scrollbar {
  width: 6px;
}

.player-control-panel::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
  border-radius: 3px;
}

.player-control-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 3px;
}

.player-control-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}
</style>
