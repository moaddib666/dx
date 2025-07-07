<script setup lang="ts">
</script>

<template>
  <div class="rpg-avatar">
    <div class="rpg-avatar__wrapper">
      <img
          src="https://images.squarespace-cdn.com/content/v1/605e90f9c17ee25104dba783/1684973142360-DGM2VVQ5D1356WLMWZQD/Screenshot+2023-05-24+170440.png?format=1500w"
          alt="Character Avatar"
          class="rpg-avatar__image"
          sizes="content"
      />
    </div>
  </div>
</template>

<style scoped>
.rpg-avatar {
  width: 10rem;
  height: 15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  background: url("@/assets/rpg_bars/rpg_avatar_border.png") no-repeat center;
  background-size: cover;

  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;

}

.rpg-avatar__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  mask: url("@/assets/rpg_bars/rpg_avatar_border_mask_invented.png") no-repeat center;
  mask-size: cover;
}

.rpg-avatar__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

</style>