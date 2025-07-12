<script setup lang="ts">
// Arrow must dynamically rotate based on the current direction hovered
// If center section is hovered, and the stairs exists we must show the stairs instead of the arrow
// If stairs are locked, we must show the locked stairs
// If direction is active, it must show the active section
// If direction is unavailable, it must show the unavailable section
// If direction is dangerous, it must show the danger section
// if direction is locked, it must show the locked section
// The pressed section must be emitted to the parent component
import {computed, ref} from 'vue';
import {WorldPosition, PositionConnection} from '@/api/dx-backend/api';

// Direction mapping constants
const DIRECTIONS = {
  TOP_LEFT: 'top-left',
  TOP_CENTER: 'top-center',
  TOP_RIGHT: 'top-right',
  MIDDLE_LEFT: 'middle-left',
  MIDDLE_CENTER: 'middle-center',
  MIDDLE_RIGHT: 'middle-right',
  BOTTOM_LEFT: 'bottom-left',
  BOTTOM_CENTER: 'bottom-center',
  BOTTOM_RIGHT: 'bottom-right'
};

// Arrow rotation classes mapping
const ARROW_ROTATIONS = {
  [DIRECTIONS.TOP_LEFT]: 'arrow-up-left',
  [DIRECTIONS.TOP_CENTER]: 'arrow-up',
  [DIRECTIONS.TOP_RIGHT]: 'arrow-up-right',
  [DIRECTIONS.MIDDLE_LEFT]: 'arrow-left',
  [DIRECTIONS.MIDDLE_CENTER]: '',
  [DIRECTIONS.MIDDLE_RIGHT]: 'arrow-right',
  [DIRECTIONS.BOTTOM_LEFT]: 'arrow-down-left',
  [DIRECTIONS.BOTTOM_CENTER]: 'arrow-down',
  [DIRECTIONS.BOTTOM_RIGHT]: 'arrow-down-right'
};

const props = defineProps({
  position: {
    type: Object as () => WorldPosition,
    required: false,
    default: () => ({
      id: '',
      connections: [],
      characters: [],
      anomalies: [],
      sub_location: '',
      location: '',
      is_safe: true
    })
  }
});

const emit = defineEmits(['move']);

// State for hover and interaction
const hoveredDirection = ref<string | null>(null);
const hasStairs = computed(() => {
  // Check if there are vertical connections (up/down)
  if (!props.position?.connections) return false;
  for (const conn of props.position.connections) {
    if (conn.direction && (conn.direction.toLowerCase() === 'up' || conn.direction.toLowerCase() === 'down')) {
      return true;
    }
  }
  return false;
});

const stairsLocked = computed(() => {
// check middle center connection for stairs
  if (!props.position?.connections) return true;
  const connection = connectionMap.value[DIRECTIONS.MIDDLE_CENTER];
  return connection?.is_locked || false; // Default to false if is_locked is not specified
});

// Map connections to compass directions
const connectionMap = computed(() => {
  if (!props.position?.connections) {
    console.warn('[CompassRPG]', 'No connections available for the position.', props.position);
    return {};
  }

  const connections = props.position.connections;
  const map: Record<string, PositionConnection> = {};

  console.debug('[CompassRPG]', 'Mapping connections to directions:', connections);
  // Process each connection and map to a direction
  connections.forEach(conn => {
    // Skip invalid or inactive connections
    if (!conn || conn.is_active === false) return;

    // Map directions based on the direction property
    const direction = conn.direction?.toLowerCase();
    if (!direction) return;

    if (direction === 'north-west') map[DIRECTIONS.TOP_LEFT] = conn;
    else if (direction === 'north') map[DIRECTIONS.TOP_CENTER] = conn;
    else if (direction === 'north-east') map[DIRECTIONS.TOP_RIGHT] = conn;
    else if (direction === 'west') map[DIRECTIONS.MIDDLE_LEFT] = conn;
    else if (direction === 'east') map[DIRECTIONS.MIDDLE_RIGHT] = conn;
    else if (direction === 'south-west') map[DIRECTIONS.BOTTOM_LEFT] = conn;
    else if (direction === 'south') map[DIRECTIONS.BOTTOM_CENTER] = conn;
    else if (direction === 'south-east') map[DIRECTIONS.BOTTOM_RIGHT] = conn;
    else if (direction === 'up' || direction === 'down') map[DIRECTIONS.MIDDLE_CENTER] = conn; // Use middle center for vertical connections
    else {
      console.warn('[CompassRPG]', 'Unknown direction:', direction, 'for connection:', conn);
    }
  });

  return map;
});

const is_downstairs = computed(() => {
  // Check if the current position has stairs
  return props.position?.connections.some(conn => conn.direction?.toLowerCase() === 'down');
});

const is_upstairs = computed(() => {
  // Check if the current position has stairs
  return props.position?.connections.some(conn => conn.direction?.toLowerCase() === 'up');
});

