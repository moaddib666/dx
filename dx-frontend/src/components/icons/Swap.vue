<template>
  <button class="swipe-icon" title="swap">
    <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        class="swipe-icon__svg"
        aria-label="Swap Icon"
    >
      <path
          d="M8 12L12 16L16 12L14.59 10.59L13 12.17V8H11V12.17L9.41 10.59L8 12ZM4 18H20V20H4V18ZM4 4H20V6H4V4Z"
          fill="currentColor"
      />
    </svg>
  </button>
</template>

<script>
export default {
  name: "SwapIcon",
  methods: {},
};
</script>

<style scoped>
.swipe-icon {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease-in-out;
}

.swipe-icon:hover {
  background: rgba(0, 0, 0, 0.1);
}

.swipe-icon:active {
  background: rgba(0, 0, 0, 0.2);
}

.swipe-icon__svg {
  width: 1.5em;
  height: 1.5em;
  fill: currentColor;
  transition: transform 0.2s ease-in-out;
}

.swipe-icon:hover .swipe-icon__svg {
  transform: scale(1.2);
}
</style>
