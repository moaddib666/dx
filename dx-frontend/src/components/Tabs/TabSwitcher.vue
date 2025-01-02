<template>
  <div class="tab-switcher">
    <!-- Tab Header -->
    <div class="tab-buttons">
      <button
          v-for="(tab, index) in tabs"
          :key="index"
          :class="['tab-button', { active: activeTabId === tab.id }]"
          @click="switchTab(tab.id)"
      >
        {{ tab.name }}
      </button>
      <!-- Active Tab Indicator -->
      <div
          class="tab-indicator"
          :style="{ width: indicatorWidth, left: indicatorLeft }"
      ></div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <slot :tabId="activeTabId"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "TabSwitcher",
  props: {
    tabs: {
      type: Array,
      required: true, // Expects an array of tabs [{ id: 'itemSelector', name: 'Items' }, { id: 'skillSelector', name: 'Skills' }]
    },
    initialTabId: {
      type: String,
      default: null, // Sets the initial active tab
    },
  },
  data() {
    return {
      activeTabId: this.initialTabId || (this.tabs[0] && this.tabs[0].id), // Default to the first tab if no initialTabId is provided
    };
  },
  computed: {
    indicatorWidth() {
      const activeTab = this.$refs.tabs?.querySelector(".tab-button.active");
      return activeTab ? `${activeTab.offsetWidth}px` : "0px";
    },
    indicatorLeft() {
      const activeTab = this.$refs.tabs?.querySelector(".tab-button.active");
      return activeTab ? `${activeTab.offsetLeft}px` : "0px";
    },
  },
  methods: {
    switchTab(tabId) {
      this.activeTabId = tabId;
      this.$emit("tab-switched", tabId); // Emit the active tab ID to the parent
    },
  },
};
</script>

<style scoped>
.tab-switcher {
  display: flex;
  flex-direction: column;
}

.tab-buttons {
  display: flex;
  position: relative;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.tab-button {
  flex: 1;
  padding: 0.5rem;
  text-align: center;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  position: relative;
  z-index: 1;
  transition: color 0.2s ease;
}

.tab-button:hover {
  color: #00e5ff;
}

.tab-button.active {
  color: #00e5ff;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  height: 3px;
  background: #00e5ff;
  border-radius: 3px;
  transition: width 0.3s ease, left 0.3s ease;
  z-index: 0;
}

.tab-content {
  margin-top: 1rem;
}
</style>