// Get the status class for a direction
const getDirectionClass = (direction: string) => {
  const conn = connectionMap.value[direction];
  if (!conn) return 'unavailable';

  // Check if the connection is locked - this takes precedence over other statuses
  // Default to false if is_locked is not specified
  if (conn.is_locked === true) return 'locked';

  // In the current data structure, we don't have position_to_details
  // We'll check if the position itself is marked as unsafe
  // if (props.position && props.position.is_safe === false) return 'danger';

  return 'active';
};

// Handle hover on a direction
const handleHover = (direction: string | null) => {
  console.debug('[CompassRPG]', 'Hovering over direction:', direction);
  const con = connectionMap.value[direction || ''];
  if (!con) {
    return;
  }
  hoveredDirection.value = direction;
};

// Handle click on a direction
const handleMove = (direction: string) => {
  const conn = connectionMap.value[direction];
  // Allow movement if connection exists and is not locked
  // Default to allowing movement if is_locked is not specified
  if (conn && conn.is_locked !== true) {
    emit('move', conn);
  } else {
    console.warn('[CompassRPG]', 'Cannot move in direction:', direction, 'Connection', conn, ' is locked or does not exist.');
  }
};

// Handle click on stairs
const handleStairsMove = () => {
  // Since vertical connections are not supported in the current data structure,
  // this function does nothing
  return;
};

// Get the arrow rotation class based on hovered direction
const arrowRotationClass = computed(() => {
  console.debug('[CompassRPG]', 'Hovered direction:', hoveredDirection.value);
  if (!hoveredDirection.value) return 'arrow-up';
  const arrowDirection = ARROW_ROTATIONS[hoveredDirection.value] || 'arrow-up';
  console.debug('[CompassRPG]', 'Arrow rotation class:', arrowDirection);
  return arrowDirection;
});

</script>

<template>
  <div class="compass--holder">
    <div class="compass--container">
      <div class="compass--background">
        <!-- Arrow that rotates based on hovered direction -->
        <div
            class="arrow-wrapper"
            v-if="!hasStairs || hoveredDirection !== DIRECTIONS.MIDDLE_CENTER"
        >
          <div
              class="compass--background--real-center arrow"
              :class="arrowRotationClass"
          ></div>
        </div>

        <!-- Stairs for vertical movement (up/down) -->
        <div
            class="compass--background--stairs stairs"
            :class="{ 'stairs--locked': stairsLocked }"
            v-if="hasStairs && hoveredDirection === DIRECTIONS.MIDDLE_CENTER"
        >
          <div class="stairs-arrow stairs-arrow-down" v-if="is_downstairs"></div>
          <div class="stairs-arrow stairs-arrow-up" v-if="is_upstairs"></div>
        </div>
      </div>

      <!-- Outer compass sections -->
      <div class="compass--outer--mask">
        <div class="compass--outer">
          <!-- Top row -->
          <div
              class="compass--outer--section--top--left compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.TOP_LEFT)"
              @mouseover="handleHover(DIRECTIONS.TOP_LEFT)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.TOP_LEFT)"
          ></div>
          <div
              class="compass--outer--section--top--center compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.TOP_CENTER)"
              @mouseover="handleHover(DIRECTIONS.TOP_CENTER)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.TOP_CENTER)"
          ></div>
          <div
              class="compass--outer--section--top--right compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.TOP_RIGHT)"
              @mouseover="handleHover(DIRECTIONS.TOP_RIGHT)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.TOP_RIGHT)"
          ></div>

          <!-- Middle row -->
          <div
              class="compass--outer--section--middle--left compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.MIDDLE_LEFT)"
              @mouseover="handleHover(DIRECTIONS.MIDDLE_LEFT)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.MIDDLE_LEFT)"
          ></div>
          <div
              class="compass--outer--section--middle--center compass--outer--section"
              @mouseover="handleHover(DIRECTIONS.MIDDLE_CENTER)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.MIDDLE_CENTER)"
          ></div>
          <div
              class="compass--outer--section--middle--right compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.MIDDLE_RIGHT)"
              @mouseover="handleHover(DIRECTIONS.MIDDLE_RIGHT)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.MIDDLE_RIGHT)"
          ></div>

          <!-- Bottom row -->
          <div
              class="compass--outer--section--bottom--left compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.BOTTOM_LEFT)"
              @mouseover="handleHover(DIRECTIONS.BOTTOM_LEFT)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.BOTTOM_LEFT)"
          ></div>
          <div
              class="compass--outer--section--bottom--center compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.BOTTOM_CENTER)"
              @mouseover="handleHover(DIRECTIONS.BOTTOM_CENTER)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.BOTTOM_CENTER)"
          ></div>
          <div
              class="compass--outer--section--bottom--right compass--outer--section"
              :class="getDirectionClass(DIRECTIONS.BOTTOM_RIGHT)"
              @mouseover="handleHover(DIRECTIONS.BOTTOM_RIGHT)"
              @mouseleave="handleHover(null)"
              @click="handleMove(DIRECTIONS.BOTTOM_RIGHT)"
          ></div>
        </div>
      </div>

      <!-- Inner compass (center) -->
      <div class="compass--inner--mask">
        <div
            class="compass--inner"
            :class="{
              'locked': hasStairs && stairsLocked ,
              'active': hasStairs,
            }"
        ></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.compass--holder {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.compass--container {
  min-width: 15rem;
  min-height: 15rem;
  background-image: url('@/assets/images/compass/compass.png');
  background-size: cover;
  background-position: center;
  position: relative;
}

.compass--outer--mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mask-image: url('@/assets/images/compass/compass-mask.png');
  mask-size: cover;
  mask-position: center;
  -webkit-mask-position: center;
  -webkit-mask-image: url('@/assets/images/compass/compass-mask-selectors.png');
  -webkit-mask-size: cover;
}

