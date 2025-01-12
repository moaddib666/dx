<template>
  <div class="modificator-holder">
    <!-- Icon to toggle the modificators -->
    <div
        class="toggle-icon"
        :title="'Show Modificators'"
        @click="toggleList"
    >
      <responsive-mini-icon
          :image-url="icon || null"
          :alt-text="'Modificators'"
          alt="Modificator Icon"
      />
    </div>

    <!-- Dropdown list of modificators -->
    <div
        class="modificator-list"
        v-if="showList"
    >
      <div
          class="modificator"
          v-for="mod in modificators"
          :key="mod.id"
          :title="mod.modificator.description"
      >
        <responsive-mini-icon
            :image-url="mod.modificator.icon || null"
            :alt-text="mod.modificator.name"
        />
        <div class="details">
          <span class="name">{{ mod.modificator.name }}</span>
          <div class="stat-changes">
            <span
                class="stat"
                v-for="(stat, index) in mod.modificator.stat_changes"
                :key="index"
            >
              {{ stat.stat }}: +{{ stat.value }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import ResponsiveMiniIcon from "@/components/icons/ResponsiveMiniIcon.vue";

export default {
  name: "MinimalModificatorHolder",
  components: {
    ResponsiveMiniIcon,
  },
  props: {
    modificators: {
      type: Array,
      required: true,
    },
    icon: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      showList: false,
    };
  },
  methods: {
    toggleList() {
      this.showList = !this.showList;
    },
  },
};
</script>

<style scoped>
.modificator-holder {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
}

.toggle-icon {
  cursor: pointer;
  display: inline-block;
  transition: transform 0.2s ease-in-out;
}

.toggle-icon:hover {
  transform: scale(1.1);
}

.modificator-list {
  position: fixed;
  top: 5rem;
  left: 2.5rem;
  background: rgba(50, 50, 50, 0.9);
  border-radius: 0.3rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 200px;
  z-index: 10;
}

.modificator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem;
  border-radius: 0.3rem;
  background: rgba(255, 255, 255, 0.1);
  transition: background 0.2s ease;
}

.modificator:hover {
  background: rgba(255, 255, 255, 0.2);
}

.details {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.name {
  font-size: 0.9rem;
  font-weight: bold;
  color: white;
}

.stat-changes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem;
  font-size: 0.75rem;
  color: #a4ffb0;
}

.stat {
  background: rgba(100, 100, 100, 0.3);
  padding: 0.2rem 0.4rem;
  border-radius: 0.2rem;
  white-space: nowrap;
}
</style>
