<template>
  <div class="skill-icon-inline">
    <img v-if="icon" :src="icon" alt="Skill Icon" :title="name" class="skill-icon"/>
    <img v-else alt="Default Skill Icon" class="skill-icon" src="@/assets/images/skill/default.webp"/>
    <span class="skill-name">{{ name }}</span>
  </div>
</template>

<script>
export default {
  name: "ActionIconMini",
  props: {
    skill: {
      type: Object,
      required: true,
    },
  },
  computed: {
    name() {
      return this.skill.name || "Unnamed";
    },
    icon() {
      return this.skill.icon || null;
    },
  },
};
</script>

<style scoped>
.skill-icon-inline {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* Space between icon and text */
  font-family: "Roboto", sans-serif;
  color: #ffffff;
  white-space: nowrap; /* Prevent text wrapping */
  overflow: hidden;
}

.skill-icon {
  width: 2em; /* Icon size proportional to font size */
  height: 2em;
  object-fit: contain;
  border-radius: 0.2em; /* Optional: Rounded corners */
}

.skill-name {
  text-transform: uppercase;
  font-weight: bold;
  font-size: 0.8em; /* Match font size to icon size */
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.5); /* Subtle text shadow */
  max-width: 8em; /* Limit max width to prevent overflow */
  overflow: hidden;
  text-overflow: ellipsis; /* Ellipsis for overflow text */

}
</style>
