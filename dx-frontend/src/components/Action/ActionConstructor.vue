<template>
  <div class="action-constructor-container">
    <div class="action-constructor-holder">
      <GameObjectSelector
          :gameObjects="availableGameObjects"
          :selectedId="selectedGameObjectId"
          @update:selectedId="updateSelectedGameObjectId"
      />
      <ActionPreview v-if="computedSelectedSkill !== null" :action="computedSelectedSkill"/>
      <CompactButton @click="$emit('cancelAction')">Cancel</CompactButton>
      <CompactButton v-if="selectedGameObjectId && computedSelectedSkill" @click="applyAction">Apply</CompactButton>
    </div>
    <TabSwitcher :tabs="
      [
          { id: 'skillSelector', name: 'Skills' },
          { id: 'itemSelector', name: 'Items' },
          { id: 'specialSelector', name: 'Special' },
      ]
      "
                 @tab-switched="switchTab"
                 initialTabId="skillSelector"
    />
    <TypeFilter
      :selectedTypes="selectedTypes"
      @update:selectedTypes="selectedTypes = $event"
    />
    <div class="action-selector-holder">
      <SkillSelector
          v-if="currentTab === 'skillSelector'"
          :key="'skillSelector-' + selectedTypes.join('-')"
          :actions="availableSkills"
          :preSelected="selectedGameObjectId"
          :playerService="playerService"
          :selectedTypes="selectedTypes"
          @skill-selected="updateSelectedSkill"
      />
      <ItemSelector
          v-if="currentTab === 'itemSelector'"
          :key="'itemSelector-' + selectedTypes.join('-')"
          :characterItems="availableItems"
          :playerService="playerService"
          :selectedTypes="selectedTypes"
          @item-selected="updateSelectedItem"
      />
      <SpecialSelector
          v-if="currentTab === 'specialSelector'"
          :key="'specialSelector-' + selectedTypes.join('-')"
          :isSafe="isSafe"
          :special-actions="availableSpecials"
          :playerService="playerService"
          :selectedTypes="selectedTypes"
          @special-selected="updateSelectedSpecial"
      ></SpecialSelector>
    </div>
  </div>
</template>

<script>
import GameObjectSelector from "@/components/Selectors/GameObjectSelector.vue";
import ActionPreview from "@/components/Pickers/ActionPreview.vue";
import CompactPlayButton from "@/components/btn/CompactPlayButton.vue";
import SkillSelector from "@/components/Selectors/SkillSelector.vue";
import CompactButton from "@/components/btn/CompactButton.vue";
import ItemSelector from "@/components/Selectors/ItemSelector.vue";
import TabSwitcher from "@/components/Tabs/TabSwitcher.vue";
import SpecialSelector from "@/components/Selectors/SpecialSelector.vue";
import TypeFilter from "@/components/Filters/TypeFilter.vue";

export default {
  name: "ActionConstructor",
  components: {
    SpecialSelector,
    TabSwitcher,
    ItemSelector,
    CompactButton,
    GameObjectSelector,
    ActionPreview,
    CompactPlayButton,
    SkillSelector,
    TypeFilter,
  },
  computed: {
    computedSelectedSkill() {
      return this.selectedSkill || this.selectedItem?.item?.skill || this.selectedSpecial?.skill;
    },
    actionData() {
      if (!this.selectedItem && !this.selectedSkill && !this.selectedSpecial) return null;

      if (this.selectedSpecial) {
        return {
          actionType: this.selectedSpecial.actionType,
          actionData: this.selectedSpecial.actionData,
          skill: null,
          item: null,
          targets: [this.selectedGameObjectId], // Selected game object as target
        };
      }
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
      default: () => [],
    },
    isSafe: {
      type: Boolean,
      required: false,
    },
    availableSkills: {
      type: Array,
      default: () => [],
    },
    availableItems: {
      type: Array,
      default: () => [],
    },
    availableSpecials: {
      type: Array,
      default: () => [],
    },
    preSelectedTarget: {
      type: String,
      default: null,
    },
    playerService: {
      type: Object,
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
      selectedSpecial: null,
      currentTab: "skillSelector",
      selectedTypes: [], // Array to store selected types for filtering
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
      this.selectedTypes = []; // Reset selected types when switching tabs
    },
    reset() {
      this.selectedSkill = null;
      this.selectedItem = null;
      this.selectedSpecial = null;
    },
    applyAction() {
      if (!(this.selectedSkill || this.selectedItem || this.selectedSpecial) || !this.selectedGameObjectId) return;
      this.$emit("applyAction", this.actionData);
      this.reset();
    },
    updateSelectedSpecial(special) {
      this.reset()
      this.selectedSpecial = special;
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
  width: 39vw;
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
