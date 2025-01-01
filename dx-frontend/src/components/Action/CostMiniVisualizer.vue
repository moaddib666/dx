<template>
  <div class="cost-visualizer">
    <div
        v-for="cost in costList"
        :key="cost.kind"
        :class="['cost-item', costClass(cost.kind)]"
        :title="`${cost.kind} Cost: ${cost.value}`"
    >
      <span class="cost-value">{{ cost.value }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "CostMiniVisualizer",
  props: {
    cost: {
      type: Array,
      required: true, // Expects an array of cost objects: [{ kind: 'Action Points', value: 10 }, ...]
    },
  },
  computed: {
    costList() {
      return this.cost || []; // Fallback to an empty array if no costs are provided
    },
  },
  methods: {
    costClass(kind) {
      const classes = {
        "Action Points": "ap-cost",
        Energy: "energy-cost",
        Health: "health-cost",
      };
      return classes[kind] || "default-cost";
    },
  },
};
</script>

<style scoped>
.cost-visualizer {
  display: flex;
  gap: 0.3rem; /* Space between cost items */
  flex-wrap: wrap; /* Allow wrapping for responsiveness */
  justify-content: center;
  align-items: center;
  font-size: 0.7rem;
}

.cost-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5em; /* Fixed size for each square */
  height: 1.5em;
  border-radius: 0.3em;
  font-weight: bold;
  text-align: center;
  color: #fff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  transition: transform 0.2s ease-in-out;
}

.cost-item:hover {
  transform: scale(1.1); /* Slightly enlarge on hover */
}

/* Cost Types */
.ap-cost {
  background: linear-gradient(90deg, rgba(50, 205, 50, 1) 0%, rgba(144, 238, 144, 1) 100%);
  box-shadow: 0 0 5px rgba(144, 238, 144, 0.8);
}

.energy-cost {
  background: linear-gradient(90deg, rgba(0, 123, 255, 1) 0%, rgba(0, 232, 255, 1) 100%);
  box-shadow: 0 0 5px rgba(0, 232, 255, 0.8);
}

.health-cost {
  background: linear-gradient(90deg, rgba(255, 69, 58, 1) 0%, rgba(255, 165, 0, 1) 100%);
  box-shadow: 0 0 5px rgba(255, 165, 0, 0.8);
}

.default-cost {
  background: linear-gradient(90deg, rgba(128, 128, 128, 1) 0%, rgba(192, 192, 192, 1) 100%);
  box-shadow: 0 0 5px rgba(192, 192, 192, 0.8);
}

.cost-value {
  z-index: 1;
}
</style>
