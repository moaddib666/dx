<template>
  <div class="character-template-detail">
    <!-- Tab Navigation -->
    <div class="tab-navigation">
      <div
        v-for="(tab, index) in tabs"
        :key="index"
        :class="['tab', { active: currentTab === index }]"
        @click="goToTab(index)"
      >
        <span class="tab-label">{{ tab.label }}</span>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <component
        :is="tabs[currentTab].component"
        v-if="tabs[currentTab] && tabs[currentTab].component"
        v-bind="tabs[currentTab].data"
        @update="onTemplateUpdate"
      />
    </div>
  </div>
</template>

<script>
import BasicInfoTab from './tabs/BasicInfoTab.vue';
import StatsTab from './tabs/StatsTab.vue';
import BioTab from './tabs/BioTab.vue';
import EquipmentTab from './tabs/EquipmentTab.vue';
import AbilitiesTab from './tabs/AbilitiesTab.vue';

export default {
  name: 'CharacterTemplateDetail',
  components: {
    BasicInfoTab,
    StatsTab,
    BioTab,
    EquipmentTab,
    AbilitiesTab
  },
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      currentTab: 0
    };
  },
  computed: {
    tabs() {
      return [
        {
          label: "Basic Info",
          component: BasicInfoTab,
          data: {
            template: this.template,
            service: this.service
          }
        },
        {
          label: "Stats",
          component: StatsTab,
          data: {
            template: this.template,
            service: this.service
          }
        },
        {
          label: "Bio",
          component: BioTab,
          data: {
            template: this.template,
            service: this.service
          }
        },
        {
          label: "Equipment",
          component: EquipmentTab,
          data: {
            template: this.template,
            service: this.service
          }
        },
        {
          label: "Abilities",
          component: AbilitiesTab,
          data: {
            template: this.template,
            service: this.service
          }
        }
      ];
    }
  },
  methods: {
    goToTab(index) {
      if (index >= 0 && index < this.tabs.length) {
        this.currentTab = index;
      }
    },
    onTemplateUpdate(data) {
      this.$emit('update', data);
    }
  }
};
</script>

<style scoped>
.character-template-detail {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* Tab Navigation */
.tab-navigation {
  display: flex;
  background-color: #2d2d2d;
  border-bottom: 1px solid #444;
  margin-bottom: 20px;
}

.tab {
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
  color: #ccc;
}

.tab:hover {
  background-color: #3a3a3a;
  color: #fff;
}

.tab.active {
  background-color: #1E90FF;
  color: #fff;
  border-bottom-color: #1E90FF;
}

.tab-label {
  font-size: 14px;
  font-weight: 500;
}

/* Tab Content */
.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 20px;
}
</style>