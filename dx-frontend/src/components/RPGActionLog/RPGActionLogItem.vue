<template>
  <div class="action-log-item">
    <!-- Action Description -->
    <div class="action-section">
      <div class="action-text">
        <CharacterInlineDetails
          :char-id="action.initiator"
          :gm-mode="false"
          class="highlight-initiator"
        />
        <span v-html="getActionTemplate()"></span>
        <template v-if="hasNonSelfTargets">
          <CharacterInlineDetails
            v-for="targetId in action.targets"
            :key="targetId"
            :char-id="targetId"
            :gm-mode="false"
            class="highlight-target"
          />
        </template>
      </div>
    </div>

    <!-- Outcomes Section -->
    <div class="outcomes-section" v-if="action.impacts && action.impacts.length > 0">
      <div
        v-for="impact in action.impacts"
        :key="impact.id"
        class="outcome-text"
      >
        <span v-html="getOutcomeTemplate(impact)"></span>
        <CharacterInlineDetails
          v-if="impact.target !== action.initiator"
          :char-id="impact.target"
          :gm-mode="false"
          class="highlight-target"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, withDefaults, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { type CharacterActionLog, ActionType5f8Enum, OutcomeEnum, ImpactTypeEnum, ImpactViolationType } from "@/api/dx-backend";
import CharacterInlineDetails from "@/components/Character/CharacterInlineDetails.vue";

interface Props {
  action: CharacterActionLog;
}

const props = withDefaults(defineProps<Props>(), {});
const { t } = useI18n();

// Computed properties
const hasTargets = computed(() => {
  return props.action.targets && props.action.targets.length > 0;
});

const isSelfTargeting = computed(() => {
  return hasTargets.value && props.action.targets.length === 1 && props.action.targets[0] === props.action.initiator;
});

const hasNonSelfTargets = computed(() => {
  return hasTargets.value && !isSelfTargeting.value;
});

// Template definitions for different action types (without character names - handled by components)
const actionTemplates = {
  [ActionType5f8Enum.UseSkill]: {
    base: " using the <span class='highlight-skill'>{skill}</span> on ",
    noTarget: " using the <span class='highlight-skill'>{skill}</span>.",
    noSkill: " performing an action on ",
    self: " using the <span class='highlight-skill'>{skill}</span> on <span class='highlight-target'>self</span>."
  },
  [ActionType5f8Enum.UseItem]: {
    base: " using the <span class='highlight-item'>{item}</span> on ",
    noTarget: " using the <span class='highlight-item'>{item}</span>.",
    self: " using the <span class='highlight-item'>{item}</span> on <span class='highlight-target'>self</span>."
  },
  [ActionType5f8Enum.SnatchItem]: {
    base: " crawling and want to snatch something from the ",
    noTarget: " attempting to snatch an item.",
    self: " examining their own belongings."
  },
  [ActionType5f8Enum.Move]: {
    base: " moving to a new position.",
    noTarget: " moving around.",
    self: " repositioning themselves."
  },
  [ActionType5f8Enum.DiceRoll]: {
    base: " rolling dice.",
    noTarget: " making a dice roll.",
    self: " rolling dice for themselves."
  },
  [ActionType5f8Enum.Inspect]: {
    base: " inspecting ",
    noTarget: " looking around carefully.",
    self: " examining <span class='highlight-target'>themselves</span>."
  },
  [ActionType5f8Enum.Gift]: {
    base: " giving a gift to ",
    noTarget: " preparing a gift.",
    self: " keeping something for <span class='highlight-target'>themselves</span>."
  },
  default: {
    base: " performing <span class='highlight-skill'>{actionType}</span> on ",
    noTarget: " performing <span class='highlight-skill'>{actionType}</span>.",
    self: " performing <span class='highlight-skill'>{actionType}</span> on <span class='highlight-target'>self</span>."
  }
};

