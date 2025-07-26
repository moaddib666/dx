<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import RPGGridWithScroller from "@/components/RPGGrid/RPGGridWithScroller.vue";
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import skillService from '@/services/skillService';
import { dragDropService } from '@/services/DragDropService.js';

// Props definition
const props = defineProps({
  // Grid configuration
  rows: {
    type: Number,
    default: 3
  },
  cols: {
    type: Number,
    default: 8
  },
  cellSize: {
    type: Number,
    default: 6 // Size in rem
  },
  // Drag configuration
  isDraggable: {
    type: Boolean,
    default: false
  },
  isSkillsDraggable: {
    type: Boolean,
    default: false
  }
});

// Emit events
const emit = defineEmits(['skillSelected']);

// State
const skills = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedSchool = ref('');
const selectedGrade = ref('');
const selectedType = ref('');
const schools = ref([]);
const grades = ref([]);
const types = ref([]);

// Dragging state
const position = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

// Computed properties
const filteredSkills = computed(() => {
  let result = skills.value;

  // Filter by school if selected
  if (selectedSchool.value) {
    result = result.filter(skill => skill.school === selectedSchool.value);
  }

  // Filter by grade if selected
  if (selectedGrade.value) {
    result = result.filter(skill => skill.grade === selectedGrade.value);
  }

  // Filter by type if selected
  if (selectedType.value) {
    result = result.filter(skill => skill.type === selectedType.value);
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter(skill =>
      skill.name.toLowerCase().includes(query) ||
      (skill.description && skill.description.toLowerCase().includes(query))
    );
  }

  return result;
});

// Event handlers
const onLoadingStarted = () => {
  isLoading.value = true;
  error.value = null;
};

const onSkillsLoaded = () => {
  skills.value = skillService.getAllSkills();
  isLoading.value = false;

  // Extract unique schools, grades, and types for the filters
  const schoolSet = new Set();
  const gradeSet = new Set();
  const typeSet = new Set();

  skills.value.forEach(skill => {
    if (skill.school) {
      schoolSet.add(skill.school);
    }
    if (skill.grade) {
      gradeSet.add(skill.grade);
    }
    if (skill.type) {
      typeSet.add(skill.type);
    }
  });

  schools.value = Array.from(schoolSet);
  grades.value = Array.from(gradeSet);
  types.value = Array.from(typeSet);
};

const onLoadingFailed = (err) => {
  console.error('Failed to load skills:', err);
  error.value = err.message || 'Failed to load skills';
  isLoading.value = false;
};

// UI actions
const refreshSkills = async () => {
  try {
    isLoading.value = true;
    await skillService.updateSkillsCache();
    onSkillsLoaded();
  } catch (err) {
    console.error('Error refreshing skills:', err);
    onLoadingFailed(err);
  }
};

const selectSkill = (skill) => {
  // Emit the selected skill to parent components
  emit('skillSelected', skill);
};

// Helper methods
const getSkillInitials = (name) => {
  if (!name) return '??';
  return name.substring(0, 2).toUpperCase();
};

const formatSchoolName = (schoolId) => {
  const school = skillService.getSchool(schoolId);
  if (!school) return schoolId;

  return school.name || schoolId;
};

// Handle drag start event
const onDragStart = (event, skill) => {
  if (!props.isSkillsDraggable) return;

  console.log('Drag start:', skill);

  // Set the drag data to the skill's JSON string
  const skillJson = JSON.stringify(skill);
  event.dataTransfer.setData('text/plain', skillJson);
  // Also set it as application/json for better compatibility
  event.dataTransfer.setData('application/json', skillJson);
  // Set a custom type to identify this as a skill
  event.dataTransfer.setData('application/rpg-skill', skillJson);

  // Set the drag effect to 'copy' to indicate that we're copying the skill
  event.dataTransfer.effectAllowed = 'copy';

  // Add a class to the dragged element for visual feedback
  event.target.classList.add('dragging');

  // Create a custom drag image
  const dragImage = createDragImage(skill);
  if (dragImage) {
    // Use the custom drag image
    event.dataTransfer.setDragImage(dragImage, dragImage.width / 2, dragImage.height / 2);

    // Clean up the drag image after a short delay
    setTimeout(() => {
      if (dragImage.parentNode) {
        document.body.removeChild(dragImage);
      }
    }, 100);
  }

  // Notify the drag drop service that we've started dragging
  dragDropService.startDrag({
    type: 'rpg-skill',
    data: skill
  });

  // Remove the class when the drag ends
  const onDragEnd = () => {
    event.target.classList.remove('dragging');
    event.target.removeEventListener('dragend', onDragEnd);
  };

  event.target.addEventListener('dragend', onDragEnd);
};

