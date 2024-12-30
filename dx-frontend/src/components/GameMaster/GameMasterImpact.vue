<template>
  <div class="impact-container">
    <div class="character-select">
      <!-- Initiator Selection -->
      <label for="initiator">Initiator</label>
      <input
          v-if="!initiatorData"
          type="text"
          id="initiator"
          v-model="initiator"
          @change="fetchCharacterData('initiator')"
          placeholder="Enter Initiator ID"
      />
      <div v-else @click="cleanInitiatorData">
        <CharacterInlineCard :icon="initiatorData.biography.avatar" :name="initiatorData.name"/>
      </div>
    </div>

    <div class="character-select">
      <!-- Target Selection -->
      <label for="target">Target</label>
      <input
          v-if="!targetData"
          type="text"
          id="target"
          v-model="target"
          @change="fetchCharacterData('target')"
          placeholder="Enter Target ID"
      />
      <div v-else @click="cleanTargetData">
        <CharacterInlineCard :icon="targetData.biography.avatar" :name="targetData.name"/>
      </div>
    </div>

    <!-- Impact Type Dropdown -->
    <div class="dropdown">
      <label for="impactType">Impact Type</label>
      <select id="impactType" v-model="impactType">
        <option value="Heal">Heal</option>
        <option value="Damage">Damage</option>
      </select>
    </div>

    <!-- Impact Violation Dropdown -->
    <div class="dropdown">
      <label for="impactViolation">Impact Violation</label>
      <select id="impactViolation" v-model="impactViolation">
        <option value="Physical">Physical</option>
        <option value="Energy">Energy</option>
        <option value="None">None</option>
      </select>
    </div>

    <!-- Apply Button -->
    <button class="apply-button" @click="applyImpact">Apply</button>
  </div>
</template>

<script>
import {ActionGameApi, CharacterGameApi} from "@/api/backendService.js";
import CharacterInlineCard from "@/components/Game/Location/CharacterInlineCard.vue";

export default {
  name: "GameMasterImpact",
  components: {CharacterInlineCard},
  data() {
    return {
      initiator: "",
      target: "",
      impactType: "Heal",
      impactViolation: "Physical",
      initiatorData: null,
      targetData: null,
    };
  },
  methods: {
    async cleanInitiatorData() {
      this.initiatorData = null;
      this.initiator = "";
    },
    async cleanTargetData() {
      this.targetData = null;
      this.target = "";
    },
    async fetchCharacterData(type) {
      const id = type === "initiator" ? this.initiator : this.target;

      if (!id) return;

      // Placeholder for API call
      try {
        const response = (await CharacterGameApi.characterPlayerRetrieve(id)).data; // Replace with actual API call
        if (type === "initiator") {
          this.initiatorData = response;
        } else if (type === "target") {
          this.targetData = response;
        }
      } catch (error) {
        console.error(`Failed to fetch ${type} data:`, error);
      }
    },
    async applyImpact() {
      if (!this.initiator || !this.target) {
        alert("Please provide both initiator and target IDs.");
        return;
      }

      const impact = {
        initiator: this.initiator,
        target: this.target,
        impact_type: this.impactType,
        impact_violation: this.impactViolation,
      };
      await ActionGameApi.actionGmRegisterImpactCreate(impact);
      this.$emit("applyImpact", impact);
    },
  },
};
</script>

<style scoped>
.impact-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 0 auto;
  padding: 20px;
  background: #1e1e1e;
  color: white;
  border-radius: 10px;
  flex: 1;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.8);
}

.character-select {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.character-info {
  display: flex;
  align-items: center;
  gap: 15px;
  background: #2e2e2e;
  padding: 10px;
  border-radius: 8px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.dropdown {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

label {
  font-weight: bold;
  color: #bbbbbb;
}

select,
input {
  padding: 10px;
  border-radius: 5px;
  border: none;
  background: #2e2e2e;
  color: white;
  font-size: 14px;
}

.apply-button {
  padding: 10px 20px;
  background: #007bff;
  border: none;
  border-radius: 5px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.apply-button:hover {
  background: #0056b3;
}
</style>
