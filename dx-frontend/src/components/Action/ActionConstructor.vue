<template>
  <div class="action-constructor">
    <div class="action-constructor-holder">
      <GameObjectSelector
          :gameObjects="availableGameObjects"
          :selectedId="selectedGameObjectId"
          @update:selectedId="updateSelectedGameObjectId"
      />
      <ActionPreview v-if="selectedAction !== null" :action="selectedAction"/>
      <GlassButton @click="$emit('cancelAction')">Cancel</GlassButton>
      <GlassButton v-if="selectedGameObjectId && selectedAction" @click="applyAction">Apply</GlassButton>
    </div>
    <div class="action-selector-holder">
      <ActionSelector
          :actions="availableActions"
          :preSelected="selectedGameObjectId"
          @action-selected="updateSelectedAction"
      />
    </div>
  </div>
</template>

<script>
import GameObjectSelector from "@/components/Selectors/GameObjectSelector.vue";
import ActionPreview from "@/components/Pickers/ActionPreview.vue";
import GlassPlayButton from "@/components/btn/GlassPlayButton.vue";
import ActionSelector from "@/components/Selectors/ActionSelector.vue";
import GlassButton from "@/components/btn/Glass.vue";

export default {
  name: "ActionConstructor",
  components: {
    GlassButton,
    GameObjectSelector,
    ActionPreview,
    GlassPlayButton,
    ActionSelector,
  },
  props: {
    availableGameObjects: {
      type: Array,
      required: true,
    },
    availableActions: {
      type: Array,
      required: true,
    },
    preSelectedTarget: {
      type: String,
      default: null,
    },
  },
  watch: {
    preSelectedTarget(newTarget) {
      this.updateSelectedGameObjectId(newTarget);
    },
  },
  data() {
    return {
      selectedGameObjectId: null,
      selectedAction: null,
    };
  },
  mounted() {
    if (this.preSelectedTarget !== null) {
      this.updateSelectedGameObjectId(this.preSelectedTarget);
    }
  },
  methods: {
    reset() {
      this.selectedAction = null;
      this.selectedGameObjectId = null;
    },
    applyAction() {
      if (!this.selectedAction || !this.selectedGameObjectId) return;

      const actionObject = {
        actionType: "USE_SKILL", // TODO: add support of actions on backend
        actionData: {},
        skill: this.selectedAction.id,
        targets: [this.selectedGameObjectId], // Selected game object as target
      };

      this.$emit("applyAction", actionObject);
      this.reset();
    },
    updateSelectedGameObjectId(id) {
      this.selectedGameObjectId = id;
    },
    updateSelectedAction(action) {
      this.selectedAction = action;
    },
  },
};
</script>

<style scoped>
.action-constructor {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 0.5rem;
}

.action-constructor-holder {
  display: flex;
  align-items: center;
  flex-direction: row;
  gap: 0.1rem;
}

.action-selector-holder {
  width: 100%;
}
</style>
