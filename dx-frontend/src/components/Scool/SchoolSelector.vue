<template>
  <div class="schools-column">
    <ResponsiveMiniIcon
        v-for="school in schools"
        :key="school.id"
        :title="school.name"
        @click="selectSchool(school)"
        :alt-text="school.name"
        :is-disabled="isDisabled(school.id)"
        :is-active="isLearned(school.id)"
        :is-selected="school.id === selectedSchoolId"
        :image-url="school.icon"/>
  </div>
</template>

<script>
import ResponsiveMiniIcon from "@/components/icons/ResponsiveMiniIcon.vue";

export default {
  name: "SchoolSelector",
  components: {ResponsiveMiniIcon},
  props: {
    schools: {
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
    selectedSchoolId: {
      type: String,
      default: null,
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
    isDisabled(schoolId) {
      return !this.canLearnSchool && !this.isLearned(schoolId);
    },
    selectSchool(school) {
      if (!this.isDisabled(school.id)) {
        this.$emit("school-selected", school);
      }
    },
  },
};
</script>

<style scoped>
.schools-column {
  display: flex;
  flex-direction: column; /* Upside-down arrangement */
  align-items: flex-start;
  justify-content: center;
  background: rgba(30, 30, 30, 0.9);
  border-radius: 0.5rem 0 0 0.5rem;
  padding: 0.5rem;
  gap: 0.5rem;
}

.schools-column > * {
  cursor: pointer;
}

</style>
