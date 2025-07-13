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
  border-image: url("@/assets/rpg/grid_cell.png");
  padding: 2rem;
  border-image-slice:
      15 15 15 15 fill;
  border-image-width:
      3em 3em 3em 3em;
  border-image-outset:
      0px 0px 0px 0px;
  border-image-repeat:
      stretch stretch;
}

</style>