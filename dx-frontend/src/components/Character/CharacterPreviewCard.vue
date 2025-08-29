<template>
  <div
      class="character-card"
  >
    <!-- Main backdrop overlay for readability -->
    <div class="character-backdrop"></div>

    <!-- Flow energy border effect -->
    <div class="flow-border"></div>

    <img :src="avatarUrl" alt="Character Avatar" class="character-avatar"/>
    <!-- Content container -->
    <div class="character-content">
      <!-- Header section -->
      <div class="character-header">
        <h3 class="character-title">{{ characterName }}</h3>
        <div class="character-path">
          <div class="path-icon-wrapper" v-if="hasPathIcon">
            <img :src="pathIcon" class="path-icon" alt="Path Icon">
          </div>
          <span class="path-name">{{ pathName }}</span>
        </div>
      </div>

      <!-- Bio section -->
      <div class="character-bio-section">
        <p class="character-bio">{{ truncatedBio }}</p>
      </div>

      <!-- Footer with tags and rank -->
      <div class="character-footer">
        <div class="character-tags">
          <span v-for="(tag, index) in characterTags.slice(0, 1)" :key="index" class="tag-badge">
            {{ tag.length > 15 ? tag.substring(0, 15) + '...' : tag }}
          </span>
          <span v-if="characterTags.length > 3" class="tag-badge tag-more">
            +{{ characterTags.length - 3 }}
          </span>
        </div>

        <div class="rank-badge">
          <span class="rank-text">{{ rankName }}</span>
        </div>
      </div>
    </div>

    <!-- Hover glow effect -->
    <div class="hover-glow"></div>
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
            'rank' in character &&
            'path' in character &&
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
      return bio.length > 80 ? bio.substring(0, 80) + '...' : bio;
    },
    avatarUrl() {
      // Safely handle null biography or missing avatar
      return this.character.biography && this.character.biography.avatar
        ? this.character.biography.avatar
        : '/img/default-avatar.png'; // Return a default avatar URL
    },
    characterTags() {
      // Safely handle null or undefined tags
      return this.character.tags || [];
    },
    rankName() {
      // Safely handle null or undefined rank
      return this.character.rank && this.character.rank.name
        ? this.character.rank.name
        : 'Unknown Rank';
    },
    pathName() {
      // Safely handle null or undefined path
      return this.character.path && this.character.path.name
        ? this.character.path.name
        : 'No Path';
    },
    characterName() {
      // Safely handle null or undefined character name
      return this.character.name || 'Unnamed Character';
    },
    hasPathIcon() {
      // Check if path and path.icon exist
      return !!(this.character.path && this.character.path.icon);
    },
    pathIcon() {
      // Safely get path icon
      return this.character.path && this.character.path.icon
        ? this.character.path.icon
        : '';
    }
  }
};
</script>

<style scoped>
/* Universal box-sizing and overflow protection */
.character-card *,
.character-card *::before,
.character-card *::after {
  box-sizing: border-box;
}

