<template>
  <div class="bio-container">
    <p class="bio-text">
      {{ shortBio }}
      <span v-if="showFullBio"> {{ bio.background }}</span>
      <button v-if="!showFullBio" @click="toggleBio" class="toggle-btn">More</button>
    </p>
  </div>
</template>

<script>
export default {
  name: "BioComponent",
  props: {
    bio: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showFullBio: false,
    };
  },
  computed: {
    shortBio() {
      return this.bio.background.slice(0, 50) + "...";
    },
  },
  methods: {
    toggleBio() {
      this.showFullBio = !this.showFullBio;
    },
  },
};
</script>

<style scoped>
.bio-container {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.9);
}

.bio-text {
  line-height: 1.2;
}

.toggle-btn {
  background: none;
  border: none;
  color: #00e5ff;
  cursor: pointer;
  font-size: 0.8rem;
}
</style>
