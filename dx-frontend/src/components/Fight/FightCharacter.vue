<script setup lang="ts">
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import RPGAvatar from "@/components/PlayerRPGBars/RPGAvatar.vue";

interface Character {
  name?: string;
  title?: string;
  avatar?: string;
}

const props = defineProps<{
  direction?: 'left' | 'right';
  character?: Character;
}>();

// Default values if props are not provided
const direction = props.direction || 'left';
const character = props.character || {
  name: 'The Arbiter',
  title: 'The God of the Arena',
  avatar: undefined
};
</script>

<template>
  <div class="holder" :class="{ 'direction-right': direction === 'right' }">
    <!-- Left direction (default): Avatar on left, Container on right -->
    <template v-if="direction === 'left'">
      <RPGAvatar
        class="character-avatar left-avatar"
        :avatar-url="character.avatar"
      />
      <RPGContainer class="character-container left-container">
        <div class="info--holder left-info">
          <h1 class="character-name">
            {{ character.name }}
          </h1>
          <tr/>
          <h2 class="character-name-alt">
            {{ character.title }}
          </h2>
        </div>
      </RPGContainer>
    </template>

    <!-- Right direction: Container on left, Avatar on right -->
    <template v-else>
      <RPGContainer class="character-container right-container">
        <div class="info--holder right-info">
          <h1 class="character-name">
            {{ character.name }}
          </h1>
          <tr/>
          <h2 class="character-name-alt">
            {{ character.title }}
          </h2>
        </div>
      </RPGContainer>
      <RPGAvatar
        class="character-avatar right-avatar"
        :avatar-url="character.avatar"
      />
    </template>
  </div>
</template>

<style scoped>
/*
 * Responsive Text Implementation:
 * - Using CSS clamp() for fluid responsive sizing that scales with viewport width
 * - Font sizes scale between minimum and maximum values based on viewport width
 * - Letter spacing is also responsive to improve readability on smaller screens
 * - Margins and spacing use responsive units to maintain proper proportions
 * - Media queries handle layout adjustments while clamp() handles text sizing
 */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&display=swap');

.holder {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

/* Common styles for info holder */
.info--holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: clamp(0.5rem, 2vw, 1rem) auto;
}

/* Left direction specific styles */
.left-avatar {
  width: 10rem;
  overflow: hidden;
  margin-right: -5rem; /* Negative margin for overlap */
  z-index: 2; /* Ensure avatar is above container */
}

.left-container {
  flex: 1;
  z-index: 1;
}

.left-info {
  padding-left: 5rem; /* Space for the overlapping avatar */
}

/* Right direction specific styles */
.right-container {
  flex: 1;
  z-index: 1;
}

.right-avatar {
  width: 10rem;
  overflow: hidden;
  margin-left: -5rem; /* Negative margin for overlap */
  z-index: 2; /* Ensure avatar is above container */
}

.right-info {
  padding-right: 5rem; /* Space for the overlapping avatar */
}

/* Character name and title styles */
.character-name {
  font-family: 'Cinzel', serif;
  font-weight: 200;
  font-size: clamp(1.5rem, 3vw, 2.1rem);
  letter-spacing: clamp(0.05em, 0.5vw, 0.1em);
  text-transform: uppercase;
  color: #d6b97b;
}

/* Alternative fantasy fonts */
.character-name-alt {
  color: #d6b97b;
  font-family: 'Pirata One', 'Metamorphous', 'Creepster', cursive;
  font-size: clamp(1rem, 2vw, 1.5rem);
  text-align: center;
}

.info--holder tr {
  width: 100%;
  height: 0.05rem;
  background-color: #d6b97b;
  margin: 0.5rem 0;
}

/* Responsive styles */
@media (max-width: 768px) {
  .holder {
    max-width: 100%;
  }

  .left-avatar, .right-avatar {
    width: 8rem;
  }

  .left-avatar {
    margin-right: -4rem;
  }

  .right-avatar {
    margin-left: -4rem;
  }

  .left-info {
    padding-left: 4rem;
  }

  .right-info {
    padding-right: 4rem;
  }
}

@media (max-width: 480px) {
  .left-avatar, .right-avatar {
    width: 6rem;
  }

  .left-avatar {
    margin-right: -3rem;
  }

  .right-avatar {
    margin-left: -3rem;
  }

  .left-info {
    padding-left: 3rem;
  }

  .right-info {
    padding-right: 3rem;
  }
}

</style>