<template>
  <div class="rank-container">
    <strong class="rank-name">{{ rank.name }}</strong>
    <div class="progress-bar">
      <div
          class="progress"
          :style="{ width: progressPercentage + '%' }"
      ></div>
    </div>
    <div class="rank-info">
      <span>{{ experience }}/{{ rank.experience_needed }} XP</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "RankComponent",
  props: {
    rank: {
      type: Object,
      required: true,
    },
    experience: {
      type: Number,
      required: true,
    },
  },
  computed: {
    progressPercentage() {
      return Math.min(
          (this.experience / this.rank.experience_needed) * 100,
          100
      );
    },
  },
};
</script>

<style scoped>
.rank-container {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  width: 100%;
}

.rank-name {
  font-size: 0.9rem;
  font-weight: bold;
  text-transform: capitalize;
  color: #00e5ff;
}

.progress-bar {
  background: rgba(255, 255, 255, 0.1);
  height: 0.5rem;
  border-radius: 0.3rem;
  overflow: hidden;
  width: 100%;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #00ff7f, #00e5ff);
  border-radius: 0.3rem;
}

.rank-info {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
}
</style>
