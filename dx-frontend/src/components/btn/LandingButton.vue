<template>
  <div class="dx-button" @click="handleClick" role="button" tabindex="0">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "LandingButton",
  props: {
    action: {
      type: Function,
      required: true,
    },
  },
  methods: {
    handleClick() {
      if (this.action) this.action();
    },
  },
};
</script>

<style scoped>
.dx-button {
  display: inline-block;
  background: #292929;
  color: #e0e0e0;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), inset 0 -3px 6px #1a1a1a;
  background-image: linear-gradient(145deg, #404040, #292929);
  border: 2px solid #444;
  text-align: center;
}

.dx-button:hover {
  background-image: linear-gradient(145deg, #505050, #3a3a3a);
  transform: translateY(-2px);
}

.dx-button:active {
  transform: translateY(2px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3), inset 0 3px 6px #1a1a1a;
}

.dx-button:focus {
  outline: 2px solid #e0e0e0;
}
</style>
