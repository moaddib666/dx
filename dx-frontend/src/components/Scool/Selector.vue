<script>

import {SchoolGameApi} from "@/api/backendService.js";

export default {
  name: "SchoolSelector",
  props: {
    path: {
      type: String,
      required: true
    },
    selected: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      schools: []
    }
  },
  created() {
    this.loadSchools();
  },
  methods: {
    async loadSchools() {
      const importSchools = await SchoolGameApi.schoolSchoolsGetAllSchoolsRetrieve(
          {
            params: {
              path: this.path
            }
          },
      )
    }
  },
}
</script>

<template>


</template>

<style scoped>

</style>