// Create a custom drag image
const createDragImage = (skill) => {
  // Create a new element for the drag image
  const dragImage = document.createElement('div');
  dragImage.className = 'custom-drag-image';

  // Add skill icon
  const iconContainer = document.createElement('div');
  iconContainer.className = 'drag-image-icon';

  if (skill.icon) {
    const img = document.createElement('img');
    img.src = skill.icon;
    img.alt = skill.name;
    iconContainer.appendChild(img);
  } else {
    // Create fancy placeholder
    iconContainer.classList.add('fancy-placeholder');

    const initials = document.createElement('span');
    initials.className = 'initials';
    initials.textContent = getSkillInitials(skill.name);
    iconContainer.appendChild(initials);
  }

  // Add skill name
  const nameContainer = document.createElement('div');
  nameContainer.className = 'drag-image-name';
  nameContainer.textContent = skill.name;

  // Add skill school if available
  if (skill.school) {
    const schoolContainer = document.createElement('div');
    schoolContainer.className = 'drag-image-school';
    schoolContainer.textContent = formatSchoolName(skill.school);
    dragImage.appendChild(schoolContainer);
  }

  // Assemble the drag image
  dragImage.appendChild(iconContainer);
  dragImage.appendChild(nameContainer);

  // Add styles
  Object.assign(dragImage.style, {
    position: 'absolute',
    top: '-1000px', // Position off-screen
    padding: '10px',
    background: '#444',
    border: '2px solid #1E90FF',
    borderRadius: '6px',
    boxShadow: '0 0 15px rgba(30, 144, 255, 0.8)',
    color: 'white',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '5px',
    zIndex: '9999',
    pointerEvents: 'none'
  });

  Object.assign(iconContainer.style, {
    width: '40px',
    height: '40px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#555',
    borderRadius: '4px',
    marginBottom: '5px',
    position: 'relative',
    overflow: 'hidden'
  });

  // Apply additional styles for fancy placeholder
  if (iconContainer.classList.contains('fancy-placeholder')) {
    Object.assign(iconContainer.style, {
      background: 'linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 100%)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)'
    });

    // Add the glow effect
    const glowEffect = document.createElement('div');
    Object.assign(glowEffect.style, {
      position: 'absolute',
      top: '-50%',
      left: '-50%',
      width: '200%',
      height: '200%',
      background: 'radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%)',
      animation: 'pulse 3s ease-in-out infinite',
      zIndex: '1'
    });
    iconContainer.appendChild(glowEffect);

    // Style the initials
    if (iconContainer.querySelector('.initials')) {
      Object.assign(iconContainer.querySelector('.initials').style, {
        position: 'relative',
        zIndex: '2',
        fontSize: '1rem',
        fontWeight: 'bold',
        textShadow: '0 1px 3px rgba(0, 0, 0, 0.5)',
        color: '#ffffff'
      });
    }
  }

  if (iconContainer.querySelector('img')) {
    Object.assign(iconContainer.querySelector('img').style, {
      maxWidth: '100%',
      maxHeight: '100%',
      objectFit: 'contain'
    });
  }

  Object.assign(nameContainer.style, {
    fontWeight: 'bold',
    fontSize: '12px',
    textAlign: 'center',
    maxWidth: '100px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap'
  });

  if (dragImage.querySelector('.drag-image-school')) {
    Object.assign(dragImage.querySelector('.drag-image-school').style, {
      fontSize: '10px',
      color: '#aaa',
      textTransform: 'capitalize'
    });
  }

  // Add to the document
  document.body.appendChild(dragImage);

  return dragImage;
};

// Dragging functionality
const startDrag = (event) => {
  if (!props.isDraggable) return;

  // Don't start drag if we're clicking on an interactive element
  const interactiveElements = ['INPUT', 'SELECT', 'BUTTON', 'A'];
  if (interactiveElements.includes(event.target.tagName)) {
    return;
  }

  isDragging.value = true;

  // Calculate the offset between mouse position and element's top-left corner
  // Use the RPGContainer element (first element with gm-rpg-skills class)
  const container = document.querySelector('.gm-rpg-skills');
  const rect = container ? container.getBoundingClientRect() : event.currentTarget.getBoundingClientRect();

  dragOffset.value = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };

  // Set initial position if not already set
  if (position.value.x === 0 && position.value.y === 0) {
    position.value = {
      x: rect.left,
      y: rect.top
    };
  }

  // Add event listeners for drag and end drag
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', endDrag);

  // Prevent default behavior
  event.preventDefault();
};

