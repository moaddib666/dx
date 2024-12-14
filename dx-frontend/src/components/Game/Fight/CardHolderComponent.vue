<template>
  <div class="card-holder">
    <ActionCardComponent
        v-for="(card, index) in cards"
        :key="index"
        :action="card.action"
        @move="moveAction"
        @delete="deleteAction"
        @duplicate="duplicateAction"

    >
      <template v-slot:icon>
        {{ card.icon }}
      </template>
    </ActionCardComponent>
  </div>
</template>

<script>
import ActionCardComponent from './ActionCardComponent.vue';
import Action from "@/models/Action";

export default {
  name: 'CardHolderComponent',
  components: {
    ActionCardComponent
  },
  props: {
    cards: {
      type: Array[Action],
      required: true
    }
  },
  methods: {
    moveAction(action, direction) {
      console.log('Moving card:', action, direction);
      this.$emit('move', action, direction);
    },
    deleteAction(action) {
      console.log('Deleting card:', action);
      this.$emit('delete', action);
    },
    duplicateAction(action) {
      console.log('Duplicating card:', action);
      this.$emit('duplicate', action);
    }
  }
}
</script>

<style scoped>
.card-holder {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  align-items: flex-end;
  padding: 2vh;
  height: 20vh;
}
</style>
