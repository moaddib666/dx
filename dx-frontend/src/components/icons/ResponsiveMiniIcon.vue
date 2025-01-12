<script>
export default {
  name: "ResponsiveMiniIcon",
  props: {
    imageUrl: {
      type: String,
      required: false,
    },
    title: {
      type: String,
      required: false,
    },
    altText: {
      type: String,
      required: false,
    },
    isSelected: {
      type: Boolean,
      default: false,
    },
    isActive: {
      type: Boolean,
      default: false,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<template>
  <div>
    <img v-if="imageUrl"
        :class="['responsive-mini-icon', isActive ? 'active' : '', isDisabled ? 'disabled' : '', isSelected ? 'selected' : '']"
        :src="imageUrl"
        :title="title"
        :alt="altText"
    >
    <img v-else
        :class="['responsive-mini-icon', isActive ? 'active' : '', isDisabled ? 'disabled' : '', isSelected ? 'selected' : '']"
        src="@/assets/images/skill/default.webp"
        :title="title"
        :alt="altText"
    >
    <slot class="icon-overlay-item"></slot>
  </div>
</template>

<style scoped>
.responsive-mini-icon {
  width: 3em;
  height: 3em;
  border-radius: 50%;
  object-fit: cover;
  object-position: center;
  border: 1px solid black;
}

.responsive-mini-icon.active {
  border: 0.2em solid #00e5ff;
  box-shadow: 0 0 1em #00e5ff;
}

.responsive-mini-icon.selected {
  border: 0.2em solid #00ff00;
  box-shadow: 0 0 1em #00ff00;
}

.responsive-mini-icon.disabled {
  filter: grayscale(100%);
}

.icon-overlay-item {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.3rem;
}

.icon-overlay-item > * {
  background: rgba(0, 0, 0, 0.5);
  padding: 0.2rem;
  border-radius: 0.3rem;
}

.icon-overlay-item > *:first-child {
  background: rgba(0, 0, 0, 0.8);
  padding: 0.3rem;
}

.icon-overlay-item > *:last-child {
  background: rgba(0, 0, 0, 0.8);
  padding: 0.3rem;
}

</style>