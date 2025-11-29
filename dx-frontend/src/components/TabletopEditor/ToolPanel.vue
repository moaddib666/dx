<template>
  <div class="tool-panel">
    <h3 class="tool-panel-title">Editor Tools</h3>

    <!-- Mode Switch -->
    <div class="mode-switch">
      <button
        class="mode-button"
        :class="{ active: editorMode === 'config' }"
        @click="changeMode('config')"
      >
        Map Config
      </button>
      <button
        class="mode-button"
        :class="{ active: editorMode === 'availability' }"
        @click="changeMode('availability')"
      >
        Availability
      </button>
      <button
        class="mode-button"
        :class="{ active: editorMode === 'object' }"
        @click="changeMode('object')"
      >
        Objects
      </button>
      <button
        class="mode-button"
        :class="{ active: editorMode === 'path' }"
        @click="changeMode('path')"
      >
        Paths
      </button>
    </div>

    <div class="tools-list">
      <button
        v-for="tool in visibleTools"
        :key="tool.id"
        :class="['tool-button', { 'active': tool.id === selectedTool }]"
        @click="selectTool(tool.id)"
        :title="tool.description"
      >
        <span class="tool-icon">{{ tool.icon }}</span>
        <span class="tool-name">{{ tool.name }}</span>
      </button>
    </div>

    <div class="tool-options">
      <h4 class="options-title">Legend / View Options</h4>
      <label class="option-checkbox">
        <input type="checkbox" :checked="availabilityVisible" @change="toggleAvailability" />
        <span>Show Availability</span>
      </label>
      <label class="option-checkbox">
        <input type="checkbox" :checked="pathsVisible" @change="togglePaths" />
        <span>Show Paths</span>
      </label>
      <label class="option-checkbox">
        <input type="checkbox" :checked="objectsVisible" @change="toggleObjects" />
        <span>Show Objects</span>
      </label>
      <label class="option-checkbox">
        <input type="checkbox" :checked="gridVisible" @change="toggleGrid" />
        <span>Show Grid</span>
      </label>
      <label class="option-checkbox">
        <input type="checkbox" :checked="backgroundVisible" @change="toggleBackground" />
        <span>Show Background</span>
      </label>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'ToolPanel',
  data() {
    return {
      tools: [
        {
          id: 'select',
          name: 'Select',
          icon: '👆',
          description: 'Select and inspect cells'
        },
        {
          id: 'availability',
          name: 'Availability',
          icon: '🚫',
          description: 'Toggle cell availability (spawning/movement)'
        },
        {
          id: 'wall',
          // Internally still uses the 'wall' tool id, but in Path mode this
          // acts as the Path/Edge editing tool.
          name: 'Path / Edges',
          icon: '🧭',
          description: 'Edit movement paths and connections between cells'
        },
        {
          id: 'spawner-player',
          name: 'Player Spawner',
          icon: '👤',
          description: 'Place player spawn points'
        },
        {
          id: 'spawner-npc',
          name: 'NPC Spawner',
          icon: '👹',
          description: 'Place NPC/enemy spawn points'
        },
        {
          id: 'spawner-object',
          name: 'Object Spawner',
          icon: '📦',
          description: 'Place object spawn points'
        },
        {
          id: 'spawner-effect',
          name: 'Effect Spawner',
          icon: '✨',
          description: 'Place effect/trap spawn points'
        },
        {
          id: 'erase',
          name: 'Erase',
          icon: '🗑️',
          description: 'Remove spawners and objects'
        }
      ]
    };
  },
  computed: {
    ...mapGetters('tabletopEditor', [
      'selectedTool',
      'gridVisible',
      'backgroundVisible',
      'editorMode',
      'availabilityVisible',
      'pathsVisible',
      'objectsVisible'
    ]),

    visibleTools() {
      // Filter tools based on the current editor mode
      if (this.editorMode === 'config') {
        // Map Config mode does not need placement tools; keep only Select
        return this.tools.filter(tool => tool.id === 'select');
      }

      if (this.editorMode === 'availability') {
        return this.tools.filter(tool =>
          tool.id === 'select' || tool.id === 'availability'
        );
      }

      if (this.editorMode === 'object') {
        return this.tools.filter(tool =>
          tool.id === 'select' ||
          tool.id === 'spawner-player' ||
          tool.id === 'spawner-npc' ||
          tool.id === 'spawner-object' ||
          tool.id === 'spawner-effect' ||
          tool.id === 'erase'
        );
      }

      // Path mode: select + path/edges tool (internally 'wall')
      if (this.editorMode === 'path') {
        return this.tools.filter(tool =>
          tool.id === 'select' || tool.id === 'wall'
        );
      }

      // Fallback: show all tools
      return this.tools;
    }
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'selectTool',
      'toggleGridVisibility',
      'toggleBackgroundVisibility',
      'setEditorMode',
      'toggleAvailabilityVisibility',
      'togglePathsVisibility',
      'toggleObjectsVisibility'
    ]),
    changeMode(mode) {
      this.setEditorMode(mode);
    },
    toggleGrid() {
      this.toggleGridVisibility();
    },
    toggleBackground() {
      this.toggleBackgroundVisibility();
    },
    toggleAvailability() {
      this.toggleAvailabilityVisibility();
    },
    togglePaths() {
      this.togglePathsVisibility();
    },
    toggleObjects() {
      this.toggleObjectsVisibility();
    }
  }
};
</script>

<style scoped>
.tool-panel {
  background: rgba(20, 20, 30, 0.95);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  padding: 15px;
  color: #e0e0e0;
}

.tool-panel-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.mode-switch {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.mode-button {
  flex: 1;
  background: rgba(40, 40, 60, 0.6);
  border: 1px solid rgba(100, 100, 150, 0.4);
  border-radius: 4px;
  padding: 6px 8px;
  color: #e0e0e0;
  font-size: 12px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.mode-button.active {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  color: #00d4ff;
}

.tools-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.tool-button {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(40, 40, 60, 0.6);
  border: 2px solid rgba(100, 100, 150, 0.3);
  border-radius: 6px;
  padding: 10px 12px;
  color: #e0e0e0;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  text-align: left;
}

.tool-button:hover {
  background: rgba(60, 60, 80, 0.8);
  border-color: rgba(0, 212, 255, 0.5);
  transform: translateX(3px);
}

.tool-button.active {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.tool-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.tool-name {
  flex: 1;
  font-weight: 500;
}

.tool-options {
  border-top: 1px solid rgba(100, 100, 150, 0.3);
  padding-top: 15px;
}

.options-title {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.option-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  cursor: pointer;
  user-select: none;
}

.option-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #00d4ff;
}

.option-checkbox span {
  font-size: 14px;
  color: #e0e0e0;
}

.option-checkbox:hover span {
  color: #00d4ff;
}
</style>
