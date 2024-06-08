<template>
  <div class="json-path-character">
    <img src="@/assets/icons/json-path-icon.svg" alt="JSON Path Character" />
  </div>
</template>

<script setup>
</script>

<style scoped>
.json-path-character {
  position: fixed;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  border: 2px solid #00ffcc;
  border-radius: 0 12px 12px 0;
  padding: 10px;
  z-index: 100;
  box-shadow: 0 0 10px #00ffcc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.json-path-character img {
  width: 50px;
  height: auto;
}
</style>
