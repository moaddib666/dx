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
  background-color: #1e1e1e; /* Primary Background */
  border-radius: 4px;
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
  z-index: 10;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #444; /* Element Background */
  border: 1px solid #555; /* Border Color */
  color: #ffffff; /* Primary Text */
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.nav-arrow:hover:not(:disabled) {
  background-color: #555;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  color: #1E90FF; /* Accent Color */
}

.nav-arrow:disabled {
  background-color: #333;
  color: #666;
  cursor: not-allowed;
  border-color: #444;
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