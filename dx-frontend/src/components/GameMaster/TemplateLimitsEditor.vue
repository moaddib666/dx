<template>
  <div class="template-limits-editor">
    <div class="limits-form">
      <!-- Stats Points Limit -->
      <div class="limit-group">
        <label for="max-stats-points">Maximum Stats Points</label>
        <input
          id="max-stats-points"
          type="number"
          min="1"
          max="1000"
          :value="validation.max_stats_points_count"
          @input="updateLimit('max_stats_points_count', $event.target.value)"
          class="limit-input"
        />
        <div class="limit-description">
          Total points that can be distributed across all character stats
        </div>
        <div class="current-usage">
          Current usage: {{ currentStatsPoints }} / {{ validation.max_stats_points_count }}
          <span :class="{ 'over-limit': currentStatsPoints > validation.max_stats_points_count }">
            {{ currentStatsPoints > validation.max_stats_points_count ? '(Over Limit!)' : '' }}
          </span>
        </div>
      </div>

      <!-- Schools Limit -->
      <div class="limit-group">
        <label for="max-schools">Maximum Non-Base Schools</label>
        <input
          id="max-schools"
          type="number"
          min="0"
          max="50"
          :value="validation.max_schools_count"
          @input="updateLimit('max_schools_count', $event.target.value)"
          class="limit-input"
        />
        <div class="limit-description">
          Maximum number of non-base schools that can be learned (base schools are always included)
        </div>
        <div class="current-usage">
          Current non-base schools: {{ currentNonBaseSchools }} / {{ validation.max_schools_count }}
          <span :class="{ 'over-limit': currentNonBaseSchools > validation.max_schools_count }">
            {{ currentNonBaseSchools > validation.max_schools_count ? '(Over Limit!)' : '' }}
          </span>
        </div>
      </div>

      <!-- Spells Limit -->
      <div class="limit-group">
        <label for="max-spells">Maximum Non-Base Spells</label>
        <input
          id="max-spells"
          type="number"
          min="0"
          max="100"
          :value="validation.max_spells_count"
          @input="updateLimit('max_spells_count', $event.target.value)"
          class="limit-input"
        />
        <div class="limit-description">
          Maximum number of non-base spells that can be learned (base spells are always included)
        </div>
        <div class="current-usage">
          Current non-base spells: {{ currentNonBaseSpells }} / {{ validation.max_spells_count }}
          <span :class="{ 'over-limit': currentNonBaseSpells > validation.max_spells_count }">
            {{ currentNonBaseSpells > validation.max_spells_count ? '(Over Limit!)' : '' }}
          </span>
        </div>
      </div>

      <!-- Items Limit -->
      <div class="limit-group">
        <label for="max-items">Maximum Items</label>
        <input
          id="max-items"
          type="number"
          min="0"
          max="100"
          :value="validation.max_items_count"
          @input="updateLimit('max_items_count', $event.target.value)"
          class="limit-input"
        />
        <div class="limit-description">
          Maximum number of items that can be carried in inventory
        </div>
        <div class="current-usage">
          Current items: {{ currentItems }} / {{ validation.max_items_count }}
          <span :class="{ 'over-limit': currentItems > validation.max_items_count }">
            {{ currentItems > validation.max_items_count ? '(Over Limit!)' : '' }}
          </span>
        </div>
      </div>

      <!-- Modificators Limit -->
      <div class="limit-group">
        <label for="max-modificators">Maximum Modificators</label>
        <input
          id="max-modificators"
          type="number"
          min="0"
          max="50"
          :value="validation.max_modificators_count"
          @input="updateLimit('max_modificators_count', $event.target.value)"
          class="limit-input"
        />
        <div class="limit-description">
          Maximum number of modificators that can be applied to the character
        </div>
        <div class="current-usage">
          Current modificators: {{ currentModificators }} / {{ validation.max_modificators_count }}
          <span :class="{ 'over-limit': currentModificators > validation.max_modificators_count }">
            {{ currentModificators > validation.max_modificators_count ? '(Over Limit!)' : '' }}
          </span>
        </div>
      </div>

      <!-- Rank Limit -->
      <div class="limit-group">
        <label for="max-rank">Maximum Rank Grade</label>
        <input
          id="max-rank"
          type="number"
          min="0"
          max="10"
          :value="validation.max_rank_grade"
          @input="updateLimit('max_rank_grade', $event.target.value)"
          class="limit-input"
        />
        <div class="limit-description">
          Maximum rank grade that can be assigned (0 = highest, 10 = lowest)
        </div>
        <div class="current-usage">
          Current rank: {{ currentRank }} / {{ validation.max_rank_grade }}
          <span :class="{ 'over-limit': currentRank > validation.max_rank_grade }">
            {{ currentRank > validation.max_rank_grade ? '(Over Limit!)' : '' }}
          </span>
        </div>
      </div>

      <!-- Presets Section -->
      <div class="presets-section">
        <h3>Limit Presets</h3>
        <div class="presets-buttons">
          <button @click="applyPreset('beginner')" class="preset-btn">Beginner</button>
          <button @click="applyPreset('intermediate')" class="preset-btn">Intermediate</button>
          <button @click="applyPreset('advanced')" class="preset-btn">Advanced</button>
          <button @click="applyPreset('expert')" class="preset-btn">Expert</button>
          <button @click="applyPreset('unlimited')" class="preset-btn preset-unlimited">Unlimited</button>
        </div>
        <div class="preset-description">
          {{ getPresetDescription() }}
        </div>
      </div>

      <!-- Reset Section -->
      <div class="reset-section">
        <button @click="resetToDefaults" class="reset-btn">Reset to Defaults</button>
        <div class="reset-description">
          Reset all limits to their default values
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import skillService from '@/services/skillService.js';

