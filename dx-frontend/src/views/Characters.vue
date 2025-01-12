<template>
  <div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import {CharacterGameApi} from "@/api/backendService.js";

export default {
  components: {
  },
  async mounted() {
    await this.checkIfHasCharacter()
  },
  async created() {
    await this.checkIfHasCharacter()
  },
  methods: {
    async checkIfHasCharacter() {
      try {
        const hasCharacter = (await CharacterGameApi.characterPlayerCharacterDetailsRetrieve()).data
        this.$router.push({name: 'CharacterInfo'})
      } catch (error) {
        this.$router.push({name: 'CharacterSubmit'})
      }
    }
  }

};
</script>
