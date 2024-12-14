<template>
  <div class="countdown" v-if="valueToDisplay > 0">
    <h1 id="timeLeft" :class="countdownClass">
      ⏳ <span>{{ valueToDisplay }}</span>
    </h1>
  </div>
</template>

<script>
import { Turn } from "@/models/Turn";

export default {
  name: "CountDown",
  props: {
    turn: {
      type: Turn,
      required: true,
    },
  },
  data() {
    return {
      valueToDisplay: 0,
      countdownInterval: null,
    };
  },
  computed: {
    countdownClass() {
      if (this.valueToDisplay <= 5) {
        return 'alert pulse';
      } else if (this.valueToDisplay <= 15) {
        return 'warning pulse';
      }
      return '';
    },
  },
  watch: {
    turn: {
      handler(newVal) {
        this.startCountdown(newVal);
      },
      immediate: true,
      deep: true,
    },
  },
  methods: {
    startCountdown(turn) {
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
      }

      const updateCountdown = () => {
        this.valueToDisplay = Math.max(Math.round(turn.timeLeft()), 0);
        if (this.valueToDisplay <= 0) {
          clearInterval(this.countdownInterval);
        }
      };

      updateCountdown();
      this.countdownInterval = setInterval(updateCountdown, 1000);
    },
  },
  mounted() {
    this.startCountdown(this.turn);
  },
  beforeDestroy() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }
  },
};
</script>

<style scoped>
.countdown {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  font-weight: bold;
  color: white;
}

#timeLeft {
  font-size: 3rem;
  font-family: 'Orbitron', sans-serif;
  width: 9rem;
  text-align: left;
  padding: 1rem;
}

.pulse {
  animation: pulse 1s infinite;
}

.warning {
  color: var(--cyber-yellow);
}

.alert {
  color: var(--crimson-red);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
</style>
