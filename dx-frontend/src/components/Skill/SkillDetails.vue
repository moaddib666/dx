<template>
  <div class="skill-inspector">
    <!-- Icon and Section -->
    <SkillIcon :skill="skill" class="skill-icon" :title="skill.description"/>

    <div class="info-holder">
      <!-- Impact Section -->
      <span>Impacts:</span>
      <div class="impacts">
        <div
            v-for="violation in violationService.listCachedViolations()"
            :key="violation.id"
        >
          <ResponsiveMiniIcon
              :title="violation.id"
              :alt-text="violation.id"
              :image-url="violation.icon"
              :is-disabled="!hasViolation(violation.id)"
          />
        </div>
      </div>
      <span>Requires:</span>
      <div class="requires">
        <div v-for="stat in statsService.listCachedStats()" :key="stat.id">
          <ResponsiveMiniIcon
              :title="stat.id"
              :altText="stat.id"
              :imageUrl="stat.icon"
              :is-disabled="getStatValue(stat.id) <= 0"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SkillIcon from "@/components/Action/ActionIcon.vue";
import StatsGameService from "@/services/statService.js";
import ViolationsGameService from "@/services/violationService.js";
import ResponsiveMiniIcon from "@/components/icons/ResponsiveMiniIcon.vue";

export default {
  name: "SkillInspector",
  components: {
    ResponsiveMiniIcon,
    SkillIcon,
  },
  props: {
    skill: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      statsService: StatsGameService,
      violationService: ViolationsGameService,
      requiresMap: {},
      violationMap: {},
    };
  },
  methods: {
    getStatValue(stat) {
      return this.requiresMap[stat] || 0;
    },
    hasViolation(violation) {
      return this.violationMap[violation] || false;
    },
  },
  watch: {
    skill: {
      handler(newSkill) {
        // Reset the maps
        this.requiresMap = {};
        this.violationMap = {};

        if (!newSkill.impact) return;

        for (const impact of newSkill.impact) {
          // Ensure impact.formula.requires is defined
          this.violationMap[impact.type] = true;
          if (impact.formula?.requires) {
            for (const requirement of impact.formula.requires) {
              if (requirement.stat) {
                this.requiresMap[requirement.stat] =
                    (this.requiresMap[requirement.stat] || 0) + requirement.value;
              }
            }
          }
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.skill-icon {
  margin: 1rem;
}
.skill-inspector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(43, 43, 43, 0.8);
  border-radius: 0.5rem;
  color: white;
  font-family: "Roboto", sans-serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  gap: 1rem;
  margin: auto;
  font-size: 0.7rem;
}
.info-holder {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
}
.impacts,
.requires {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.2rem;
}
</style>
