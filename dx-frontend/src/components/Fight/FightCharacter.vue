<script setup lang="ts">

import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import RPGAvatar from "@/components/PlayerRPGBars/RPGAvatar.vue";
</script>

<template>
  <div class="holder">
    <RPGAvatar class="character-avatar">
      :avatar-url="props.character.avatar"
    </RPGAvatar>
    <RPGContainer>
      <div class="info--holder">
        <h1 class="character-name">
          The Arbiter
        </h1>
        <tr/>
        <h2 class="character-name-alt">
          The God of the Arena
        </h2>
      </div>
    </RPGContainer>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&display=swap');

.info--holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 1rem auto;
  padding-left: 5rem;
}

.character-name {
  font-family: 'Cinzel', serif;
  font-weight: 200;
  font-size: 2.1rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #d6b97b;
}

/* Alternative fantasy fonts */
.character-name-alt {
  color: #d6b97b;
  font-family: 'Pirata One', 'Metamorphous', 'Creepster', cursive;
}

.info--holder h2 {
  font-size: 1.5rem;
  text-align: center;
}

.info--holder tr {
  width: 100%;
  height: 0.05rem;
  background-color: #d6b97b;
  margin: 0.5rem 0;
}

.holder {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.character-avatar {
  width: 10rem;
  overflow: hidden;
  margin-right: -5rem;
}

</style>