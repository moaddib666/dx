<template>
  <div class="dropdown-skill-selector">
    <!-- Current Selected Skill -->
    <div class="selected-skill" @click="toggleDropdown">
      <ActionIconMini :skill="currentSkill" class="icon"/>
      <CostMiniVisualizer :cost="currentSkill.cost" class="cost"/>
      <span class="dropdown-arrow">▼</span>
    </div>

    <!-- Dropdown List -->
    <div v-if="dropdownVisible" class="dropdown-list">
      <div
          v-for="skill in skills"
          :key="skill.id"
          class="dropdown-item"
          @click="selectSkill(skill.id)"
      >
        <ActionIconMini :skill="skill" class="icon"/>
        <CostMiniVisualizer :cost="skill.cost" class="cost"/>
      </div>
    </div>
  </div>
</template>

<script>
import ActionIconMini from "@/components/Action/ActionIconMini.vue";
import CostMiniVisualizer from "@/components/Action/CostMiniVisualizer.vue";

export default {
  name: "DropdownActionSelector",
  components: {
    CostMiniVisualizer,
    ActionIconMini,
  },
  props: {
    skills: {
      type: Array,
      required: true, // Array of skills
    },
    selectedActionId: {
      type: Number,
      default: null, // ID of the currently selected skill
    },
  },
  data() {
    return {
      dropdownVisible: false, // Tracks whether the dropdown is open
    };
  },
  computed: {
    currentSkill() {
      // Get the currently selected skill from the skills array
      return this.skills.find((skill) => skill.id === this.selectedActionId) || {
        name: "Select Skill",
        icon: null,
      };
    },
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    selectSkill(skillId) {
      this.$emit("action-selected", skillId); // Emit the selected skill ID
      this.dropdownVisible = false; // Close the dropdown
    },
  },
};
</script>

<style scoped>
.dropdown-skill-selector {
  position: relative;
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  justify-content: center;
  align-items: flex-start;
}

.selected-skill {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: background 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}

.selected-skill:hover {
  background: rgba(0, 0, 0, 0.9);
}

.dropdown-arrow {
  color: white;
  font-size: 0.8rem;
  margin-left: auto;
  justify-self: flex-end;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  width: 100%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  z-index: 1000;
  height: 12rem;
  overflow-y: auto;

  /* Custom scrollbar */
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;

}

.dropdown-item {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 0.3rem;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 0.5rem;
  flex: 1;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.06);
}

.dropdown-item:not(:last-child) {
  margin-bottom: 0.3rem;
}

.icon {
  display: flex;
}
.cost {
  display: flex;
  justify-self: flex-end;
  margin-left: auto;
}
</style>