// Outcome templates based on dice roll results and impact types (without character names)
const outcomeTemplates = {
  [OutcomeEnum.CriticalSuccess]: {
    [ImpactTypeEnum.Damage]: [
      "The <span class='highlight-skill'>{skill}</span> been resonating with the Dimensional Anomaly and been increased x2 - <span class='highlight-outcome'>Critical Success</span>! Takes <span class='highlight-damage'>{formattedSize}</span> devastating damage by <span class='highlight-violation'>{violation}</span>",
      "With perfect precision, the <span class='highlight-skill'>{skill}</span> strikes true - <span class='highlight-outcome'>Critical Success</span>! Takes <span class='highlight-damage'>{formattedSize}</span> devastating damage from <span class='highlight-violation'>{violation}</span>",
      "The attack resonates with incredible power - <span class='highlight-outcome'>Critical Success</span>! Suffers <span class='highlight-damage'>{formattedSize}</span> critical damage by <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Heal]: [
      "The healing energy surges with incredible power - <span class='highlight-outcome'>Critical Success</span>! Recovers <span class='highlight-heal'>{formattedSize}</span> health through <span class='highlight-violation'>{violation}</span>",
      "Divine intervention amplifies the healing - <span class='highlight-outcome'>Critical Success</span>! Is restored by <span class='highlight-heal'>{formattedSize}</span> health via <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Shield]: [
      "Exceptional success! Experiences <span class='highlight-damage'>{formattedSizeWithPrep}</span> <span class='highlight-violation'>{type}</span> effect from <span class='highlight-violation'>{violation}</span> - <span class='highlight-outcome'>Critical Success</span>"
    ],
    default: [
      "Exceptional success! Experiences <span class='highlight-damage'>{formattedSizeWithPrep}</span> <span class='highlight-violation'>{type}</span> effect from <span class='highlight-violation'>{violation}</span> - <span class='highlight-outcome'>Critical Success</span>"
    ]
  },
  [OutcomeEnum.GoodLuck]: {
    [ImpactTypeEnum.Damage]: [
      "Fortune favors the strike - <span class='highlight-outcome'>Good Luck</span>! Takes <span class='highlight-damage'>{formattedSize}</span> damage from <span class='highlight-violation'>{violation}</span>",
      "A lucky hit connects well - <span class='highlight-outcome'>Good Luck</span>! Suffers <span class='highlight-damage'>{formattedSize}</span> damage by <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Heal]: [
      "The healing flows smoothly - <span class='highlight-outcome'>Good Luck</span>! Recovers <span class='highlight-heal'>{formattedSize}</span> health through <span class='highlight-violation'>{violation}</span>"
    ],
    default: [
      "Things go better than expected - <span class='highlight-outcome'>Good Luck</span>! Receives <span class='highlight-damage'>{formattedSizeWithPrep}</span> <span class='highlight-violation'>{type}</span> effect from <span class='highlight-violation'>{violation}</span>"
    ]
  },
  [OutcomeEnum.BaseValue]: {
    [ImpactTypeEnum.Damage]: [
      "The <span class='highlight-skill'>{skill}</span> punched in face with <span class='highlight-damage'>{formattedSize}</span> damage by <span class='highlight-violation'>{violation}</span>",
      "A solid hit connects - takes <span class='highlight-damage'>{formattedSize}</span> damage from <span class='highlight-violation'>{violation}</span>",
      "The attack lands as expected, dealing <span class='highlight-damage'>{formattedSize}</span> damage via <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Heal]: [
      "The <span class='highlight-item'>{item}</span> healed for <span class='highlight-heal'>{formattedSize}</span> health by <span class='highlight-violation'>{violation}</span>",
      "Steady healing energy flows, restoring <span class='highlight-heal'>{formattedSize}</span> health through <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Shield]: [
      "The action succeeds normally, providing <span class='highlight-damage'>{formattedSizeWithPrep}</span> protection via <span class='highlight-violation'>{violation}</span>"
    ],
    default: [
      "The action succeeds normally, affecting with <span class='highlight-damage'>{formattedSizeWithPrep}</span> <span class='highlight-violation'>{type}</span> via <span class='highlight-violation'>{violation}</span>"
    ]
  },
  [OutcomeEnum.BadLuck]: {
    [ImpactTypeEnum.Damage]: [
      "While casting the initiator was distracted by the noise and the <span class='highlight-skill'>{skill}</span> missed but they were scratched for <span class='highlight-damage'>{formattedSize}</span> damage by <span class='highlight-violation'>{violation}</span>",
      "Bad timing affects the attack - <span class='highlight-outcome'>Bad Luck</span>! Only takes <span class='highlight-damage'>{formattedSize}</span> glancing damage from <span class='highlight-violation'>{violation}</span>",
      "The strike goes awry but still connects for <span class='highlight-damage'>{formattedSize}</span> damage via <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Heal]: [
      "The healing is disrupted but still provides <span class='highlight-heal'>{formattedSize}</span> health through <span class='highlight-violation'>{violation}</span>",
      "Despite complications, <span class='highlight-heal'>{formattedSize}</span> health is restored via <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Shield]: [
      "Things don't go as planned - <span class='highlight-outcome'>Bad Luck</span>! Still gains <span class='highlight-damage'>{formattedSizeWithPrep}</span> protection from <span class='highlight-violation'>{violation}</span>"
    ],
    default: [
      "Things don't go as planned - <span class='highlight-outcome'>Bad Luck</span>! Still receives <span class='highlight-damage'>{formattedSizeWithPrep}</span> <span class='highlight-violation'>{type}</span> from <span class='highlight-violation'>{violation}</span>"
    ]
  },
  [OutcomeEnum.CriticalFail]: {
    [ImpactTypeEnum.Damage]: [
      "While casting the initiator was distracted by the noise and the <span class='highlight-skill'>{skill}</span> missed and hit themselves for <span class='highlight-damage'>{formattedSize}</span> damage by <span class='highlight-violation'>{violation}</span>",
      "Disaster strikes! - <span class='highlight-outcome'>Critical Fail</span>! The attack backfires, causing <span class='highlight-damage'>{formattedSize}</span> damage to the initiator via <span class='highlight-violation'>{violation}</span>",
      "Complete failure! The action goes horribly wrong, resulting in <span class='highlight-damage'>{formattedSize}</span> self-inflicted damage from <span class='highlight-violation'>{violation}</span>"
    ],
    [ImpactTypeEnum.Heal]: [
      "The healing magic goes awry - <span class='highlight-outcome'>Critical Fail</span>! Instead of healing, <span class='highlight-damage'>{formattedSize}</span> damage is dealt via <span class='highlight-violation'>{violation}</span>",
      "Magical backlash occurs, causing <span class='highlight-damage'>{formattedSize}</span> damage instead of healing through <span class='highlight-violation'>{violation}</span>"
    ],
    default: [
      "Everything goes wrong - <span class='highlight-outcome'>Critical Fail</span>! The action backfires with <span class='highlight-damage'>{formattedSizeWithPrep}</span> <span class='highlight-violation'>{type}</span> effect from <span class='highlight-violation'>{violation}</span>"
    ]
  }
};

