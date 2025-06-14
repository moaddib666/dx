<template>
  <div
      class="character-card"
      :style="bgStyle"
      :class="{ 'no-action': noActionPoints && !deathOverlay }"
      @click="$emit('click')"
  >

    <!-- Horizontal Name of the Character -->
    <div class="character-name">{{ name }}</div>
    <!-- Horizontal Attribute Bars at the bottom -->
    <div class="card-bars" style="position:absolute; bottom:0; width:100%">
      <AttributeBar
          v-for="(attribute, index) in attributeBars"
          :key="index"
          :current="attribute.current"
          :max="attribute.max"
          :type="attribute.name"
          class="attribute-bar"
      />
    </div>
    <!-- Death or knockout overlay -->
    <div v-if="deathOverlay" class="death-overlay"></div>
    <!-- Red overlay for low health -->
    <div v-else-if="lowHealth" class="low-health-overlay"></div>

  </div>
</template>

<script>

import AttributeBar from "@/components/GameMaster/Character/AttributeBar.vue";

export default {
  name: "CharacterCard",
  components: {AttributeBar},
  props: {
    icon: {type: String, required: true},
    name: {type: String, required: true},
    // details is expected to include an "attributes" array.
    details: {type: Object, default: () => ({})}
  },
  computed: {
    bgStyle() {
      return {
        backgroundImage: `url(${this.icon})`,
        backgroundSize: "cover",
        backgroundPosition: "center"
      };
    },
    // Build an array of attributes from details.attributes (an array)
    attributeBars() {
      return this.details?.attributes || [];
    },
    // Determines if the character has no action points
    noActionPoints() {
      const attrArr = this.details?.attributes || [];
      const actionAttr = attrArr.find(attr =>
          attr.name.toLowerCase().includes("action")
      );
      return actionAttr ? actionAttr.current === 0 : false;
    },
    // Determines if the character's health is below 10
    lowHealth() {
      const attrArr = this.details?.attributes || [];
      const healthAttr = attrArr.find(attr => attr.name.toLowerCase() === "health");
      return healthAttr ? healthAttr.current < 10 : false;
    },
    // Death or knockout overlay
    deathOverlay() {
      const attrArr = this.details?.attributes || [];
      const healthAttr = attrArr.find(attr => attr.name.toLowerCase() === "health");
      return healthAttr ? healthAttr.current <= 0 : false;
    }
  }
};
</script>

<style scoped>
.character-card {
  height: 7rem;
  width: 4rem;
  border: 0.1rem solid #ccc;
  border-radius: 0.5rem;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

/* Character name at the top */
.character-name {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 0.5rem;
  padding: 0.1rem 0.2rem;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}


/* Red overlay for low health */
.low-health-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 0, 0, 0.2);
  pointer-events: none;
}

.death-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("@/assets/images/avatar/death.webp" ) no-repeat center;
  background-size: cover;
  pointer-events: none;
  mix-blend-mode: screen;
}



/* Gray out the card if no action points */
.no-action {
  filter: grayscale(100%);
  opacity: 0.7;
}

</style>
