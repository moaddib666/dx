<template>
  <div class="user-action-log">
    <div v-for="(action, index) in actions" :key="action.id">
      <!-- Separator if cycle changes -->
      <div v-if="shouldInsertSeparator(index)" class="cycle-separator">
        Cycle: {{ action.cycle }}
      </div>

      <!-- UserActionLogItem Component -->
      <UserActionLogItem
          :initiator="action.initiator"
          :actionType="action.action_type"
          :skill="action.skill"
          :data="action.data"
          :impacts="action.impacts"
      />
    </div>
  </div>
</template>

<script>
import UserActionLogItem from "./UserActionLogItem.vue";

export default {
  name: "UserActionLog",
  components: {
    UserActionLogItem,
  },
  props: {
    actions: {
      type: Array,
      required: true,
    },
  },
  methods: {
    shouldInsertSeparator(index) {
      if (index === 0) return true; // Always add a separator for the first item
      return this.actions[index].cycle !== this.actions[index - 1].cycle;
    },
  },
};
</script>

<style scoped>
.user-action-log {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.cycle-separator {
  font-weight: bold;
  color: yellow;
  margin: 0.5rem 0;
  border-top: 0.2rem solid rgba(255, 255, 255, 0.5);
  padding-top: 0.5rem;
}
</style>
