<template>
  <div class="action-constructor-container">
    <div class="action-constructor-holder">
      <GameObjectSelector
          :gameObjects="availableGameObjects"
          :selectedId="selectedGameObjectId"
          @update:selectedId="updateSelectedGameObjectId"
      />
      <ActionPreview v-if="computedSelectedSkill !== null" :action="computedSelectedSkill"/>
      <GlassButton @click="$emit('cancelAction')">Cancel</GlassButton>
      <GlassButton v-if="selectedGameObjectId && computedSelectedSkill" @click="applyAction">Apply</GlassButton>
    </div>
    <TabSwitcher :tabs="
      [
          { id: 'skillSelector', name: 'Skills' },
          { id: 'itemSelector', name: 'Items' },
      ]
      "
                 @tab-switched="switchTab"
                 initialTabId="skillSelector"
    />
    <div class="action-selector-holder" v-if="true">

      <SkillSelector
          v-if="currentTab === 'skillSelector'"
          :actions="availableSkills"
          :preSelected="selectedGameObjectId"
          @skill-selected="updateSelectedSkill"
      />
      <ItemSelector
          v-if="currentTab === 'itemSelector'"
          :characterItems="availableItems"
          @item-selected="updateSelectedItem"
      />
    </div>
  </div>
</template>

<script>
import GameObjectSelector from "@/components/Selectors/GameObjectSelector.vue";
import ActionPreview from "@/components/Pickers/ActionPreview.vue";
import GlassPlayButton from "@/components/btn/GlassPlayButton.vue";
import SkillSelector from "@/components/Selectors/SkillSelector.vue";
import GlassButton from "@/components/btn/Glass.vue";
import ItemSelector from "@/components/Selectors/ItemSelector.vue";
import TabSwitcher from "@/components/Tabs/TabSwitcher.vue";

export default {
  name: "ActionConstructor",
  components: {
    TabSwitcher,
    ItemSelector,
    GlassButton,
    GameObjectSelector,
    ActionPreview,
    GlassPlayButton,
    SkillSelector,
  },
  computed: {
    computedSelectedSkill() {
      return this.selectedSkill || this.selectedItem?.item?.skill;
    },
    actionData() {
      if (!this.selectedItem && !this.selectedSkill) return null;
      return {
        actionType: this.selectedItem ? "USE_ITEM" : "USE_SKILL",
        actionData: {},
        skill: this.selectedItem ? null : this.selectedSkill.id,
        item: this.selectedItem ? this.selectedItem.id : null,
        targets: [this.selectedGameObjectId], // Selected game object as target
      };
    },
  },
  props: {
    availableGameObjects: {
      type: Array,
      required: true,
    },
    availableSkills: {
      type: Array,
      required: true,
    },
    availableItems: {
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
      selectedSkill: null,
      selectedItem: null,
      currentTab: "skillSelector",
    };
  },
  mounted() {
    if (this.preSelectedTarget !== null) {
      this.updateSelectedGameObjectId(this.preSelectedTarget);
    }
  },
  methods: {
    switchTab(tabId) {
      this.currentTab = tabId;
    },
    reset() {
      this.selectedSkill = null;
      this.selectedItem = null;
    },
    applyAction() {
      if (!(this.selectedSkill || this.selectedItem) || !this.selectedGameObjectId) return;
      this.$emit("applyAction", this.actionData);
      this.reset();
    },
    updateSelectedGameObjectId(id) {
      this.selectedGameObjectId = id;
    },
    updateSelectedSkill(skill) {
      this.reset()
      this.selectedSkill = skill;
    },
    updateSelectedItem(item) {
      this.reset()
      this.selectedItem = item;
    }
  },
};
</script>

<style scoped>
.action-constructor-container {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
}

.action-constructor-holder {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;
  width: 100%;
  padding: 0.5rem;
  gap: 0.1rem;
}

.action-selector-holder {
  width: 100%;
  height: 20rem;
  max-height: 20rem;
  display: flex;
  flex-direction: row;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;
  gap: 0.1rem;
  overflow-x: hidden;
}
</style>
