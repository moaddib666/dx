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

// Template keys for different action types (to be translated)
const actionTemplateKeys = {
  [ActionType5f8Enum.UseSkill]: {
    base: "actionLog.templates.useSkill.base",
    noTarget: "actionLog.templates.useSkill.noTarget",
    noSkill: "actionLog.templates.useSkill.noSkill",
    self: "actionLog.templates.useSkill.self"
  },
  [ActionType5f8Enum.UseItem]: {
    base: "actionLog.templates.useItem.base",
    noTarget: "actionLog.templates.useItem.noTarget",
    self: "actionLog.templates.useItem.self"
  },
  [ActionType5f8Enum.SnatchItem]: {
    base: "actionLog.templates.snatchItem.base",
    noTarget: "actionLog.templates.snatchItem.noTarget",
    self: "actionLog.templates.snatchItem.self"
  },
  [ActionType5f8Enum.Move]: {
    base: "actionLog.templates.move.base",
    noTarget: "actionLog.templates.move.noTarget",
    self: "actionLog.templates.move.self"
  },
  [ActionType5f8Enum.DiceRoll]: {
    base: "actionLog.templates.diceRoll.base",
    noTarget: "actionLog.templates.diceRoll.noTarget",
    self: "actionLog.templates.diceRoll.self"
  },
  [ActionType5f8Enum.Inspect]: {
    base: "actionLog.templates.inspect.base",
    noTarget: "actionLog.templates.inspect.noTarget",
    self: "actionLog.templates.inspect.self"
  },
  [ActionType5f8Enum.Gift]: {
    base: "actionLog.templates.gift.base",
    noTarget: "actionLog.templates.gift.noTarget",
    self: "actionLog.templates.gift.self"
  },
  default: {
    base: "actionLog.templates.default.base",
    noTarget: "actionLog.templates.default.noTarget",
    self: "actionLog.templates.default.self"
  }
};

