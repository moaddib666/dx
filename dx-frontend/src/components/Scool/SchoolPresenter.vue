<template>
  <div class="details-section">
    <div v-if="school" class="details-container">
      <!-- Selected School Header -->
      <div class="selected-school">
        <div class="header">
          <h3>{{ school.name }}</h3>
          <div v-if="!isLearned(school.id) && canLearnSchool" class="learn-school-button">
            <button @click="learnSchool(school.id)">Learn</button>
          </div>
          <responsive-mini-icon :image-url="school.icon" :title="school.name" alt="School Icon"
                                :alt-text="school.name"/>
        </div>
        <p>{{ school.description }}</p>

      </div>

      <!-- Skills Section -->
      <div class="skills-section">
          <div
              v-for="skill in getSkillsForSchool(school.id)"
              :key="skill.id"
              :class="['skill-item', { learned: isSkillLearned(skill.id) }]"
              @click="selectSkill(skill)"
          >
            <SkillDetails :skill="skill"/>
          </div>
      </div>

      <!-- Learn Button -->

    </div>

    <!-- Placeholder for no selection -->
    <div v-else class="placeholder">
      <p>Select a school to view details.</p>
    </div>
  </div>
</template>

<script>
import SkillDetails from "@/components/Skill/SkillDetails.vue";
import ResponsiveMiniIcon from "@/components/icons/ResponsiveMiniIcon.vue";

export default {
  name: "SchoolPresenter",
  components: {ResponsiveMiniIcon, SkillDetails},
  props: {
    school: {
      type: Object,
      default: null,
    },
    skills: {
      type: Array,
      required: true,
    },
    learnedSchools: {
      type: Array,
      required: true,
    },
    activeSlots: {
      type: Number,
      required: true,
    },
  },
  computed: {
    canLearnSchool() {
      return this.learnedSchools.length < this.activeSlots;
    },
  },
  methods: {
    isLearned(schoolId) {
      return this.learnedSchools.some((school) => school.school === schoolId);
    },
    getSkillsForSchool(schoolId) {
      return this.skills
          .filter((skill) => skill.skill.school === schoolId)
          .map((skill) => skill.skill);
    },
    isSkillLearned(skillId) {
      return this.skills.some((skill) => skill.skill.id === skillId);
    },
    learnSchool(schoolId) {
      this.$emit("learn-school", schoolId);
    },
    selectSkill(skill) {
      this.$emit("skill-selected", skill);
    },
  },
};
</script>

<style scoped>
.details-section {
  flex: 1;
  padding: 1em;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  background: rgba(20, 20, 20, 0.95);
  border-radius: 0 0.5rem 0.5rem 0;
}

.details-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 1rem;
}



.selected-school {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  flex: 1;
  width: 100%;
  font-size: 1.5em;
}

.selected-school p {
  margin: 0;
  color: rgba(200, 200, 200, 0.9);
  font-size: 0.8em;
}

.selected-school .header {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  align-items: center;
}

.selected-school h3 {
  margin: 0;
  font-size: 1.2rem;
}

.selected-school p {
  margin: 0.5rem 0 0;
  color: rgba(200, 200, 200, 0.9);
}

.skills-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 0.5em;
  max-height: 60vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) rgba(0, 0, 0, 0.5);
}


.skill-item {
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  margin: auto;
}

.skill-item.learned {
  border-left: 1em solid #00ff00;
}

.learn-school-button {
  text-align: center;
}

.learn-school-button button {
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.learn-school-button button:hover {
  background: #0056b3;
}

.placeholder {
  text-align: center;
  color: rgba(200, 200, 200, 0.8);
}
</style>
