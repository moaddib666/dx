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

    <!-- Skills Dropdown -->
    <DropdownActionSelector :skills="availableActions" @action-selected="setPreparedAction" :selected-action-id="preparedActionId" v-if="initiator" class="dropdown"/>
    <!-- Submit Button -->
    <LandingButton :action="applyImpact">
      Apply
    </LandingButton>
  </div>
</template>

<script>
import {ActionGameApi, CharacterGameApi, SkillsGameApi} from "@/api/backendService.js";
import CharacterInlineCard from "@/components/Game/Location/CharacterInlineCard.vue";
import DropdownActionSelector from "@/components/Action/DropdownActionSelector.vue";
import LandingButton from "@/components/btn/LandingButton.vue";
import ActionService from "@/services/actionsService.js";

export default {
  name: "GameMasterImpact",
  components: {LandingButton, DropdownActionSelector, CharacterInlineCard},
  data() {
    return {
      initiator: "",
      target: "",
      impactType: "Heal",
      impactViolation: "Physical",
      initiatorData: null,
      targetData: null,
      availableSkills: [],
      preparedActionId: null,
      actionService: null,
    };
  },
  async created() {
    this.actionService = new ActionService(ActionGameApi);
  },
  computed: {
    availableActions() {
      if (!this.availableSkills) return [];
      return this.availableSkills.map((skill) => (skill.skill));
    },
  },
  methods: {
    async setPreparedAction(actionId) {
      this.preparedActionId = actionId;
    },
    async cleanInitiatorData() {
      this.initiatorData = null;
      this.initiator = "";
    },
    async cleanTargetData() {
      this.targetData = null;
      this.target = "";
    },
    async setInitiator(id) {
      this.initiator = id;
      await this.fetchCharacterData("initiator");
    },
    async setTarget(id) {
      this.target = id;
      await this.fetchCharacterData("target");
    },
    async fetchCharacterSkills(id) {
      this.availableSkills = (await SkillsGameApi.skillsGmSkillsList(id)).data.results;
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
      if (!this.initiator || !this.target || !this.preparedActionId) {
        alert("Please fill all required fields.");
        return;
      }

      const action = {
        actionType: "USE_SKILL",
        actionData: {},
        position: null,
        targets: [this.target],
        skill: this.preparedActionId,
        characterId: this.initiator,
      }

      const result = await this.actionService.performActionForCharacter(action);
      this.$emit("applied", result);
      //
      // const impact = {
      //   initiator: this.initiator,
      //   target: this.target,
      //   impact_type: this.impactType,
      //   impact_violation: this.impactViolation,
      // };
      // await ActionGameApi.actionGmRegisterImpactCreate(impact);
      // this.$emit("applyImpact", impact);
    },
  },
  watch: {
    initiator(val) {
      this.initiatorData = null;
      if (val) this.fetchCharacterSkills(this.initiator); else this.availableSkills = [];
    },
  }
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
  width: 100%;
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
