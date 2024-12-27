<template>
  <div class="action-log-item">
    <div class="action-row">
      <SmallCharPreview class="initiator" :char="action.initiator" @select="handleSelect" />
      <div class="action-info">
        <span class="action-id">ID: {{ action.id }}</span>
        <span class="action-type">Type: {{ action.action_type }}</span>
        <span class="cycle">Cycle: {{ action.cycle.id }}</span>
        <span class="status">
          <span :class="{ 'status-true': action.accepted, 'status-false': !action.accepted }">
            Accepted: {{ action.accepted ? 'Yes' : 'No' }}
          </span>
          <span :class="{ 'status-true': action.performed, 'status-false': !action.performed }">
            Performed: {{ action.performed ? 'Yes' : 'No' }}
          </span>
        </span>
      </div>
      <div v-if="action.accepted && !action.performed" class="targets-row">
        <SmallCharPreview
            v-for="target in action.targets"
            :key="target.id"
            :char="target"
            @select="handleSelect"
        />
      </div>
      <div v-if="action.performed" class="impacts-row">
        <ImpactComponent
            v-for="impact in action.impacts"
            :key="impact.id"
            :impact="impact"
            @selectTarget="handleSelect"
        />
      </div>
    </div>
  </div>
</template>

<script>
import SmallCharPreview from './SmallCharPreview.vue';
import ImpactComponent from './ImpactComponent.vue';

export default {
  name: 'ActionLogItem',
  components: {
    SmallCharPreview,
    ImpactComponent,
  },
  props: {
    action: Object,
  },
  methods: {
    handleSelect(id) {
      console.log('Selected ID:', id);
    },
  },
};
</script>

<style scoped>
.action-log-item {
  display: flex;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 0.5rem;
  background: #1c1c1c;
  align-items: center;
  gap: 0.5rem;
}

.action-row {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 0.6rem;
}

.initiator {
  flex: 0 0 3rem; /* Fixed size for SmallCharPreview */
}

.action-info {
  flex: 0 0 15rem; /* Fixed size for action-info */
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.75rem;
  color: #ccc;
}

.action-id {
  font-weight: bold;
  color: #ffcc00;
}

.action-type, .cycle {
  color: #aaa;
}

.status {
  display: flex;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.status-true {
  color: #00ff00;
}

.status-false {
  color: #ff0000;
}

.targets-row, .impacts-row {
  flex: 1; /* Dynamic size for targets or impacts */
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
}

.targets-row > *:not(:last-child), .impacts-row > *:not(:last-child) {
  margin-right: 0.3rem;
}

h4 {
  font-size: 0.8rem;
  color: #ffcc00;
}
</style>
