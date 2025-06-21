<template>
  <div class="info-section">
    <h4>Entities</h4>
    <div class="entities-container">
      <!-- Players -->
      <div v-if="room.players.length > 0" class="entity-group">
        <div class="entity-header">
          <i class="icon-users" style="color: #00ff00;"></i>
          <span>Players ({{ room.players.length }})</span>
        </div>
        <div class="entity-list">
          <div
              v-for="player in room.players"
              :key="player.id"
              class="entity-item"
              @click="onPlayerClick(player)"
          >
            <div class="entity-avatar">
              <img
                  :src="getPlayerAvatar(player.id)"
                  alt="Player Avatar"
                  class="avatar-image"
                  @error="handleAvatarError"
              />
            </div>
            <div class="entity-info">
              <span class="entity-name">{{ player.name || 'Unknown Player' }}</span>
              <span class="entity-status">{{ player.status || 'Active' }}</span>
            </div>
            <EditInDjangoAdmin
                :id="player.id"
                :app="player.object_type?.app_label || 'world'"
                :model="player.object_type?.model || 'player'"
            />
          </div>
        </div>
      </div>

      <!-- NPCs -->
      <div v-if="room.npcs.length > 0" class="entity-group">
        <div class="entity-header">
          <i class="icon-user-friends" style="color: #ffff00;"></i>
          <span>NPCs ({{ room.npcs.length }})</span>
        </div>
        <div class="entity-list">
          <div
              v-for="npc in room.npcs"
              :key="npc.id"
              class="entity-item"
              @click="onNpcClick(npc)"
          >
            <div class="entity-avatar">
              <img
                  :src="getNpcAvatar(npc.id)"
                  alt="NPC Avatar"
                  class="avatar-image"
                  @error="handleAvatarError"
              />
            </div>
            <div class="entity-info">
              <span class="entity-name">{{ npc.name || 'Unknown NPC' }}</span>
              <span class="entity-type">{{ npc.type || 'Neutral' }}</span>
            </div>
            <EditInDjangoAdmin
                :id="npc.id"
                :app="npc.object_type?.app_label || 'world'"
                :model="npc.object_type?.model || 'npc'"
            />
          </div>
        </div>
      </div>

      <!-- Objects -->
      <div v-if="resolvedRoomObjects.length > 0" class="entity-group">
        <div class="entity-header">
          <i class="icon-cube" style="color: #ff8800;"></i>
          <span>Objects ({{ resolvedRoomObjects.length }})</span>
        </div>
        <div class="entity-list">
          <div
              v-for="object in resolvedRoomObjects"
              :key="object.id"
              class="entity-item"
          >
            <!-- Item Avatar -->
            <div class="entity-avatar">
              <img
                  :src="getItemAvatar(object.resolvedItem)"
                  :alt="object.resolvedItem.name || 'Item'"
                  class="avatar-image"
                  @error="handleAvatarError"
              />
            </div>
            <!-- Simplified Item Info -->
            <div class="entity-info">
              <span class="entity-name">{{ object.resolvedItem.name || 'Unknown Object' }}</span>
              <div class="entity-details">
                <span class="entity-rarity">{{ object.resolvedItem.rarity || 'Common' }}</span>
                <span v-if="object.resolvedItem.charges_left" class="entity-charges">
                  {{ object.resolvedItem.charges_left }}
                </span>
              </div>
            </div>
            <!-- Admin Edit Button -->
            <EditInDjangoAdmin
                :id="object.id"
                :app="object.object_type?.app_label || 'world'"
                :model="object.object_type?.model || 'gameobject'"
            />
          </div>
        </div>
      </div>

      <!-- Anomalies -->
      <div v-if="room.anomalies.length > 0" class="entity-group">
        <div class="entity-header">
          <i class="icon-exclamation-triangle" style="color: #ff0088;"></i>
          <span>Anomalies ({{ room.anomalies.length }})</span>
        </div>
        <div class="entity-list">
          <div
              v-for="anomaly in room.anomalies"
              :key="anomaly.id"
              class="entity-item"
          >
            <div class="entity-info">
              <span class="entity-name">{{ anomaly.name || 'Unknown Anomaly' }}</span>
              <span class="entity-danger">{{ anomaly.danger || 'Low' }}</span>
            </div>
            <EditInDjangoAdmin
                :id="anomaly.id"
                :app="anomaly.object_type?.app_label || 'world'"
                :model="anomaly.object_type?.model || 'anomaly'"
            />
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="!hasEntities" class="empty-entities">
        <p>No entities in this room</p>
      </div>
    </div>
  </div>
</template>

<script>
import EditInDjangoAdmin from '@/components/EditInDjangoAdmin.vue';
import {CharacterInfoGameService} from '@/services/characterInfoService.js';
import {itemsService} from '@/services/ItemsService.js';

