<script>
import SpellButtonComponent from "@/components/Game/Fight/SpellButtonComponent.vue";

export default {
  name: "SpellHolderComponent",
  components: {SpellButtonComponent},
  props: {
    spells: {
      type: Array,
      required: true
    }
  },
  methods: {
    cast(spellId) {
      console.debug('Casting spell:', spellId);
      this.$emit('cast', spellId);
    }
  }
}
</script>

<template>
  <div class="spell-holder horizontal-layout">
    <div class="spell-wrapper"   v-for="(spell, index) in spells" :key="spell.id || index">
      <SpellButtonComponent @cast="cast" :spell="spell" />
    </div>
  </div>
</template>

<style scoped>
.spell-holder {
  background: rgba(0, 0, 0, 0.5);
  padding: 1.5vh;
  width: 40vh;
  height: 40vh;
  gap: 1vh;
}

.spell-wrapper {
  width: 5vh;
  height: 5vh;

}
</style>