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
              :gmMode="gmMode"
          />
        </div>
      </div>
    </div>
    <div v-else>
      <p>No characterItems available</p>
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
    gmMode: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    groupedActions() {
      return this.actions.reduce((groups, action) => {
        const cycleNumber = action.cycle.number;
        if (!groups[cycleNumber]) {
          groups[cycleNumber] = [];
        }
        groups[cycleNumber].push(action);
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

.action-log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.refresh-button {
  padding: 0.3rem 0.6rem;
  background: #ffcc00;
  border: none;
  border-radius: 4px;
  color: #1c1c1c;
  font-weight: bold;
  font-size: 0.75rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.refresh-button:hover {
  background: #ffd633;
}

.action-list {
  display: flex;
  flex-direction: column;
}

.cycle-group {
  margin-bottom: 1rem;
}

.cycle-header {
  font-size: 0.85rem;
  font-weight: bold;
  color: #ffcc00;
  margin-bottom: 0.25rem;
  border-bottom: 1px solid #444;
  padding-bottom: 0.25rem;
}

.cycle-actions {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
</style>
