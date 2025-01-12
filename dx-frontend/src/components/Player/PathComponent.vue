<template>
  <div class="path-container">
    <img :src="path.icon" alt="Path Icon" class="path-icon"/>
    <div class="path-details">
      <span class="path-name">{{ path.name }}</span>
      <p class="path-description">{{ path.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "PathComponent",
  props: {
    path: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.path-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 0.3rem;
  padding: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.path-icon {
  width: 2rem;
  height: 2rem;
  object-fit: contain;
}

.path-details {
  font-size: 0.9rem;
}

.path-name {
  font-weight: bold;
  color: #00e5ff;
}

.path-description {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
}
</style>
