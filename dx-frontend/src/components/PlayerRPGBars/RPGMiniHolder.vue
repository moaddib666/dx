<script setup lang="ts">
</script>

<template>
  <div
      class="rpg-effects-holder"
  >
    <div class="rpg-effects-holder__wrapper">
      <img
          src="https://npr.brightspotcdn.com/dims4/default/e72b23b/2147483647/strip/true/crop/3872x2592+0+0/resize/880x589!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F43%2F5d%2F91be24f147d5bb0a9c49a39a545f%2Fpexels-pixabay-270815.jpg"
          alt="RPG Effects Holder"
          class="rpg-effects-holder__image"
          sizes="content"
      />
    </div>
  </div>
</template>

<style scoped>
.rpg-effects-holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 2rem;
  height: 2rem;
  background: url('@/assets/rpg_bars/shield_holder_with_border.png') no-repeat center center;
  background-size: cover;
}
.rpg-effects-holder__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  mask: url('@/assets/rpg_bars/shield_holder_mask_invented.png') no-repeat center;
  mask-size: cover;
}
</style>