<template>
  <div class="skill compact">
    <div class="skill-icon">
      <img :src="skill.icon || placeholder" alt="Skill Icon"/>
    </div>
    <div class="skill-details">
      <span class="skill-name">{{ skill.name }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkillComponent',
  props: {
    skill: Object,
  },
  data() {
    return {
      placeholder: 'https://via.placeholder.com/24',
    };
  },
};
</script>

<style scoped>
.skill.compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1c1c1c;
}

.skill-icon img {
  width: 20px;
  height: 20px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid #555;
}

.skill-details {
  display: flex;
  flex-direction: column;
}

.skill-name {
  font-weight: bold;
  color: #e0e0e0;
  font-size: 0.85rem;
}
</style>
