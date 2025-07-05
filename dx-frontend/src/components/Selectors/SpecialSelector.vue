<template>
  <div class="special-selector">
    <!-- Render dynamically based on specialActions prop -->
    <SkillIcon
        v-for="(special, index) in specialActions"
        :key="special.action_type"
        :useSlotIcon="true"
        :fade="!canPerformSpecialAction(special)"
        @click="selectItem(special)"
        :skill="formatSkill(special)"
        :style="{ cursor: canPerformSpecialAction(special) ? 'pointer' : 'not-allowed' }"
    >
      <img
          :src="special.icon"
          :alt="special.name"
          style="width: 100%; height: 100%; object-fit: contain;"
      />
    </SkillIcon>
  </div>
</template>

<script>
import SkillIcon from "@/components/Action/ActionIcon.vue";

export default {
  name: "SpecialSelector",
  components: { SkillIcon },
  props: {
    isSafe: {
      type: Boolean,
      default: false,
    },
    playerService: {
      type: Object,
      default: null,
    },
    specialActions: {
      type: Array,
      required: true,
      default: () => [
        {
          "action_type": "SNATCH_ITEM",
          "name": "Snatch",
          "description": "The Snatch Item skill is a cunning and opportunistic ability that allows players to inspect a target for valuable items and attempt to steal them under the right conditions. It demands precision, stealth, and quick reflexes, making it a favorite among thieves, rogues, and those with a flair for seizing opportunities.",
          "immediate": true,
          "final": false,
          "icon": "http://localhost:8000/media/icons/specialActions/Snatch.webp",
          "cost": [
            {
              "kind": "Action Points",
              "value": 2
            },
            {
              "kind": "Energy",
              "value": 3
            }
          ]
        },
        {
          "action_type": "INSPECT",
          "name": "Inspect",
          "description": "The Inspect action is a utility skill that allows players to gather detailed information about a target object or character. However, its effectiveness depends on the target’s level, protection mechanisms, and the player’s stats. While not all inspections yield useful results, a successful attempt can reveal critical details, providing a strategic edge.",
          "immediate": true,
          "final": false,
          "icon": "http://localhost:8000/media/icons/specialActions/inspect.webp",
          "cost": [
            {
              "kind": "Action Points",
              "value": 2
            },
            {
              "kind": "Energy",
              "value": 3
            }
          ]
        },
        {
          "action_type": "LONG_REST",
          "name": "Long Rest",
          "description": "The Long Rest action allows players to recover their health and energy in designated safe locations. It is a vital utility for regaining strength after battles and preparing for future challenges. Additionally, a long rest can provide temporary bonuses or buffs, making it an essential part of strategic gameplay.",
          "immediate": false,
          "final": true,
          "icon": "http://localhost:8000/media/icons/specialActions/long_rest2.webp",
          "cost": [
            {
              "kind": "Action Points",
              "value": 4
            }
          ]
        }
      ],
    },
  },
  methods: {
    /**
     * Emit formatted special action when selected
     * @param {Object} special
     */
    selectItem(special) {
      // Only emit the event if the player has enough resources
      if (this.canPerformSpecialAction(special)) {
        this.$emit("special-selected", this.formatSpecial(special));
      }
    },

    /**
     * Check if the player has enough resources to perform the special action
     * @param {Object} special - The special action to check
     * @returns {boolean} - Whether the action can be performed
     */
    canPerformSpecialAction(special) {
      // If playerService is not available, assume action can be performed
      if (!this.playerService) return true;

      // Check if the special action has costs
      if (!special.cost || !Array.isArray(special.cost) || special.cost.length === 0) return true;

      // Check each cost type
      for (const cost of special.cost) {
        const currentValue = this.playerService.getCurrentAttributeValue(cost.kind);
        // If we can't get the current value or it's less than the cost, return false
        if (currentValue === null || currentValue < cost.value) {
          return false;
        }
      }

      return true;
    },

    /**
     * Format the special action for the emitted object
     * @param {Object} special
     * @returns {Object}
     */
    formatSpecial(special) {
      return {
        id: special.action_type,
        actionType: special.action_type,
        actionData: {}, // Adjust if additional data is required
        skill: this.formatSkill(special),
      };
    },

    /**
     * Format the special action into the expected skill object
     * @param {Object} special
     * @returns {Object}
     */
    formatSkill(special) {
      return {
        id: special.action_type,
        name: special.name,
        type: "special",
        icon: special.icon,
        cost: special.cost.map((c) => ({ kind: c.kind, value: c.value })), // Ensure cost format matches
      };
    },
  },
};
</script>

<style scoped>
.special-selector {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping of icons */
  gap: 0.5rem; /* Space between icons */
  justify-content: flex-start; /* Align icons to the start */
  align-items: flex-start; /* Align icons */
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>
