<template>
  <div class="action-card">
    <div class="card-content">
      <div class="card-front">
        <slot name="icon"></slot>
      </div>
      <div class="card-back">
        <div class="card-header">
          <slot name="icon"></slot>
          {{ action.getName() }}
        </div>
        <div class="card-body">
          <div class="row action">
            At: {{ action.getTargetName() }}
          </div>
          <div class="row points">AP: {{ action.getActionPointsCost() }}</div>
          <div class="row energy">Energy: {{ action.getEnergyCost() }}</div>
          <div class=" row management horizontal-layout">
            <div class="move" @click="moveActionLeft"> <- </div>
            <div id="delete"  @click="deleteAction"> x </div>
            <div id="duplicate" @click="duplicateAction"> d </div>
            <div class="move" @click="moveActionRight"> -> </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Action from "@/models/Action";
export default {
  name: 'ActionCardComponent',
  props: {
    action: {
      type: Action,
      required: true
    },
  },
  methods: {
    deleteAction() {
      console.log('Deleting action:', this.action);
      this.$emit('delete', this.action);
    },
    duplicateAction() {
      console.log('Duplicating action:', this.action);
      this.$emit('duplicate', this.action);
    },
    moveActionLeft() {
      this.moveAction('left', this.action);
    },
    moveActionRight() {
      this.moveAction('right', this.action);
    },
    moveAction(direction) {
      console.log('Moving action:', this.action, direction);
      this.$emit('move', this.action, direction);
    },
  }
}
</script>

<style scoped>
.action-card {
  width: 4rem;
  height: 6rem;
  position: relative;
  margin: 0;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.action-card:hover {
  margin: 0 1rem 1rem -3rem;
  height: 10rem;
  width: 5rem;
  padding: 2rem;
  z-index: 2;
}

#delete:hover {
  color: red;
}

#duplicate:hover {
  color: yellow;
}

.move:hover {
  color: #00bfff;
}
.card-content {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(46, 42, 42, 0.9);
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 191, 255, 0.5);
  color: white;
  font-family: 'Orbitron', sans-serif;
  overflow: hidden;
}

.card-front {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  transition: opacity 0.3s ease-in-out;
}

.card-back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(46, 42, 42, 0.9);
  border-radius: 10px;
  padding: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.row {
  display: flex;
  justify-content: space-between;
  margin: 1em;
}

.action-card:hover .card-front {
  opacity: 0;
}

.action-card:hover .card-back {
  opacity: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 191, 255, 0.5);
  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;
}


.card-body {
  display: flex;
  flex-direction: column;
}

.action {
  font-size: 0.8rem;
}


.points,
.energy {
  font-size: 0.7rem;
}


</style>
