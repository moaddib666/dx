<script>
import SkillIcon from "@/components/Action/ActionIcon.vue";

export default {
  name: "CharacterSkills.vue",
  components: {SkillIcon},
  data() {
    return {
      skills: [
        {
          "id": 24,
          "name": "Hellfire",
          "multi_target": true,
          "type": "attack",  // iccon of attack sckill + red glow border 'attack' | 'defense' |'heal' | 'buff' | 'debuff' | 'utility' | 'special'
          "cost": [
            { // Optional
              "kind": "Action Points",
              "value": 10
            },
            { // Optional
              "kind": "Energy",
              "value": 40
            },
            { // Optional
              "kind": "Health",
              "value": 40
            }
            // Posiible something been added
          ],
          "icon": null, // Optional
        }
      ],
    };
  },
}
</script>

<template>
  <div>
    <h1>Character Skills</h1>
    <div v-for="skill in skills" :key="skill.id">
      <SkillIcon :skill="skill"/>
    </div>
  </div>
</template>

<style scoped>

</style>