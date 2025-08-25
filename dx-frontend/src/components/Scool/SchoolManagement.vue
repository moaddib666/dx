<template>
  <div class="school-management">
    <!-- School GmCharSelector -->
    <SchoolSelector
        :schools="schools"
        :learnedSchools="learnedSchools"
        :activeSlots="activeSlots"
        :selectedSchoolId="selectedSchool?.id"
        @school-selected="handleSchoolSelection"
    />

    <!-- School Presenter -->
    <SchoolPresenter
        :school="selectedSchool"
        :skills="skills"
        :learnedSchools="learnedSchools"
        :activeSlots="activeSlots"
        @learn-school="learnSchool"
        @skill-selected="selectSkill"
    />
  </div>
</template>

<script>

import SchoolSelector from "@/components/Scool/SchoolSelector.vue";
import SchoolPresenter from "@/components/Scool/SchoolPresenter.vue";

export default {
  name: "SchoolManagement",
  components: {
    SchoolSelector,
    SchoolPresenter,
  },
  props: {
    schools: {
      type: Array,
      required: true,
    },
    learnedSchools: {
      type: Array,
      required: true,
    },
    skills: {
      type: Array,
      required: true,
    },
    activeSlots: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      selectedSchool: null,
    };
  },
  methods: {
    handleSchoolSelection(school) {
      this.selectedSchool = school;
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
.school-management {
  display: flex;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 0.5rem;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}
</style>