const onDrag = (event) => {
  if (!isDragging.value) return;

  // Get the container element to calculate its dimensions
  const container = document.querySelector('.gm-rpg-skills');
  const containerWidth = container ? container.offsetWidth : 300; // Default fallback width
  const containerHeight = container ? container.offsetHeight : 400; // Default fallback height

  // Get viewport dimensions
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  // Calculate new position based on mouse movement and offset
  let newX = event.clientX - dragOffset.value.x;
  let newY = event.clientY - dragOffset.value.y;

  // Apply boundary constraints to keep the component within the viewport
  // Left boundary
  newX = Math.max(0, newX);
  // Right boundary (subtract container width to prevent it from going off-screen)
  newX = Math.min(viewportWidth - containerWidth, newX);
  // Top boundary
  newY = Math.max(0, newY);
  // Bottom boundary (subtract container height to prevent it from going off-screen)
  newY = Math.min(viewportHeight - containerHeight, newY);

  // Update position
  position.value = {
    x: newX,
    y: newY
  };

  // Prevent default behavior
  event.preventDefault();
};

const endDrag = () => {
  isDragging.value = false;

  // Remove event listeners
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', endDrag);
};

// Handle image load errors
const handleImageError = (event, skill) => {
  // Replace the image with a fancy placeholder
  const img = event.target;
  const parent = img.parentNode;

  // Create fancy placeholder
  const placeholder = document.createElement('div');
  placeholder.className = 'skill-placeholder fancy-placeholder';

  // Add initials
  const initials = document.createElement('span');
  initials.className = 'initials';
  initials.textContent = getSkillInitials(skill.name);
  placeholder.appendChild(initials);

  // Replace the image with the placeholder
  parent.replaceChild(placeholder, img);
};

// Lifecycle hooks
onMounted(async () => {
  try {
    isLoading.value = true;

    // Initialize the service and load skills
    await skillService.updateSkillsCache();
    onSkillsLoaded();
  } catch (err) {
    console.error('Error initializing skills list:', err);
    onLoadingFailed(err);
  }
});

onBeforeUnmount(() => {
  // Clean up drag event listeners if they're still active
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', endDrag);
});
</script>

<template>
  <RPGContainer
    class="gm-rpg-skills"
    :class="{ 'draggable': isDraggable }"
    :style="isDraggable ? { position: 'absolute', left: position.x + 'px', top: position.y + 'px', zIndex: isDragging ? 1000 : 10 } : {}"
    @mousedown="startDrag"
  >
    <div class="skills-list-header">
      <h3>Skills</h3>
      <div class="filters-container">
        <div class="skills-filter">
          <select v-model="selectedSchool" class="filter-select school-filter">
            <option value="">All Schools</option>
            <option v-for="schoolId in schools" :key="schoolId" :value="schoolId">
              {{ formatSchoolName(schoolId) }}
            </option>
          </select>
        </div>
        <div class="skills-filter">
          <select v-model="selectedGrade" class="filter-select grade-filter">
            <option value="">All Grades</option>
            <option v-for="grade in grades" :key="grade" :value="grade">
              {{ grade }}
            </option>
          </select>
        </div>
        <div class="skills-filter">
          <select v-model="selectedType" class="filter-select type-filter">
            <option value="">All Types</option>
            <option v-for="type in types" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>
      </div>
      <div class="search-container">
        <input
          v-model="searchQuery"
          class="search-input"
          placeholder="Search skills..."
          type="text"
        />
        <button class="refresh-btn" title="Refresh Skills" @click="refreshSkills">
          <span class="icon-refresh"></span>
        </button>
      </div>
    </div>
    <div class="skills-grid-container">
      <div v-if="isLoading" class="loading-indicator">
        Loading skills...
      </div>

      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else-if="filteredSkills.length === 0" class="no-skills">
        No skills found.
      </div>

      <RPGGridWithScroller
        v-else
        :row-count="rows"
        :col-count="cols"
        :cell-size="cellSize"
        :items="filteredSkills"
        class="skills-grid"
        @grid-item-picked="selectSkill"
      >
        <template #default="{ item }">
          <div
            class="skill-wrapper"
            :draggable="isSkillsDraggable"
            @dragstart="onDragStart($event, item)"
            @click="selectSkill(item)"
          >
            <div
              class="skill-cell"
              :class="{
                'skill-type-border': item.type,
                [`skill-type-${item.type}`]: item.type,
                'skill-grade-border': item.grade,
                [`skill-grade-${item.grade}`]: item.grade
              }"
            >
              <div class="skill-icon">
                <img
                  v-if="item.icon"
                  :alt="item.name"
                  :src="item.icon"
                  class="skill-image"
                  @error="handleImageError($event, item)"
                />
                <div v-else class="skill-placeholder fancy-placeholder">
                  <span class="initials">{{ getSkillInitials(item.name) }}</span>
                </div>
              </div>
              <div class="skill-info">
                <div class="skill-name">{{ item.name }}</div>
                <div v-if="item.school" class="skill-school-label">{{ formatSchoolName(item.school) }}</div>
                <div v-if="item.grade" class="skill-grade-number">{{ item.grade }}</div>
              </div>
            </div>
          </div>
        </template>
      </RPGGridWithScroller>
    </div>
  </RPGContainer>