export default {
  name: 'TemplateLimitsEditor',
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      skillService: skillService
    };
  },
  computed: {
    validation() {
      return this.template.validation || {};
    },
    currentStatsPoints() {
      return this.template.data.stats.reduce((sum, stat) => sum + stat.value, 0);
    },
    currentNonBaseSchools() {
      return this.skillService.getNonBaseSchoolIds(this.template.data.schools).length;
    },
    currentNonBaseSpells() {
      return this.skillService.getNonBaseSpellIds(this.template.data.spells).length;
    },
    currentItems() {
      return this.template.data.items.length;
    },
    currentModificators() {
      return this.template.data.modificators.length;
    },
    currentRank() {
      return this.template.data.rank;
    }
  },
  methods: {
    updateLimit(limitName, value) {
      const numValue = parseInt(value, 10);
      if (!isNaN(numValue) && numValue >= 0) {
        const newValidation = { ...this.validation };
        newValidation[limitName] = numValue;
        this.service.setValidation(newValidation);
      }
    },

    applyPreset(presetName) {
      const presets = {
        beginner: {
          max_stats_points_count: 50,
          max_schools_count: 2,
          max_spells_count: 5,
          max_items_count: 10,
          max_modificators_count: 3,
          max_rank_grade: 8
        },
        intermediate: {
          max_stats_points_count: 75,
          max_schools_count: 3,
          max_spells_count: 10,
          max_items_count: 15,
          max_modificators_count: 5,
          max_rank_grade: 6
        },
        advanced: {
          max_stats_points_count: 100,
          max_schools_count: 5,
          max_spells_count: 15,
          max_items_count: 20,
          max_modificators_count: 8,
          max_rank_grade: 4
        },
        expert: {
          max_stats_points_count: 150,
          max_schools_count: 8,
          max_spells_count: 25,
          max_items_count: 30,
          max_modificators_count: 12,
          max_rank_grade: 2
        },
        unlimited: {
          max_stats_points_count: 1000,
          max_schools_count: 50,
          max_spells_count: 100,
          max_items_count: 100,
          max_modificators_count: 50,
          max_rank_grade: 0
        }
      };

      const preset = presets[presetName];
      if (preset) {
        this.service.setValidation(preset);
      }
    },

    resetToDefaults() {
      const defaults = {
        max_stats_points_count: 100,
        max_schools_count: 5,
        max_spells_count: 15,
        max_items_count: 20,
        max_modificators_count: 8,
        max_rank_grade: 5
      };
      this.service.setValidation(defaults);
    },

    getPresetDescription() {
      const descriptions = {
        beginner: 'Low limits suitable for new characters or restricted campaigns',
        intermediate: 'Moderate limits for balanced gameplay',
        advanced: 'Higher limits for experienced characters',
        expert: 'Very high limits for veteran characters',
        unlimited: 'No practical limits - use with caution'
      };
      
      // Try to detect which preset is currently active
      const current = this.validation;
      for (const [presetName, description] of Object.entries(descriptions)) {
        // This is a simplified detection - you might want to make it more sophisticated
        if (presetName === 'beginner' && current.max_stats_points_count <= 50) {
          return description;
        }
      }
      
      return 'Custom limits configuration';
    }
  }
};
</script>

<style scoped>
.template-limits-editor {
  padding: 20px;
  background: #1e1e1e;
  color: #ffffff;
  font-family: 'Roboto', sans-serif;
}

.limits-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.limit-group {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #444;
}

.limit-group label {
  display: block;
  font-weight: bold;
  color: #1E90FF;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.limit-input {
  width: 100%;
  max-width: 200px;
  padding: 8px 12px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.limit-input:focus {
  border-color: #1E90FF;
  outline: none;
}

.limit-description {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #ccc;
  line-height: 1.4;
}

.current-usage {
  margin-top: 0.75rem;
  padding: 8px 12px;
  background: rgba(30, 144, 255, 0.1);
  border-radius: 4px;
  font-size: 0.9rem;
  color: #fff;
  border-left: 3px solid #1E90FF;
}

.over-limit {
  color: #ff6b6b;
  font-weight: bold;
}

.presets-section {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #444;
}

.presets-section h3 {
  color: #1E90FF;
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
}

.presets-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.preset-btn {
  padding: 8px 16px;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.preset-btn:hover {
  background: #555;
  transform: translateY(-1px);
}

.preset-unlimited {
  background: #ff6b6b;
}

.preset-unlimited:hover {
  background: #ff5252;
}

.preset-description {
  font-size: 0.9rem;
  color: #ccc;
  font-style: italic;
}

.reset-section {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #444;
  text-align: center;
}

.reset-btn {
  padding: 10px 20px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
}

.reset-btn:hover {
  background: #d32f2f;
  transform: translateY(-1px);
}

.reset-description {
  font-size: 0.9rem;
  color: #ccc;
}

/* Responsive design */
@media (max-width: 768px) {
  .presets-buttons {
    flex-direction: column;
  }
  
  .preset-btn {
    width: 100%;
  }
  
  .limit-input {
    max-width: 100%;
  }
}
</style>