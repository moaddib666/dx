<script setup lang="ts">
import { ref } from 'vue';
import RPGCell from "@/components/RPGGrid/RPGCell.vue";
import ItemSelectIcon from "@/components/icons/ItemSelectIcon.vue";
import SkillSelectIcon from "@/components/icons/SkillSelectIcon.vue";
import CharacterSelectIcon from "@/components/icons/CharacterSelectIcon.vue";
import PositionSelectIcon from "@/components/icons/PositionSelectIcon.vue";
import GameObjectSelectIcon from "@/components/icons/GameObjectSelectIcon.vue";
import LocationSelectorIcon from "@/components/icons/LocationSelectorIcon.vue";

// Define props for optional ID parameters
const props = defineProps({
  gameObjectId: {
    type: [String, Number],
    default: null
  },
  positionId: {
    type: [String, Number],
    default: null
  },
  locationId: {
    type: [String, Number],
    default: null
  },
  characterId: {
    type: [String, Number],
    default: null
  },
  skillId: {
    type: [String, Number],
    default: null
  },
  itemId: {
    type: [String, Number],
    default: null
  }
});

// Define emits
const emit = defineEmits(['settingClick']);

const showSettings = ref(false);

const toggleSettings = () => {
  showSettings.value = !showSettings.value;
};
</script>
<template>
  <div class="trigger-container">
    <!--  Main Trigger Visual-->
    <RPGCell class="trigger--main" @click="toggleSettings" title="Trigger Settings">
      <img src="@/assets/icons/trigger-icon-v1.png" class="empty-trigger-icon"  alt="empty-trigger-icon" />
    </RPGCell>
    <!-- OnClick Settings Area underneath the main trigger visual -->
    <div class="trigger--settings" v-if="showSettings">
      <div class="trigger--settings--row">
        <RPGCell
          class="trigger--settings--icon trigger--settings__gameObject"
          :class="{ 'has-id': gameObjectId }"
          title="Select Game Object"
          :data-id="gameObjectId"
        >
          <GameObjectSelectIcon class="trigger--settings--icon--content" />
          <span v-if="gameObjectId" class="id-indicator"></span>
        </RPGCell>
        <RPGCell
          class="trigger--settings--icon trigger--settings__position"
          :class="{ 'has-id': positionId }"
          title="Select Position"
          :data-id="positionId"
        >
          <PositionSelectIcon class="trigger--settings--icon--content" />
          <span v-if="positionId" class="id-indicator"></span>
        </RPGCell>
        <RPGCell
          class="trigger--settings--icon trigger--settings__location"
          :class="{ 'has-id': locationId }"
          title="Select Location"
          :data-id="locationId"
        >
          <LocationSelectorIcon class="trigger--settings--icon--content" />
          <span v-if="locationId" class="id-indicator"></span>
        </RPGCell>
      </div>
      <div class="trigger--settings--row">
        <RPGCell
          class="trigger--settings--icon trigger--settings__npc"
          :class="{ 'has-id': characterId }"
          title="Select Character"
          :data-id="characterId"
        >
          <CharacterSelectIcon class="trigger--settings--icon--content" />
          <span v-if="characterId" class="id-indicator"></span>
        </RPGCell>
        <RPGCell
          class="trigger--settings--icon trigger--settings__skill"
          :class="{ 'has-id': skillId }"
          title="Select Skill"
          :data-id="skillId"
        >
          <SkillSelectIcon class="trigger--settings--icon--content" />
          <span v-if="skillId" class="id-indicator"></span>
        </RPGCell>
        <RPGCell
          class="trigger--settings--icon trigger--settings__item"
          :class="{ 'has-id': itemId }"
          title="Select Item"
          :data-id="itemId"
        >
          <ItemSelectIcon class="trigger--settings--icon--content" />
          <span v-if="itemId" class="id-indicator"></span>
        </RPGCell>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trigger-container {
  position: relative;
  width: 4em;
  height: 4em;
}

.trigger--main {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 4.8em;
  height: 4.8em;
  background-color: #f0f0f0;
  cursor: pointer;
  position: relative;
  z-index: 2;
}

.trigger--settings {
  position: absolute;
  top: 0;
  left: 4em;
  width: 12em;
  display: flex;
  flex-direction: column;
  z-index: 10;
}

.trigger--settings--row {
  display: flex;
}

.trigger--settings--icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2em;
  height: 2em;
  cursor: pointer;
  transition: transform 0.2s ease;
  position: relative; /* Added for positioning the id-indicator */
}

.trigger--settings--icon:hover {
  transform: scale(1.1);
}

.trigger--settings--icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 2px;
}

.trigger--settings__position--content {
  font-size: 0.8em;
  text-align: center;
  color: #333;
}

.trigger--settings--icon--content {
  width: 100%;
  height: 100%;
  min-width: 2em;
  min-height: 2em;
  display: block;
}

/* Styles for cells with IDs */
.trigger--settings--icon.has-id {
  border: 1px solid #4CAF50; /* Green border for cells with IDs */
  box-shadow: 0 0 3px rgba(76, 175, 80, 0.5); /* Subtle green glow */
}

/* ID indicator dot */
.id-indicator {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 6px;
  height: 6px;
  background-color: #4CAF50; /* Green dot */
  border-radius: 50%;
  z-index: 3;
}

.empty-trigger-icon {
  width: 100%;
  height: 100%;
  opacity: 0.5;
  transition: opacity 0.4s ease;
}

.empty-trigger-icon:hover {
  opacity: 1;
  transition: width 0.2s ease, height 0.2s ease;
}
.empty-trigger-icon:active {
  opacity: 1;
  width: 80%;
  height: 80%;
}
</style>