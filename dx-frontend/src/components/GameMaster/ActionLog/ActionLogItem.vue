<template>
  <div class="action-log-item">
    <div class="action-header">
      <SmallCharPreview :char="action.initiator" @select="handleSelect"/>
      <span class="action-type">Action: {{ action.action_type }}</span>
    </div>

    <div class="action-status">
      <span class="cycle">Cycle: {{ action.cycle.id }}</span>
      <span :class="{ true: 'status-true', false: 'status-false' }[action.accepted]" class="accepted">
        Accepted: {{ action.accepted ? 'Yes' : 'No' }}
      </span>
      <span :class="{ true: 'status-true', false: 'status-false' }[action.performed]" class="performed">
        Performed: {{ action.performed ? 'Yes' : 'No' }}
      </span>
    </div>

    <div v-if="action.targets.length" class="action-targets">
      <h4>Targets:</h4>
      <div class="targets-list">
        <SmallCharPreview
            v-for="target in action.targets"
            :key="target.id"
            :char="target"
            @select="handleSelect"
        />
      </div>
    </div>

    <SkillComponent v-if="action.skill" :skill="action.skill"/>
    <PositionComponent v-if="action.position" :position="action.position"/>

    <div v-if="action.impacts.length" class="action-impacts">
      <h4>Impacts:</h4>
      <div class="impacts-list">
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
import SkillComponent from './SkillComponent.vue';
import PositionComponent from './PositionComponent.vue';
import ImpactComponent from './ImpactComponent.vue';

export default {
  name: 'ActionLogItem',
  components: {
    SmallCharPreview,
    SkillComponent,
    PositionComponent,
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
  border: 1px solid #444;
  border-radius: 8px;
  padding: 1rem;
  background: #1c1c1c;
  margin-bottom: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.action-type {
  font-weight: bold;
  color: #e0e0e0;
  font-size: 0.9rem;
}

.action-status {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #e0e0e0;
}

.cycle {
  font-weight: bold;
  color: #ffcc00;
}

.accepted, .performed {
  font-weight: bold;
}

.status-true {
  color: #00ff00;
}

.status-false {
  color: #ff0000;
}

.action-targets, .action-impacts {
  margin-top: 1rem;
}

.targets-list, .impacts-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

h4 {
  font-size: 0.95rem;
  color: #e0e0e0;
  border-bottom: 1px solid #444;
  padding-bottom: 0.25rem;
  margin-bottom: 0.5rem;
}
</style>
