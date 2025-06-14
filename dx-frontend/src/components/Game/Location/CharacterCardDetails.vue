<template>
  <div class="icon-overlay" v-if="details && Object.keys(details).length">
    <!-- Detailed View -->
    <template v-if="!isCompact">
      <div class="overlay-item rank" v-if="details.rankGrade">
        <span class="rank-title">Rank:</span>
        <span class="rank-value">{{ details.rankGrade }}</span>
      </div>
      <div
          v-for="(attribute, key) in details.attributes || {}"
          :key="key"
          class="overlay-item attribute"
      >
        <span>
          <span :class="`${key}-value`">
            {{ attribute.current !== undefined ? attribute.current : "xx" }}
          </span>
          /
          <span :class="`${key}-value`">
            {{ attribute.max !== undefined ? attribute.max : "xx" }}
          </span>
        </span>
      </div>
    </template>

    <!-- Compact View: display 3 circles with numbers -->
    <template v-else>
      <div class="compact-container">
        <!-- If rank exists, show it first -->
        <div class="compact-circle" v-if="details.rankGrade">
          {{ details.rankGrade }}
        </div>
        <!-- Show first two attributes if rank exists; otherwise first three -->
        <div
            class="compact-circle"
            v-for="(attr, index) in compactAttributes"
            :key="attr.key"
            v-if="details.rankGrade ? index < 2 : index < 3"
        >
          {{ attr.current !== undefined ? attr.current : "xx" }}
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'CharacterCardDetails',
  props: {
    details: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      isCompact: false
    }
  },
  computed: {
    compactAttributes() {
      return this.details.attributes
          ? Object.keys(this.details.attributes).map(key => ({
            key,
            ...this.details.attributes[key]
          }))
          : [];
    }
  },
  mounted() {
    this.checkSize();
    window.addEventListener('resize', this.checkSize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkSize);
  },
  methods: {
    checkSize() {
      this.isCompact = window.innerWidth < 400; // threshold for compact mode
    }
  }
}
</script>

<style scoped>
.icon-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.6rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  pointer-events: none;
  padding: 0.3rem;
  text-align: center;
  box-sizing: border-box;
}

.overlay-item {
  margin: 0.2em 0;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.rank-title, .rank-value {
  color: #f8eb67;
}

.health-name, .health-value {
  color: #e91e63;
}

.energy-name, .energy-value {
  color: #2196f3;
}

.action-name, .action-value {
  color: #9c27b0;
}

.character-name {
  font-size: 0.7em;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  max-height: 2.4em;
}

/* Compact View Styles */
.compact-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.compact-circle {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0.2rem;
  font-size: 0.6rem;
  color: #fff;
}
</style>