// Helper function to get random template from array
const getRandomTemplate = (templates: string[]): string => {
  return templates[Math.floor(Math.random() * templates.length)];
};

// Helper function to format size values
const formatSize = (size: number, type: string): string => {
  if (size === 0) {
    return '';
  }
  if (size < 0) {
    return `${Math.abs(size)} negative ${type}`;
  }
  return `${size} ${type}`;
};

// Helper function to format size with preposition
const formatSizeWithPreposition = (size: number, type: string): string => {
  if (size === 0) {
    return `no ${type}`;
  }
  if (size < 0) {
    return `${Math.abs(size)} negative ${type}`;
  }
  return `${size} ${type}`;
};

// Helper function to replace placeholders in template
const replacePlaceholders = (template: string, data: Record<string, any>): string => {
  return template.replace(/\{(\w+)\}/g, (match, key) => {
    return data[key] || match;
  });
};

// Generate action description (without character names - handled by components)
const getActionTemplate = (): string => {
  const actionType = props.action.action_type || 'unknown';
  const templates = actionTemplates[actionType] || actionTemplates.default;

  const hasSkill = props.action.skill && props.action.skill.name;

  let template: string;

  if (!hasTargets.value) {
    template = templates.noTarget || templates.base;
  } else if (isSelfTargeting.value) {
    template = templates.self || templates.base;
  } else if (actionType === ActionType5f8Enum.UseSkill && !hasSkill) {
    template = templates.noSkill || templates.base;
  } else {
    template = templates.base;
  }

  const data = {
    skill: hasSkill ? props.action.skill.name : t('actionLog.unknownSkill'),
    item: t('actionLog.unknownItem'), // This would need to be passed from action data
    actionType: t(`actionLog.actionTypes.${actionType}`) || actionType.replace(/([A-Z])/g, ' $1').trim()
  };

  return replacePlaceholders(template, data);
};

