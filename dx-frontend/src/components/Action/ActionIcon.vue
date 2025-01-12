<template>
  <div :class="typeClass" class="skill-holder">
    <div class="required-stats">
      <div v-if="costByKind('Action Points')" :title="'Action Points Cost: ' + costByKind('Action Points').value"
           class="cost ap-cost">
        <span>{{ costByKind('Action Points').value }}</span>
      </div>
      <div v-if="costByKind('Energy')" :title="'Energy Cost: ' + costByKind('Energy').value" class="cost energy-cost">
        <span>{{ costByKind('Energy').value }}</span>
      </div>
      <div v-if="costByKind('Health')" :title="'Health Cost: ' + costByKind('Health').value" class="cost health-cost">
        <span>{{ costByKind('Health').value }}</span>
      </div>
    </div>
    <div class="skill-type">
      <i :class="'type-icon ' + typeIcon" :title="type"></i>
    </div>
    <div class="icon">
      <img v-if="icon" :src="icon" alt="Skill Icon"/>
      <slot v-else-if="useSlotIcon"/>
      <img v-else alt="Skill Icon" src="@/assets/images/skill/default.webp"/>
    </div>
    <div class="skill-name">
      <span>{{ name }}</span>
    </div>
  </div>
</template>
<script>
export default {
  name: "SkillIcon",
  props: {
    fade: {
      type: Boolean,
      default: false
    },
    skill: {
      type: Object,
      required: true
    },
    useSlotIcon: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    name() {
      return this.skill.name || "Unnamed Skill";
    },
    type() {
      return this.skill.type || "utility";
    },
    icon() {
      return this.skill.icon || null;
    },
    typeClass() {
      return `skill-${this.type}` + (this.fade ? " fade" : "");
    },
    typeIcon() {
      const icons = {
        attack: "⚔️",
        defense: "🛡️",
        heal: "❤️",
        buff: "✨",
        debuff: "💀",
        utility: "🔧",
        special: "🌟"
      };
      return icons[this.type] || "🔧";
    }
  },
  methods: {
    costByKind(kind) {
      return this.skill.cost?.find((cost) => cost.kind === kind) || null;
    }
  }
};
</script>
<style scoped>
.skill-holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  width: 5rem;
  height: 5rem;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border-radius: 0.2rem;
  cursor: pointer;
  position: relative;
  color: white;
  padding: 0.2rem;
  font-family: "Orbitron", sans-serif;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.skill-holder:hover {
  transform: scale(1.05);
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
}

/* Dynamic Skill Type Colors */
.skill-attack {
  border: 2px solid #ff1744;
  box-shadow: 0 0 5px #ff1744;
}

.skill-defense {
  border: 2px solid #00e5ff;
  box-shadow: 0 0 5px #00e5ff;
}

.skill-heal {
  border: 2px solid #00ff00;
  box-shadow: 0 0 5px #00ff00;
}

.skill-buff {
  border: 2px solid #ffc107;
  box-shadow: 0 0 5px #ffc107;
}

.skill-debuff {
  border: 2px solid #b71c1c;
  box-shadow: 0 0 5px #b71c1c;
}

.skill-utility {
  border: 2px solid #9e9e9e;
  box-shadow: 0 0 5px #9e9e9e;
}

.skill-special {
  border: 2px solid #673ab7;
  box-shadow: 0 0 5px #673ab7;
}

.required-stats {
  z-index: 2;
  display: flex;
  flex-direction: row;
  font-size: 0.8rem;
  gap: 0.1rem;
}

/* Cost Icons */
.cost {
  width: 1.5rem; /* Smaller size */
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem; /* Smaller text */
  font-weight: bold;
}

.energy-cost {
  background: linear-gradient(90deg, rgba(0, 123, 255, 1) 0%, rgba(0, 232, 255, 1) 100%);
  box-shadow: 0 0 5px rgba(0, 232, 255, 0.8);
}

.ap-cost {
  background: linear-gradient(90deg, rgba(50, 205, 50, 1) 0%, rgba(144, 238, 144, 1) 100%);
  box-shadow: 0 0 5px rgba(144, 238, 144, 0.8);
}

.health-cost {
  background: linear-gradient(90deg, rgba(255, 69, 58, 1) 0%, rgba(255, 165, 0, 1) 100%);
  box-shadow: 0 0 5px rgba(255, 165, 0, 0.8);
}


/* Skill Type */
.skill-type {
  bottom: 3px;
  right: 3px;
  font-size: 0.9rem;
  color: white;
}

/* Icon */
.icon {
  position: absolute;
  width: 4rem; /* Smaller size */
  height: 4rem;
  left: 0.6rem;
  top: 0.6rem;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;

}

.icon img {
  z-index: 1;
  width: 100%;
  height: 100%;
}

.icon .placeholder {
  font-size: 1.5rem; /* Smaller placeholder */
  color: #ccc;
}

/* Skill Name */
.skill-name {
  z-index: 2;
  font-size: 0.5rem; /* Smaller text */
  text-transform: uppercase;
  margin-top: 0.2rem;
  /* color: #00e5ff; */
  color: #00e5ff;
  /* text-shadow: 0 0 5px #00e5ff; */
  text-shadow: 0 0 5px #00e5ff;
  background: rgba(0, 0, 0, 1);
  padding: 0.1rem 0.2rem;
  width: 90%;
  position: absolute;
  bottom: 0.1rem;

}

.fade {
  filter: grayscale(100%);
  opacity: 0.5;
}
</style>