export default {
  name: 'Entities',
  components: {
    EditInDjangoAdmin
  },
  props: {
    room: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      playerAvatars: new Map(), // Map to store player avatar URLs
      npcAvatars: new Map(), // Map to store NPC avatar URLs
      // Data URL for a simple colored circle as fallback avatar
      defaultAvatar: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="%23555"/></svg>'
    };
  },
  computed: {
    hasEntities() {
      return this.room.players.length > 0 ||
          this.room.npcs.length > 0 ||
          this.room.objects.length > 0 ||
          this.room.anomalies.length > 0;
    },

    // Compute resolved items for all objects in the room
    resolvedRoomObjects() {
      if (!this.room || !this.room.objects) return [];

      // Map each object to its resolved item
      return this.room.objects.map(object => {
        const resolvedItem = this.resolveItemFromWorldItem(object);
        return {
          ...object, // Keep all original object properties
          resolvedItem // Add the resolved item
        };
      });
    }
  },
  watch: {
    room: {
      handler() {
        this.fetchAvatars();
      },
      immediate: true,
      deep: true
    }
  },
  created() {
    this.fetchAvatars();
    // Initialize the items service
    itemsService.initialize().catch(error => {
      console.error('Failed to initialize ItemsService:', error);
    });
  },
  methods: {
    async fetchAvatars() {
      if (!this.room || !this.room.players || !this.room.npcs) return;

      // Fetch avatars for players
      for (const player of this.room.players) {
        if (player.id && !this.playerAvatars.has(player.id)) {
          try {
            const avatarUrl = await CharacterInfoGameService.getAvatarUrl(player.id, true) || this.defaultAvatar;
            this.playerAvatars.set(player.id, avatarUrl);
          } catch (error) {
            console.error(`Error fetching avatar for player ${player.id}:`, error);
            this.playerAvatars.set(player.id, this.defaultAvatar);
          }
        }
      }

      // Fetch avatars for NPCs
      for (const npc of this.room.npcs) {
        if (npc.id && !this.npcAvatars.has(npc.id)) {
          try {
            const avatarUrl = await CharacterInfoGameService.getAvatarUrl(npc.id, true) || this.defaultAvatar;
            this.npcAvatars.set(npc.id, avatarUrl);
          } catch (error) {
            console.error(`Error fetching avatar for NPC ${npc.id}:`, error);
            this.npcAvatars.set(npc.id, this.defaultAvatar);
          }
        }
      }
    },

    getPlayerAvatar(playerId) {
      return this.playerAvatars.get(playerId) || this.defaultAvatar;
    },

    getNpcAvatar(npcId) {
      return this.npcAvatars.get(npcId) || this.defaultAvatar;
    },

    /**
     * Get avatar URL for an item
     * @param {Object} item - The item object
     * @returns {string} - URL of the item avatar or default placeholder
     */
    getItemAvatar(item) {
      if (!item) return this.defaultAvatar;

      // Check for common image properties in item objects
      // Try different possible property names for item images
      if (item.image_url) return item.image_url;
      if (item.image) return item.image;
      if (item.avatar) return item.avatar;
      if (item.icon) return item.icon;
      if (item.icon_url) return item.icon_url;

      // Generate a colored placeholder based on item rarity
      const rarityColors = {
        'Common': '#aaaaaa',
        'Uncommon': '#55aa55',
        'Rare': '#5555ff',
        'Epic': '#aa55aa',
        'Legendary': '#ffaa00',
        'Artifact': '#ff5555'
      };

      const color = rarityColors[item.rarity] || '#aaaaaa';

      // Create a simple SVG icon with the first letter of the item name
      const firstLetter = (item.name && item.name.length > 0) ? item.name.charAt(0).toUpperCase() : '?';

      return `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><rect width="32" height="32" fill="${color}" rx="4" /><text x="50%" y="50%" font-family="Arial" font-size="16" fill="white" text-anchor="middle" dominant-baseline="middle">${firstLetter}</text></svg>`;
    },

    handleAvatarError(event) {
      event.target.src = this.defaultAvatar;
    },

    onPlayerClick(player) {
      this.$emit('player-click', player);
    },

    onNpcClick(npc) {
      this.$emit('npc-click', npc);
    },

    /**
     * Resolve the actual item from a world item
     * @param {Object} worldItem - The world item object
     * @returns {Object} - The resolved item with additional world item properties
     */
    resolveItemFromWorldItem(worldItem) {
      if (!worldItem) return { name: 'Unknown Object', rarity: 'Common' };

      // Extract the item ID from the world item
      const itemId = worldItem.item;

      if (!itemId) return {
        name: worldItem.name || 'Unknown Object',
        rarity: worldItem.rarity || 'Common',
        id: worldItem.id
      };

      // Get the item details from the items service
      const item = itemsService.getItemById(itemId);

      if (!item) return {
        name: worldItem.name || 'Unknown Object',
        rarity: worldItem.rarity || 'Common',
        id: worldItem.id
      };

      // Return a merged object with item details and world item properties
      return {
        ...item,
        worldItemId: worldItem.id, // Keep the original world item ID
        charges_left: worldItem.charges_left,
        visibility: worldItem.visibility,
        is_active: worldItem.is_active
      };
    }
  }
};
</script>

<style scoped>
.info-section {
}

.entities-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.entity-group {
  background: #2a2a2a;
  border-radius: 6px;
  overflow: hidden;
}

.entity-header {
  background: #222;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
}

.entity-list {
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.entity-item {
  display: flex;
  align-items: center;
  background: #333;
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.entity-item:hover {
  background: #3a3a3a;
}

.entity-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 0.5rem;
  background: #444;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.entity-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-right: 0.5rem;
  overflow: hidden;
}

.entity-name {
  color: #fff;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0.1rem;
}

.entity-details {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.entity-status,
.entity-type,
.entity-rarity,
.entity-danger {
  color: #ccc;
  font-size: 0.8rem;
  font-style: italic;
}

.entity-charges {
  color: #88ccff;
  font-size: 0.8rem;
  font-weight: bold;
  background: rgba(0, 100, 200, 0.2);
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  display: inline-block;
}

.empty-entities {
  text-align: center;
  color: #aaa;
  font-style: italic;
  padding: 2rem;
}
</style>
