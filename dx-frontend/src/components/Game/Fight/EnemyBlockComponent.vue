<script>
import EnemyComponent from "@/components/Game/Fight/EnemyComponent.vue";
import {PlayerFightParticipant} from "@/models/Player";

export default {
  name: "EnemyBlockComponent",
  components: {
    EnemyComponent
  },
  data() {
    return {
      selected: []
    }
  },
  props: {
    enemies: {
      type: Array[PlayerFightParticipant],
      required: true
    }
  },
  methods: {
    processSelection(enemy, selected) {
      // allows only one enemy to be selected at a time by this method
      console.log('Selected enemy:', enemy);
      if (selected) {
        this.selected = [enemy];
      } else {
        this.selected = [];
      }
      this.$emit('selection', selected ? enemy : null);
    },
    isSelectedEnemy(player) {
      return this.selected.find(enemy => enemy.id === player.id);
    },
    selectEnemy(enemy) {
      this.processSelection(enemy, true);
    },
    selectNone() {
      this.selected = [];
    },
    selectAll() {
      this.selected = this.enemies;
    },
    blink() {
      this.selectAll()
      setTimeout(() => {
        this.selectNone()
      }, 1000)
    }
  }
}
</script>

<template>
  <div class="enemy-block vertical-layout">
    <enemy-component
        v-for="(enemy, index) in enemies"
        :key="enemy.id || index"
        :player="enemy"
        @selection="processSelection"
        :selected="isSelectedEnemy(enemy)"
    />
  </div>
</template>

<style scoped>
.enemy-block {
  display: flex;
  gap: 10px; /* Adjust spacing as needed */
  width: 30vh;
  justify-content: space-between;
  position: absolute;
  left: 95%;
  margin-left: -32vh;
}
</style>
