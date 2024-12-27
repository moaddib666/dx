<template>
  <div class="action-log">
    <div class="action-log-header">
      <h3>Action Log</h3>
      <button class="refresh-button" @click="$emit('refresh')">Refresh</button>
    </div>
    <div v-if="sortedCycleKeys.length > 0" class="action-list">
      <div v-for="cycleId in sortedCycleKeys" :key="cycleId" class="cycle-group">
        <div class="cycle-header">Cycle: {{ cycleId }}</div>
        <div class="cycle-actions">
          <ActionLogItem
              v-for="action in groupedActions[cycleId]"
              :key="action.id"
              :action="action"
              @selectInitiator="handleInitiatorSelect"
              @selectTarget="handleTargetSelect"
          />
        </div>
      </div>
    </div>
    <div v-else>
      <p>No actions available</p>
    </div>
  </div>
</template>

<script>
import ActionLogItem from "./ActionLogItem.vue";

export default {
  name: "ActionLog",
  components: {
    ActionLogItem,
  },
  props: {
    actions: {
      type: Array,
      required: true,
    },
  },
  computed: {
    groupedActions() {
      return this.actions.reduce((groups, action) => {
        const cycleId = action.cycle.id;
        if (!groups[cycleId]) {
          groups[cycleId] = [];
        }
        groups[cycleId].push(action);
        return groups;
      }, {});
    },
    sortedCycleKeys() {
      return Object.keys(this.groupedActions)
          .map(Number)
          .sort((a, b) => b - a);
    },
  },
  methods: {
    handleInitiatorSelect(id) {
      console.log("Selected Initiator ID:", id);
    },
    handleTargetSelect(id) {
      console.log("Selected Target ID:", id);
    },
  },
};
</script>

<style scoped>
.action-log {
  border: 1px solid #444;
  border-radius: 8px;
  padding: 1.5rem;
  background: #1c1c1c;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.action-log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.refresh-button {
  padding: 0.5rem 1rem;
  background: #ffcc00;
  border: none;
  border-radius: 4px;
  color: #1c1c1c;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.refresh-button:hover {
  background: #ffd633;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cycle-group {
  border: 1px solid #555;
  border-radius: 6px;
  background: #222;
  padding: 1rem;
}

.cycle-header {
  font-size: 1rem;
  font-weight: bold;
  color: #ffcc00;
  margin-bottom: 1rem;
  border-bottom: 1px solid #444;
  padding-bottom: 0.5rem;
}

.cycle-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
</style>
