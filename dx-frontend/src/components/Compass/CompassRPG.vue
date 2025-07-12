<script setup lang="ts">
// Arrow must dynamically rotate based on the current direction hovered
// If center section is hovered, and the stairs exists we must show the stairs instead of the arrow
// If stairs are locked, we must show the locked stairs
// If direction is active, it must show the active section
// If direction is unavailable, it must show the unavailable section
// If direction is dangerous, it must show the danger section
// if direction is locked, it must show the locked section
// The pressed section must be emitted to the parent component
import { computed, ref } from 'vue';
import { WorldPosition, PositionConnection } from '@/api/dx-backend/api';

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

  // Flatten the connections array and check for vertical connections
  return props.position.connections.flat().some(conn =>
    conn.is_vertical === 'up' || conn.is_vertical === 'down'
  );
});

const stairsLocked = computed(() => {
  if (!props.position?.connections) return true;

  // Check if vertical connections are locked
  return props.position.connections.flat()
    .filter(conn => conn.is_vertical === 'up' || conn.is_vertical === 'down')
    .some(conn => conn.locked);
});

// Map connections to compass directions
const connectionMap = computed(() => {
  if (!props.position?.connections) {
    console.warn('No connections available for the position.', props.position);
    return {};
  }

  const flatConnections = props.position.connections.flat();
  const map: Record<string, PositionConnection> = {};

  console.debug('Mapping connections to directions:', flatConnections);
  // Process each connection and map to a direction
  flatConnections.forEach(conn => {
    // Skip vertical connections (handled separately for stairs)
    if (conn.is_vertical === 'up' || conn.is_vertical === 'down') return;

    // Map horizontal directions
    if (conn.is_horizontal === 'north-west') map[DIRECTIONS.TOP_LEFT] = conn;
    else if (conn.is_horizontal === 'north') map[DIRECTIONS.TOP_CENTER] = conn;
    else if (conn.is_horizontal === 'north-east') map[DIRECTIONS.TOP_RIGHT] = conn;
    else if (conn.is_horizontal === 'west') map[DIRECTIONS.MIDDLE_LEFT] = conn;
    else if (conn.is_horizontal === 'east') map[DIRECTIONS.MIDDLE_RIGHT] = conn;
    else if (conn.is_horizontal === 'south-west') map[DIRECTIONS.BOTTOM_LEFT] = conn;
    else if (conn.is_horizontal === 'south') map[DIRECTIONS.BOTTOM_CENTER] = conn;
    else if (conn.is_horizontal === 'south-east') map[DIRECTIONS.BOTTOM_RIGHT] = conn;
  });

  return map;
});

// Get the status class for a direction
const getDirectionClass = (direction: string) => {
  const conn = connectionMap.value[direction];
  if (!conn) return 'unavailable';
  if (conn.locked) return 'locked';

  // Check if the position is dangerous (not safe)
  const targetPosition = conn.position_to_details;
  if (targetPosition && targetPosition.is_safe === false) return 'danger';

  return 'active';
};

// Handle hover on a direction
const handleHover = (direction: string | null) => {
  hoveredDirection.value = direction;
};

// Handle click on a direction
const handleMove = (direction: string) => {
  const conn = connectionMap.value[direction];
  if (conn && !conn.locked) {
    emit('move', conn);
  }
};

// Handle click on stairs
const handleStairsMove = () => {
  if (!props.position?.connections || stairsLocked.value) return;

  const verticalConn = props.position.connections.flat()
    .find(conn => conn.is_vertical === 'up' || conn.is_vertical === 'down');

  if (verticalConn && !verticalConn.locked) {
    emit('move', verticalConn);
  }
};

// Get the arrow rotation class based on hovered direction
const arrowRotationClass = computed(() => {
  if (!hoveredDirection.value) return 'arrow-up';
  return ARROW_ROTATIONS[hoveredDirection.value] || 'arrow-up';
});

</script>

<template>
  <div class="compass--holder">
    <div class="compass--container">
      <div class="compass--background">
        <!-- Arrow that rotates based on hovered direction -->
        <div
          class="compass--background--real-center arrow"
          :class="arrowRotationClass"
          v-if="!hasStairs || hoveredDirection !== DIRECTIONS.MIDDLE_CENTER"
        ></div>

        <!-- Stairs for vertical movement (up/down) -->
        <div
          class="compass--background--stairs stairs"
          :class="{ 'stairs--locked': stairsLocked }"
          v-if="hasStairs && hoveredDirection === DIRECTIONS.MIDDLE_CENTER"
          @click="handleStairsMove"
        >
          <div class="stairs-arrow stairs-arrow-down"></div>
          <div class="stairs-arrow stairs-arrow-up"></div>
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
          :class="{ 'danger': hasStairs && stairsLocked }"
          @mouseover="handleHover(DIRECTIONS.MIDDLE_CENTER)"
          @mouseleave="handleHover(null)"
          @click="handleStairsMove"
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
  margin: 0.5rem auto;
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
}

.compass--background--real-center {
  width: 50%;
  height: 50%;
  border-radius: 50%;
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
}

.arrow-up {
  transform: rotate(0deg);
}

.arrow-up-left {
  transform: rotate(45deg);
}

.arrow-up-right {
  transform: rotate(-45deg);
}

.arrow-down {
  transform: rotate(180deg);
}

.arrow-down-left {
  transform: rotate(135deg);
}

.arrow-left {
  transform: rotate(90deg);
}

.arrow-down-right {
  transform: rotate(-135deg);
}

.arrow-right {
  transform: rotate(-90deg);
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