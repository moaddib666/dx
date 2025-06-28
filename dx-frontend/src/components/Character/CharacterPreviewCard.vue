<template>
  <div
      class="character-card"
      :class="{
      'inactive': !character.is_active
    }"
      :style="{ backgroundImage: `url(${character.biography.avatar})` }"
  >
    <div class="character-overlay">
      <div class="character-content">
        <h3 class="character-title">{{ character.name }}</h3>
        <div class="character-details">
          <div class="character-path">
            <img v-if="character.path && character.path.icon" :src="character.path.icon" class="path-icon" alt="Path Icon">
            <span>{{ character.path ? character.path.name : 'No Path' }}</span>
          </div>
          <p class="character-bio">{{ truncatedBio }}</p>
          <div class="character-tags">
            <span v-for="(tag, index) in character.tags" :key="index" class="tag-badge">{{ tag }}</span>
          </div>
        </div>
        <div class="character-status">
          <span v-if="character.is_active" class="status-badge active">Active</span>
          <span v-else class="status-badge inactive">Inactive</span>
          <span v-if="character.npc" class="status-badge npc">NPC</span>
          <span v-else class="status-badge player">Player</span>
          <span class="status-badge rank">{{ character.rank.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CharacterPreviewCard",
  props: {
    character: {
      type: Object,
      required: true,
      validator: (character) => {
        console.log('CharacterPreviewCard validator called with:', character);
        return (
            'id' in character &&
            'name' in character &&
            'biography' in character &&
            'npc' in character &&
            'rank' in character &&
            'path' in character &&
            'is_active' in character &&
            'tags' in character
        );
      }
    }
  },
  created() {
    console.log('CharacterPreviewCard created with character:', this.character);
  },
  computed: {
    truncatedBio() {
      if (!this.character.biography || !this.character.biography.background) {
        return 'No biography available';
      }
      const bio = this.character.biography.background;
      return bio.length > 150 ? bio.substring(0, 150) + '...' : bio;
    }
  }
};
</script>

<style scoped>
.character-card {
  position: relative;
  width: 300px;
  height: 200px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #444;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-color: #1e1e1e; /* Primary Background */
}

.character-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  border-color: #555;
}

.character-overlay {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right,
  rgba(0, 0, 0, 0.1) 0%,
  rgba(0, 0, 0, 0.6) 50%,
  rgba(0, 0, 0, 0.8) 100%);
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.character-content {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.character-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
}

.character-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-grow: 1;
}

.character-path {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1E90FF; /* Accent Color */
  font-size: 0.9rem;
}

.path-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  object-fit: cover;
}

.character-bio {
  margin: 0;
  font-size: 0.9rem;
  color: #e0e0e0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.character-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.tag-badge {
  padding: 0.15rem 0.3rem;
  border-radius: 4px;
  font-size: 0.7rem;
  background-color: rgba(30, 144, 255, 0.2);
  color: #64b5f6;
}

.character-status {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  background: rgba(0, 0, 0, 0.5);
}

.status-badge.active {
  background-color: rgba(76, 175, 80, 0.7);
  color: #ffffff;
}

.status-badge.inactive {
  background-color: rgba(158, 158, 158, 0.7);
  color: #ffffff;
}

.status-badge.npc {
  background-color: rgba(255, 152, 0, 0.7);
  color: #ffffff;
}

.status-badge.player {
  background-color: rgba(33, 150, 243, 0.7);
  color: #ffffff;
}

.status-badge.rank {
  background-color: rgba(156, 39, 176, 0.7);
  color: #ffffff;
}

/* Apply blur effect to inactive characters */
.character-card.inactive {
  filter: blur(2px);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .character-card {
    width: 280px;
  }

  .character-content {
    width: 70%;
  }
}

@media (max-width: 900px) {
  .character-card {
    width: 260px;
  }

  .character-content {
    width: 75%;
  }
}

@media (max-width: 768px) {
  .character-card {
    width: 240px;
    height: 180px;
  }

  .character-content {
    width: 70%;
  }

  .character-title {
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }

  .character-bio {
    font-size: 0.8rem;
    -webkit-line-clamp: 2;
  }

  .character-status {
    margin-top: 0.5rem;
  }

  .status-badge {
    padding: 0.15rem 0.35rem;
    font-size: 0.7rem;
  }
}
</style>