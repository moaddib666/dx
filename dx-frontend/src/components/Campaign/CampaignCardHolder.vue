<template>
  <div class="campaign-card-holder">
    <!-- Navigation arrows -->
    <button
      v-if="campaigns.length > visibleCards"
      class="nav-arrow left-arrow"
      @click="scrollLeft"
      :disabled="startIndex === 0"
    >
      &lt;
    </button>

    <!-- Cards container with horizontal scrolling -->
    <div class="cards-container" ref="cardsContainer">
      <div
        v-for="(campaign, index) in visibleCampaigns"
        :key="campaign.id"
        class="card-wrapper"
        @click="selectCampaign(campaign.id)"
      >
        <CampaignCard :campaign="campaign" />
      </div>
    </div>

    <!-- Right navigation arrow -->
    <button
      v-if="campaigns.length > visibleCards"
      class="nav-arrow right-arrow"
      @click="scrollRight"
      :disabled="startIndex >= campaigns.length - visibleCards"
    >
      &gt;
    </button>
  </div>
</template>

<script>
import CampaignCard from './CampaignCard.vue';

export default {
  name: "CampaignCardHolder",
  components: {
    CampaignCard
  },
  props: {
    campaigns: {
      type: Array,
      required: true,
      default: () => []
    },
    selectedCampaignId: {
      type: String,
      default: null
    },
    visibleCards: {
      type: Number,
      default: 3
    }
  },
  data() {
    return {
      startIndex: 0
    };
  },
  watch: {
    selectedCampaignId: {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.scrollToSelectedCampaign(newId);
        }
      }
    }
  },
  computed: {
    visibleCampaigns() {
      return this.campaigns.slice(this.startIndex, this.startIndex + this.visibleCards);
    }
  },
  methods: {
    scrollLeft() {
      if (this.startIndex > 0) {
        this.startIndex--;
      }
    },
    scrollRight() {
      if (this.startIndex < this.campaigns.length - this.visibleCards) {
        this.startIndex++;
      }
    },
    scrollToSelectedCampaign(campaignId) {
      // Find the index of the selected campaign
      const selectedIndex = this.campaigns.findIndex(campaign => campaign.id === campaignId);

      // If found, adjust startIndex to make it visible
      if (selectedIndex !== -1) {
        // If the selected campaign is before the current visible range
        if (selectedIndex < this.startIndex) {
          this.startIndex = selectedIndex;
        }
        // If the selected campaign is after the current visible range
        else if (selectedIndex >= this.startIndex + this.visibleCards) {
          // Set startIndex so that the selected campaign is the last visible one
          this.startIndex = Math.max(0, selectedIndex - this.visibleCards + 1);
        }
        // If it's already visible, no need to change startIndex
      }
    },
    selectCampaign(campaignId) {
      this.$emit('campaign-selected', campaignId);
    }
  }
};
</script>

<style scoped>
.campaign-card-holder {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 100%;
  padding: 1rem 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.cards-container {
  display: flex;
  flex-direction: row;
  overflow-x: hidden;
  scroll-behavior: smooth;
  width: 100%;
  gap: 1rem;
  padding: 0.5rem 0;
  justify-content: center;
}

.card-wrapper {
  flex: 0 0 auto;
  transition: transform 0.3s ease;
  cursor: pointer;
  margin: 0 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-wrapper:hover {
  transform: scale(1.02);
}

.nav-arrow {
  position: absolute;
  z-index: 100;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
  color: #ffffff;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-arrow:hover:not(:disabled) {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  transform: translateY(-2px);
}

.nav-arrow:disabled {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.3);
  cursor: not-allowed;
  border-color: rgba(255, 255, 255, 0.1);
}

.left-arrow {
  left: -20px;
}

.right-arrow {
  right: -20px;
}

/* Animation for arrows */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.nav-arrow:not(:disabled):hover {
  animation: pulse 1s ease-in-out infinite;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .cards-container {
    gap: 0.75rem;
  }

  .card-wrapper {
    margin: 0 0.4rem;
  }
}

@media (max-width: 900px) {
  .campaign-card-holder {
    padding: 0.75rem 0;
  }

  .card-wrapper {
    margin: 0 0.3rem;
  }
}

@media (max-width: 768px) {
  .nav-arrow {
    width: 30px;
    height: 30px;
    font-size: 14px;
  }

  .left-arrow {
    left: -15px;
  }

  .right-arrow {
    right: -15px;
  }

  .cards-container {
    gap: 0.5rem;
  }

  .card-wrapper {
    margin: 0 0.25rem;
  }
}
</style>