</template>

<style scoped>
.gm-rpg-skills {
  display: flex;
  flex-direction: column;
  color: #ffffff;
  border-radius: 4px;
  overflow: hidden;
}

.gm-rpg-skills.draggable {
  cursor: move;
}

.skills-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
}

.skills-list-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.search-container {
  display: flex;
  align-items: center;
}

.search-input {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 150px;
}

.refresh-btn {
  padding: 0.25rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.refresh-btn:hover {
  background: #555;
  color: #fff;
}

.icon-refresh::before {
  content: '↻';
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #444;
}

.skills-filter {
  flex: 1;
  min-width: 120px;
}

.filter-select {
  width: 100%;
  padding: 0.25rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 0.9rem;
}

.school-filter {
  min-width: 120px;
}

.grade-filter {
  min-width: 60px; /* More compact since it only contains numbers 0-9 */
  flex: 0.5; /* Take less space than other filters */
}

.type-filter {
  min-width: 100px;
}

.skills-grid-container {
  flex: 1;
  overflow: hidden;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.loading-indicator, .no-skills, .error-message {
  padding: 2rem;
  text-align: center;
  color: #999;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message {
  color: #ff6b6b;
}

.skills-grid {
  flex: 1;
}

.skill-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}

.skill-wrapper:hover {
  transform: scale(1.05);
}

.skill-wrapper.dragging {
  opacity: 0.9;
  background: #444;
  border: 2px solid #1E90FF;
  box-shadow: 0 0 12px rgba(30, 144, 255, 0.7);
  transform: scale(1.1);
  z-index: 1000;
  position: relative;
  cursor: grabbing;
}

.skill-cell {
  width: 90%;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 4px;
  padding: 0.3rem;
  position: relative;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

/* Type border styles */
.skill-type-border {
  border-left: 3px solid transparent;
}

.skill-type-attack {
  border-left-color: #ff1744;
  box-shadow: -2px 0 5px rgba(255, 23, 68, 0.4);
}

.skill-type-defense {
  border-left-color: #00e5ff;
  box-shadow: -2px 0 5px rgba(0, 229, 255, 0.4);
}

.skill-type-heal {
  border-left-color: #00ff00;
  box-shadow: -2px 0 5px rgba(0, 255, 0, 0.4);
}

.skill-type-Buff {
  border-left-color: #ffc107;
  box-shadow: -2px 0 5px rgba(255, 193, 7, 0.4);
}

.skill-type-debuff {
  border-left-color: #b71c1c;
  box-shadow: -2px 0 5px rgba(183, 28, 28, 0.4);
}

.skill-type-utility {
  border-left-color: #9e9e9e;
  box-shadow: -2px 0 5px rgba(158, 158, 158, 0.4);
}

.skill-type-special {
  border-left-color: #673ab7;
  box-shadow: -2px 0 5px rgba(103, 58, 183, 0.4);
}

/* Grade border styles */
.skill-grade-border {
  border-top: 3px solid transparent;
}

/* Hover effects */
.skill-wrapper:hover .skill-cell {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.skill-wrapper:hover .skill-type-border {
  border-left-width: 5px;
}

.skill-wrapper:hover .skill-grade-border {
  border-top-width: 5px;
}

.skill-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.3rem;
}

.skill-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.skill-placeholder {
  width: 100%;
  height: 100%;
  color: #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 4px;
}

.fancy-placeholder {
  background: linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
}

.fancy-placeholder::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%);
  animation: pulse 3s ease-in-out infinite;
}

.fancy-placeholder::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 30%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.2), transparent);
}

.fancy-placeholder .initials {
  position: relative;
  z-index: 2;
  font-size: 1rem;
  font-weight: bold;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  background: linear-gradient(to bottom, #ffffff, #cccccc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: float 2s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    transform: rotate(0deg);
    opacity: 0.5;
  }
  50% {
    opacity: 0.7;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.5;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

.skill-info {
  width: 100%;
  text-align: center;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.skill-name {
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  margin-bottom: 0.2rem;
}

.skill-school-label {
  font-size: 0.65rem;
  color: #aaa;
  text-transform: capitalize;
  background: rgba(0, 0, 0, 0.2);
  padding: 0.1rem 0.3rem;
  border-radius: 2px;
  margin-top: 0.1rem;
}

.skill-grade-number {
  position: absolute;
  top: -0.5rem;
  right: -0.5rem;
  font-size: 0.7rem;
  font-weight: bold;
  background: #333;
  color: white;
  width: 1.2rem;
  height: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}
</style>