.compass--outer {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);

}

.compass--outer--section--middle--center {
  transform: scale(0.6);
  cursor: pointer;
}

.compass--outer--section {
  transition: opacity 0.3s ease, transform 0.3s ease;
  mix-blend-mode: multiply;
}

.compass--outer--section:hover {
  opacity: 1;
  transform: scale(1.05);

}

.active {
  cursor: pointer;
  background: linear-gradient(90deg, rgba(22, 234, 255, 1) 0%, rgba(0, 212, 255, 1) 100%);
}

.locked {
  cursor: pointer;
  background: linear-gradient(90deg, rgba(255, 255, 0, 1) 0%, rgba(255, 165, 0, 1) 100%);
}

.unavailable {
  background: linear-gradient(90deg, rgba(128, 128, 128, 1) 0%, rgba(192, 192, 192, 1) 100%);
}

.danger {
  cursor: pointer;
  background: linear-gradient(90deg, rgba(255, 0, 0, 1) 0%, rgba(255, 69, 0, 1) 100%);
}

.compass--inner--mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mask-image: url('@/assets/images/compass/compass-mask-circle.png');
  mask-size: cover;
  mask-position: center;
  -webkit-mask-image: url('@/assets/images/compass/compass-mask-circle.png');
  -webkit-mask-size: cover;
  pointer-events: none;
}

.compass--inner {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  opacity: 0.5;
  mix-blend-mode: multiply;
}

.compass--background {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 45%;
  height: 45%;
  transform: translate(-50%, -50%);
  z-index: -1; /* Ensure it stays behind other elements */
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none; /* Prevent interaction with the background */
}

.compass--background--real-center {
  width: 50%;
  height: 50%;
  border-radius: 50%;
}

.arrow-wrapper {
  width: 50%;
  height: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: arrow-shake 5s ease-in-out infinite;
}

@keyframes arrow-shake {
  0% {
    transform: rotate(0deg);
  }
  1% {
    transform: rotate(-5deg);
  }
  2% {
    transform: rotate(4deg);
  }
  3% {
    transform: rotate(-3deg);
  }
  4% {
    transform: rotate(2deg);
  }
  5%, 85%, 100% {
    transform: rotate(0deg);
  }
  86% {
    transform: rotate(-5deg);
  }
  87% {
    transform: rotate(4deg);
  }
  88% {
    transform: rotate(-3deg);
  }
  89% {
    transform: rotate(2deg);
  }
  90% {
    transform: rotate(0deg);
  }
}

.compass--background--stairs {
  width: 100%;
  height: 100%;
  background-size: cover;
  position: relative;
}

.arrow {
  background: url('@/assets/images/compass/compass-arrow.png') no-repeat center center;
  background-size: contain;
  transition: transform 0.3s ease;
  width: 100%;
  height: 100%;
}


.arrow-up {
  transform: rotate(0deg);
}

.arrow-up-left {
  transform: rotate(-45deg);
}

.arrow-up-right {
  transform: rotate(45deg);
}

.arrow-down {
  transform: rotate(180deg);
}

.arrow-down-left {
  transform: rotate(-135deg);
}

.arrow-left {
  transform: rotate(-90deg);
}

.arrow-down-right {
  transform: rotate(135deg);
}

.arrow-right {
  transform: rotate(90deg);
}

.arrow:hover {
  cursor: pointer;
  transform: scale(1.1);
}


.stairs {
  background: url('@/assets/images/compass/compass-stairs.png') no-repeat center center;
  background-size: 50% 50%;
}

.stairs-arrow {

}

.stairs--locked {
  filter: grayscale(100%);
}

.stairs-arrow-down {
  background: url('@/assets/images/compass/compass-stairs-arrow-down.png') no-repeat center center;
  transform: rotate(0deg);
  background-size: contain;
  width: 20%;
  height: 20%;
  position: absolute;
  top: 50%;
  left: 20%;
}

.stairs-arrow-up {
  background: url('@/assets/images/compass/compass-stairs-arrow-down.png') no-repeat center center;
  transform: rotate(180deg);
  background-size: contain;
  width: 20%;
  height: 20%;
  position: absolute;
  top: 20%;
  right: 20%;
}


</style>