<script setup lang="ts">

</script>

<template>
  <div class="rpg-cell">
    <slot></slot>
  </div>
</template>

<style scoped>
.rpg-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-image: url("@/assets/rpg/grid_cell_large.png");
  padding: 10%;
  border-image-slice:
      150 150 150 150 fill;
  border-image-width:
      20px 20px 20px 20px;
  border-image-outset:
      0px 0px 0px 0px;
  border-image-repeat:
      stretch stretch;
}

</style>