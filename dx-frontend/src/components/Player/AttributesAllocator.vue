<template>
  <div class="attributes-allocator">
    <h2>{{ t('playerComponents.attributesAllocator.title') }}</h2>
    <p>{{ t('playerComponents.attributesAllocator.availablePoints') }}<span class="available-points">{{ remainingPoints }}</span></p>
    <div class="attributes-list">
      <div
          v-for="(stat, key) in characteristics"
          :key="key"
          class="attribute-item"
      >
        <div class="attribute-details">
          <div class="attribute-name">
            <span>{{ stat.name }}</span>
            <span class="attribute-value">{{ allocatedPoints[key] }}</span>
          </div>
          <div class="attribute-bar">
            <button
                :disabled="allocatedPoints[key] === 0"
                class="decrease-btn"
                @click="decreasePoints(key)"
            >
              -
            </button>
            <div class="bar">
              <div
                  :style="{ width: `${(allocatedPoints[key] / maxPointsPerAttribute) * 100}%` }"
                  class="filled-bar"
              ></div>
            </div>
            <button
                :disabled="remainingPoints === 0"
                class="increase-btn"
                @click="increasePoints(key)"
            >
              +
            </button>
          </div>
        </div>
        <p class="attribute-description">{{ stat.description }}</p>
      </div>
    </div>
    <button
        :disabled="remainingPoints > 0"
        class="submit-button"
        @click="submitAllocation"
    >
      {{ t('playerComponents.attributesAllocator.submitAllocation') }}
    </button>
  </div>
</template>

<script>
import {computed, reactive} from "vue";
import { useI18n } from 'vue-i18n';

export default {
  name: "AttributesAllocator",
  props: {
    availablePoints: {
      type: Number,
      required: true,
    },
    characteristics: {
      type: Object,
      required: true,
    },
  },
  setup(props, {emit}) {
    const { t } = useI18n();
    const allocatedPoints = reactive({});
    const maxPointsPerAttribute = 10;

    // Initialize allocation for each characteristic
    for (const key in props.characteristics) {
      allocatedPoints[key] = 0;
    }

    const remainingPoints = computed(() => {
      return (
          props.availablePoints -
          Object.values(allocatedPoints).reduce((sum, val) => sum + val, 0)
      );
    });

    const increasePoints = (statKey) => {
      if (remainingPoints.value > 0 && allocatedPoints[statKey] < maxPointsPerAttribute) {
        allocatedPoints[statKey]++;
      }
    };

    const decreasePoints = (statKey) => {
      if (allocatedPoints[statKey] > 0) {
        allocatedPoints[statKey]--;
      }
    };

    const submitAllocation = () => {
      emit("submit", allocatedPoints);
    };

    return {
      t,
      allocatedPoints,
      remainingPoints,
      increasePoints,
      decreasePoints,
      submitAllocation,
      maxPointsPerAttribute,
    };
  },
};
</script>
<style scoped>
/* Colors and Typography */
.attributes-allocator {
  text-align: center;
  color: var(--glowing-white);
  background-color: var(--gunmetal);
  padding: 20px;
  border-radius: 10px;
  max-width: 800px;
  margin: auto;
  font-family: 'Roboto', sans-serif;
}

h2 {
  font-family: 'Montserrat', sans-serif;
  color: var(--electric-blue);
  margin-bottom: 10px;
}

.available-points {
  font-weight: bold;
  color: var(--lime-green);
}

.attributes-list {
  margin-top: 20px;
}

.attribute-item {
  margin-bottom: 20px;
  padding: 10px;
  background-color: var(--dark-slate-gray);
  border-radius: 8px;
  border: 1px solid var(--deep-purple);
}

.attribute-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.attribute-name {
  font-size: 18px;
  font-weight: bold;
  color: var(--cyber-yellow);
}

.attribute-value {
  margin-left: 10px;
  color: var(--neon-pink);
}

.attribute-bar {
  display: flex;
  align-items: center;
  width: 70%;
}

.bar {
  flex: 1;
  height: 10px;
  background-color: var(--gunmetal);
  border-radius: 5px;
  overflow: hidden;
  margin: 0 10px;
  position: relative;
  border: 1px solid var(--lime-green);
}

.filled-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--electric-blue), var(--neon-pink));
  transition: width 0.3s ease;
}

button {
  padding: 5px 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  font-family: 'Montserrat', sans-serif;
  cursor: pointer;
}

.decrease-btn {
  background-color: var(--crimson-red);
  color: var(--glowing-white);
}

.decrease-btn:disabled {
  background-color: var(--dark-slate-gray);
  cursor: not-allowed;
}

.increase-btn {
  background-color: var(--lime-green);
  color: var(--glowing-white);
}

.increase-btn:disabled {
  background-color: var(--dark-slate-gray);
  cursor: not-allowed;
}

.attribute-description {
  margin-top: 5px;
  font-size: 14px;
  color: var(--cyber-yellow);
}

.submit-button {
  margin-top: 20px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-family: 'Montserrat', sans-serif;
  background: linear-gradient(90deg, var(--electric-blue), var(--neon-pink));
  color: var(--glowing-white);
  font-size: 18px;
  cursor: pointer;
}

.submit-button:disabled {
  background: var(--dark-slate-gray);
  cursor: not-allowed;
}
</style>