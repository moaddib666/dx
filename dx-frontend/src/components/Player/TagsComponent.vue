<template>
  <div class="tags-container">
    <span v-for="(tag, index) in tags" :key="index" class="tag">
      {{ tag }}
    </span>
  </div>
</template>

<script>
export default {
  name: "TagsComponent",
  props: {
    tags: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
}

.tag {
  background: rgba(0, 0, 0, 0.7);
  color: #00e5ff;
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  text-transform: capitalize;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}
</style>