// Outcome template keys for different outcomes and impact types
const outcomeTemplateKeys = {
  [OutcomeEnum.CriticalSuccess]: {
    [ImpactTypeEnum.Damage]: [
      "actionLog.outcomes.criticalSuccess.damage.1",
      "actionLog.outcomes.criticalSuccess.damage.2",
      "actionLog.outcomes.criticalSuccess.damage.3"
    ],
    [ImpactTypeEnum.Heal]: [
      "actionLog.outcomes.criticalSuccess.heal.1",
      "actionLog.outcomes.criticalSuccess.heal.2"
    ],
    [ImpactTypeEnum.Shield]: [
      "actionLog.outcomes.criticalSuccess.shield.1"
    ],
    default: [
      "actionLog.outcomes.criticalSuccess.default.1"
    ]
  },
  [OutcomeEnum.GoodLuck]: {
    [ImpactTypeEnum.Damage]: [
      "actionLog.outcomes.goodLuck.damage.1",
      "actionLog.outcomes.goodLuck.damage.2"
    ],
    [ImpactTypeEnum.Heal]: [
      "actionLog.outcomes.goodLuck.heal.1"
    ],
    default: [
      "actionLog.outcomes.goodLuck.default.1"
    ]
  },
  [OutcomeEnum.BaseValue]: {
    [ImpactTypeEnum.Damage]: [
      "actionLog.outcomes.baseValue.damage.1",
      "actionLog.outcomes.baseValue.damage.2",
      "actionLog.outcomes.baseValue.damage.3"
    ],
    [ImpactTypeEnum.Heal]: [
      "actionLog.outcomes.baseValue.heal.1",
      "actionLog.outcomes.baseValue.heal.2"
    ],
    [ImpactTypeEnum.Shield]: [
      "actionLog.outcomes.baseValue.shield.1"
    ],
    default: [
      "actionLog.outcomes.baseValue.default.1"
    ]
  },
  [OutcomeEnum.BadLuck]: {
    [ImpactTypeEnum.Damage]: [
      "actionLog.outcomes.badLuck.damage.1",
      "actionLog.outcomes.badLuck.damage.2",
      "actionLog.outcomes.badLuck.damage.3"
    ],
    [ImpactTypeEnum.Heal]: [
      "actionLog.outcomes.badLuck.heal.1",
      "actionLog.outcomes.badLuck.heal.2"
    ],
    [ImpactTypeEnum.Shield]: [
      "actionLog.outcomes.badLuck.shield.1"
    ],
    default: [
      "actionLog.outcomes.badLuck.default.1"
    ]
  },
  [OutcomeEnum.CriticalFail]: {
    [ImpactTypeEnum.Damage]: [
      "actionLog.outcomes.criticalFail.damage.1",
      "actionLog.outcomes.criticalFail.damage.2",
      "actionLog.outcomes.criticalFail.damage.3"
    ],
    [ImpactTypeEnum.Heal]: [
      "actionLog.outcomes.criticalFail.heal.1",
      "actionLog.outcomes.criticalFail.heal.2"
    ],
    default: [
      "actionLog.outcomes.criticalFail.default.1"
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
  const templateKeys = actionTemplateKeys[actionType] || actionTemplateKeys.default;

  const hasSkill = props.action.skill && props.action.skill.name;

  let templateKey: string;

  if (!hasTargets.value) {
    templateKey = templateKeys.noTarget || templateKeys.base;
  } else if (isSelfTargeting.value) {
    templateKey = templateKeys.self || templateKeys.base;
  } else if (actionType === ActionType5f8Enum.UseSkill && !hasSkill) {
    templateKey = templateKeys.noSkill || templateKeys.base;
  } else {
    templateKey = templateKeys.base;
  }

  const data = {
    skill: hasSkill ? `<span class="highlight-skill">${props.action.skill.name}</span>` : `<span class="highlight-skill">${t('actionLog.unknownSkill')}</span>`,
    item: `<span class="highlight-item">${t('actionLog.unknownItem')}</span>`, // This would need to be passed from action data
    actionType: `<span class="highlight-skill">${t(`actionLog.actionTypes.${actionType}`) || actionType.replace(/([A-Z])/g, ' $1').trim()}</span>`,
    target: `<span class="highlight-target">${t('actionLog.self')}</span>`
  };

  const template = t(templateKey, data);
  return template;
};

// Generate outcome description for each impact (without character names)
const getOutcomeTemplate = (impact: any): string => {
  const outcome = impact.dice_roll_result?.outcome;
  const impactType = impact.type;

  // Use general outcome template keys
  const outcomeGroup = outcomeTemplateKeys[outcome];
  if (!outcomeGroup) return t('actionLog.unknownOutcome', { outcome });

  const templateKeys = outcomeGroup[impactType] || outcomeGroup.default;
  if (!templateKeys) return t('actionLog.noTemplate', { outcome, impactType });

  const templateKey = getRandomTemplate(templateKeys);

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
    formattedSize: `<span class="highlight-${impactType === ImpactTypeEnum.Heal ? 'heal' : 'damage'}">${formatSize(size, typeText)}</span>`,
    formattedSizeWithPrep: `<span class="highlight-${impactType === ImpactTypeEnum.Heal ? 'heal' : 'damage'}">${formatSizeWithPreposition(size, typeText)}</span>`,
    type: `<span class="highlight-violation">${typeText}</span>`,
    violation: `<span class="highlight-violation">${violationText}</span>`,
    skill: `<span class="highlight-skill">${props.action.skill?.name || t('actionLog.unknownSkill')}</span>`,
    item: `<span class="highlight-item">${t('actionLog.unknownItem')}</span>`, // This would need to be passed from action data
    outcome: `<span class="highlight-outcome">${t(`actionLog.outcomes.${outcome}`)}</span>`
  };

  return t(templateKey, data);
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