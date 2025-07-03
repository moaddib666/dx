<template>
  <div class="character-card" @click="$emit('select')">
    <!-- Background Image -->
    <div
        class="card-background"
        :style="{ backgroundImage: `url(${icon})` }"
    >
      <!-- Gradient Overlay -->
      <div class="card-overlay"></div>

      <!-- Card Content -->
      <div class="card-content">
        <!-- Header Area -->
        <div class="card-header">
          <div v-if="details?.rankGrade" class="rank-badge">
            {{ details.rankGrade }}
          </div>
        </div>

        <!-- Character Name -->
        <div class="character-name">
          {{ name }}
        </div>

        <!-- Stats Area -->
        <CharacterCardDetails
            v-if="details"
            :details="details"
            class="stats-area"
        />
      </div>

      <!-- Selection Indicator -->
      <div class="selection-glow"></div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import CharacterCardDetails from './CharacterCardDetails.vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  details: {
    type: Object,
    default: null
  },
  selected: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])
</script>
<style scoped>
.character-card {

  width: clamp(3rem, 5vw, 5rem);
  height: clamp(6rem, 10vw, 9rem);

  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 0.75rem;
  overflow: hidden;
  position: relative;
  box-shadow:
      0 0.25rem 0.9375rem rgba(0, 0, 0, 0.4),
      0 0 0 0.125rem rgba(100, 150, 255, 0.2);
  flex-shrink: 0;
}

.character-card:hover {
  transform: translateY(-0.5rem) scale(1.02);
  box-shadow:
      0 0.5rem 1.5625rem rgba(0, 0, 0, 0.6),
      0 0 0 0.1875rem rgba(100, 150, 255, 0.5),
      0 0 1.25rem rgba(100, 150, 255, 0.3);
  z-index: 10;
}

.card-background {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  display: flex;
  flex-direction: column;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.1) 0%,
      rgba(0, 0, 0, 0.3) 40%,
      rgba(0, 0, 0, 0.8) 100%
  );
  transition: opacity 0.3s ease;
}

.character-card:hover .card-overlay {
  background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.05) 0%,
      rgba(0, 0, 0, 0.2) 40%,
      rgba(0, 0, 0, 0.7) 100%
  );
}

.card-content {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0.375rem;
}

.card-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: auto;
}

.rank-badge {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4a 100%);
  color: #1a1a1a;
  font-size: 0.6rem;
  font-weight: bold;
  padding: 0.15rem 0.4rem;
  border-radius: 1rem;
  min-width: 1rem;
  text-align: center;
  box-shadow:
      0 0.125rem 0.5rem rgba(255, 215, 0, 0.4),
      inset 0 0.0625rem 0 rgba(255, 255, 255, 0.3);
  border: 0.0625rem solid rgba(255, 215, 0, 0.6);
  line-height: 1;
}

.character-name {
  font-size: clamp(0.42rem, 0.7vw, 0.5rem);
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  text-shadow:
      0 0.125rem 0.25rem rgba(0, 0, 0, 0.8),
      0 0 0.5rem rgba(0, 0, 0, 0.6);
  margin-bottom: 0.3rem;
  line-height: 1.1;
  letter-spacing: 0.03em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stats-area {
  margin-top: auto;
}

.selection-glow {
  position: absolute;
  top: -0.125rem;
  left: -0.125rem;
  right: -0.125rem;
  bottom: -0.125rem;
  border-radius: 0.875rem;
  background: linear-gradient(45deg,
  transparent,
  rgba(100, 150, 255, 0.3),
  transparent,
  rgba(100, 150, 255, 0.3),
  transparent
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  z-index: -1;
}

.character-card:hover .selection-glow {
  opacity: 1;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

/* Responsive Design for different viewport sizes */
@media (max-width: 75em) { /* 1200px */
  .character-card {
    width: clamp(5.5rem, 9vw, 7rem);
    height: clamp(7.5rem, 13vw, 10rem);
  }

  .card-content {
    padding: 0.4rem;
  }

  .character-name {
    font-size: clamp(0.6rem, 1.3vw, 0.75rem);
    margin-bottom: 0.25rem;
  }

  .rank-badge {
    font-size: 0.55rem;
    padding: 0.125rem 0.35rem;
  }
}

@media (max-width: 48em) { /* 768px */
  .character-card {
    width: clamp(5rem, 12vw, 6.5rem);
    height: clamp(7rem, 16vw, 9rem);
  }

  .card-content {
    padding: 0.35rem;
  }

  .character-name {
    font-size: clamp(0.55rem, 1.5vw, 0.7rem);
    margin-bottom: 0.2rem;
  }

  .rank-badge {
    font-size: 0.5rem;
    padding: 0.1rem 0.3rem;
  }
}

@media (max-width: 30em) { /* 480px */
  .character-card {
    width: clamp(4.5rem, 15vw, 6rem);
    height: clamp(6.5rem, 20vw, 8.5rem);
  }

  .card-content {
    padding: 0.3rem;
  }

  .character-name {
    font-size: clamp(0.5rem, 1.8vw, 0.65rem);
    margin-bottom: 0.15rem;
  }

  .rank-badge {
    font-size: 0.45rem;
    padding: 0.08rem 0.25rem;
  }
}

/* Card Holder Row Layout Support */
.character-card-row {
  display: flex;
  gap: clamp(0.375rem, 0.75vw, 0.75rem);
  padding: 0.75rem;
  overflow-x: auto;
  align-items: flex-start;
  scrollbar-width: thin;
  scrollbar-color: rgba(100, 150, 255, 0.3) transparent;
}

.character-card-row::-webkit-scrollbar {
  height: 0.28125rem;
}

.character-card-row::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 0.140625rem;
}

.character-card-row::-webkit-scrollbar-thumb {
  background: rgba(100, 150, 255, 0.3);
  border-radius: 0.140625rem;
}

.character-card-row::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 150, 255, 0.5);
}
</style>