.character-card {
  position: relative;
  width: 320px;
  height: 200px;
  border-radius: 0.5rem;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-color: rgba(0, 0, 0, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid rgba(127, 255, 22, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
}

.character-card:hover {
  transform: translateY(-2px);
  border-color: #7fff16;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Enhanced backdrop for better text readability */
.character-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
      135deg,
      rgba(0, 0, 0, 0.2) 0%,
      rgba(0, 0, 0, 0.6) 40%,
      rgba(0, 0, 0, 0.85) 100%
  );
  backdrop-filter: blur(1px);
  transition: backdrop-filter 0.3s ease;
}

.character-card:hover .character-backdrop {
  backdrop-filter: blur(1px);
}

/* Flow energy border effect */
.flow-border {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
  transparent,
  rgba(127, 255, 22, 0.1),
  transparent,
  rgba(127, 255, 22, 0.1),
  transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 6s ease-in-out infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.character-card:hover .flow-border {
  opacity: 1;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Main content container */
.character-content {
  position: relative;
  z-index: 2;
  padding: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
  overflow: hidden;
  max-width: 100%;
}

/* Header section */
.character-header {
  flex-shrink: 0;
}

.character-title {
  margin: 0 0 4px 0;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  text-shadow:
      0 2px 4px rgba(0, 0, 0, 0.8),
      0 0 8px rgba(255, 255, 255, 0.1);
  letter-spacing: 0.5px;
  line-height: 1.2;
  max-width: 60%;
}

.character-path {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.path-icon-wrapper {
  position: relative;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(127, 255, 22, 0.2), rgba(127, 255, 22, 0.3));
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.path-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  object-fit: cover;
  filter: brightness(1.1) saturate(1.2);
}

.path-name {
  color: rgba(250, 218, 149, 0.7);
  font-size: 0.8rem;
  font-weight: 400;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
  letter-spacing: 0.3px;
}

/* Bio section */
.character-bio-section {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: flex-start;
  margin: 4px 0 8px 0;
}

.character-bio {
  margin: 0;
  font-size: 0.8rem;
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: rgba(250, 218, 149, 0.8);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
  font-weight: 400;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Footer section */
.character-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  max-width: 100%;
  overflow: hidden;
}

.character-tags {
  display: flex;
  flex-wrap: nowrap;
  gap: 3px;
  flex: 1;
  align-items: center;
  min-width: 0;
  overflow: hidden;
}

.tag-badge {
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 0.6rem;
  font-weight: 500;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  background: rgba(127, 255, 22, 0.1);
  color: #fada95;
  border: 1px solid rgba(127, 255, 22, 0.3);
  text-transform: uppercase;
  letter-spacing: 0.2px;
  transition: all 0.2s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  white-space: nowrap;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

.tag-badge:hover {
  background: rgba(127, 255, 22, 0.15);
  border-color: rgba(127, 255, 22, 0.5);
  transform: translateY(-1px);
}

.tag-more {
  background: rgba(127, 255, 22, 0.1);
  color: #fada95;
  border-color: rgba(127, 255, 22, 0.2);
}

.rank-badge {
  padding: 3px 6px;
  border-radius: 4px;
  background: linear-gradient(135deg,
  rgba(127, 255, 22, 0.2),
  rgba(127, 255, 22, 0.3)
  );
  border: 1px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(1px);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  max-width: 80px;
}

.rank-badge::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
  transparent,
  rgba(255, 255, 255, 0.1),
  transparent
  );
  transition: left 0.5s ease;
}

.character-card:hover .rank-badge::before {
  left: 100%;
}

.rank-text {
  color: #fada95;
  font-size: 0.5rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
  position: relative;
  z-index: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

/* Hover glow effect */
.hover-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 0.6rem;
  background: linear-gradient(45deg,
  rgba(127, 255, 22, 0.3),
  rgba(127, 255, 22, 0.2),
  rgba(127, 255, 22, 0.3)
  );
  background-size: 300% 300%;
  opacity: 0;
  z-index: -1;
  animation: glowPulse 3s ease-in-out infinite;
  transition: opacity 0.3s ease;
}

.character-card:hover .hover-glow {
  opacity: 1;
}

@keyframes glowPulse {
  0%, 100% {
    background-position: 0% 50%;
    opacity: 0.5;
  }
  50% {
    background-position: 100% 50%;
    opacity: 0.8;
  }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .character-card {
    width: 300px;
    height: 190px;
  }

  .tag-badge {
    max-width: 55px;
  }

  .rank-badge {
    max-width: 75px;
  }
}

@media (max-width: 900px) {
  .character-card {
    width: 280px;
    height: 180px;
  }

  .character-content {
    padding: 14px;
  }

  .character-title {
    font-size: 1.1rem;
  }

  .tag-badge {
    max-width: 50px;
    font-size: 0.55rem;
  }

  .rank-badge {
    max-width: 70px;
  }

  .rank-text {
    font-size: 0.55rem;
  }
}

@media (max-width: 768px) {
  .character-card {
    width: 260px;
    height: 170px;
  }

  .character-content {
    padding: 12px;
  }

  .character-title {
    font-size: 1rem;
    margin-bottom: 2px;
  }

  .character-bio {
    font-size: 0.75rem;
    -webkit-line-clamp: 2;
  }

  .path-name {
    font-size: 0.75rem;
  }

  .tag-badge {
    font-size: 0.5rem;
    padding: 1px 3px;
    max-width: 45px;
  }

  .rank-text {
    font-size: 0.5rem;
  }

  .rank-badge {
    max-width: 60px;
    padding: 2px 4px;
  }

  .path-icon-wrapper {
    width: 18px;
    height: 18px;
  }

  .path-icon {
    width: 14px;
    height: 14px;
  }

  .character-footer {
    gap: 4px;
  }
}

/* Dark theme optimization */
@media (prefers-color-scheme: dark) {
  .character-card {
    background-color: #000000;
  }
}

/* Performance optimizations */
.character-card * {
  will-change: auto;
}

.character-avatar {
  position: absolute;
  width: 50%;
  height: 100%;
  right: 0;
  object-fit: cover;
  object-position: center;
  z-index: 0;
  mask: linear-gradient(to left, rgba(0, 0, 0, 0.8) 60%, rgba(0, 0, 0, 0) 100%);
}
</style>