// Generate outcome description for each impact (without character names)
const getOutcomeTemplate = (impact: any): string => {
  const outcome = impact.dice_roll_result?.outcome;
  const impactType = impact.type;

  // Use general outcome templates
  const outcomeGroup = outcomeTemplates[outcome];
  if (!outcomeGroup) return t('actionLog.unknownOutcome', { outcome });

  const templates = outcomeGroup[impactType] || outcomeGroup.default;
  if (!templates) return t('actionLog.noTemplate', { outcome, impactType });

  const template = getRandomTemplate(templates);

  const size = impact.size || 0;

  // Get localized type text, fallback to raw impact type if localization fails
  const localizedType = t(`actionLog.impactTypes.${impactType}`);
  const typeText = (localizedType && !localizedType.startsWith('actionLog.'))
    ? localizedType
    : (impactType?.toLowerCase() || 'effect');

  // Get localized violation text, fallback to raw violation type if localization fails
  const localizedViolation = t(`actionLog.violationTypes.${impact.violation}`);
  const violationText = (localizedViolation && !localizedViolation.startsWith('actionLog.'))
    ? localizedViolation
    : (impact.violation || 'unknown');

  const data = {
    size: size,
    formattedSize: formatSize(size, 'damage'),
    formattedSizeWithPrep: formatSizeWithPreposition(size, typeText),
    type: typeText,
    violation: violationText,
    skill: props.action.skill?.name || t('actionLog.unknownSkill'),
    item: t('actionLog.unknownItem') // This would need to be passed from action data
  };

  return replacePlaceholders(template, data);
};
</script>

<style scoped>
.action-log-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.2rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1c1c1c;
  font-size: 0.68rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.cycle-info {
  padding: 0.25rem 0.5rem;
  background: #2a2a2a;
  border-bottom: 1px solid #444;
  font-size: 0.6rem;
  color: #888;
  font-weight: bold;
}

.action-section {
  padding: 0.5rem;
  display: flex;
  align-items: center;
  min-height: 4vh;
  flex-direction: row;
}

.action-text {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-wrap: wrap;
  font-size: 0.68rem;
  color: #e0e0e0;
  line-height: 1.3;
}

.outcomes-section {
  padding: 0.5rem;
  line-height: 1.5;
}

.outcome-text {
  display: inline;
  font-size: 0.65rem;
  color: #c0c0c0;
  line-height: 1.5;
}

.outcome-text:not(:last-child)::after {
  content: " ";
  display: inline;
}

/* Character name styling from CharacterInlineDetails */
.highlight-initiator {
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-shadow: 1px 1px 2px #000;
  font-weight: bold;
}

.highlight-target {
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-shadow: 1px 1px 2px #000;
  font-weight: bold;
}

.highlight-skill {
  color: #4a9eff;
  font-weight: bold;
  text-shadow: 0 0 3px rgba(74, 158, 255, 0.3);
}

.highlight-item {
  color: #9C27B0;
  font-weight: bold;
  text-shadow: 0 0 3px rgba(156, 39, 176, 0.3);
}

.highlight-damage {
  color: #ff4444;
  font-weight: bold;
  font-size: 1.1em;
  text-shadow: 0 0 3px rgba(255, 68, 68, 0.4);
}

.highlight-heal {
  color: #44ff44;
  font-weight: bold;
  font-size: 1.1em;
  text-shadow: 0 0 3px rgba(68, 255, 68, 0.4);
}

.highlight-violation {
  color: #ff6b9d;
  font-weight: bold;
  text-transform: capitalize;
  text-shadow: 0 0 3px rgba(255, 107, 157, 0.3);
}

.highlight-outcome {
  color: #ffd700;
  font-weight: bold;
  text-transform: uppercase;
  text-shadow: 0 0 3px rgba(255, 215, 0, 0.4);
}

/* Responsive design */
@media (max-width: 768px) {
  .action-log-item {
    font-size: 0.6rem;
  }

  .action-text {
    font-size: 0.6rem;
  }

  .outcome-text {
    font-size: 0.58rem;
  }

  .cycle-info {
    font-size: 0.55rem;
  }
}
</style>