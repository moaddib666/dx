<script setup lang="ts">

</script>

<template>
  <div class="container">
    <slot></slot>
  </div>
</template>

<style scoped>
.container {
  padding: 2.5rem;
  display: flex;
  width: 100%;
  height: 100%;
  border-image-source: url("@/assets/rpg/bordertemplate.png");
  border-image-slice: 120 150 120 150 fill;
  border-image-width: 2.5rem 2.5rem 2.5rem 2.5rem;
  border-image-outset: 0 0 0 0;
  border-image-repeat: stretch stretch;
}

</style>