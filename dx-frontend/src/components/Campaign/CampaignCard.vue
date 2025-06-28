<template>
  <div
    class="campaign-card"
    :class="{
      'inactive': !campaign.is_active,
      'completed': campaign.is_completed,
      'selected': campaign.selected
    }"
    :style="{ backgroundImage: `url(${campaign.background_image})` }"
  >
    <div class="campaign-overlay">
      <div class="campaign-content">
        <h3 class="campaign-title">{{ campaign.name }}</h3>
        <p class="campaign-description">{{ campaign.description }}</p>
        <div class="campaign-status">
          <span v-if="campaign.is_active" class="status-badge active">Active</span>
          <span v-else class="status-badge inactive">Inactive</span>
          <span v-if="campaign.is_completed" class="status-badge completed">Completed</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CampaignCard",
  props: {
    campaign: {
      type: Object,
      required: true,
      validator: (campaign) => {
        return (
            'id' in campaign &&
            'name' in campaign &&
            'description' in campaign &&
            'is_active' in campaign &&
            'is_completed' in campaign &&
            'background_image' in campaign
            // 'selected' is optional
        );
      }
    }
  }
};
</script>

<style scoped>
.campaign-card {
  position: relative;
  width: 300px;
  height: 160px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #444;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.campaign-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  border-color: #555;
}

.campaign-overlay {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right,
  rgba(0, 0, 0, 0.1) 0%,
  rgba(0, 0, 0, 0.6) 50%,
  rgba(0, 0, 0, 0.8) 100%);
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.campaign-content {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.campaign-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
}

.campaign-description {
  margin: 0;
  font-size: 0.9rem;
  color: #e0e0e0;
  flex-grow: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.campaign-status {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  background: rgba(0, 0, 0, 0.5);
}

.status-badge.active {
  background-color: rgba(76, 175, 80, 0.7);
  color: #ffffff;
}

.status-badge.inactive {
  background-color: rgba(158, 158, 158, 0.7);
  color: #ffffff;
}

.status-badge.completed {
  background-color: rgba(30, 144, 255, 0.7);
  color: #ffffff;
}

/* Apply blur effect to inactive campaigns */
.campaign-card.inactive {
  filter: blur(2px);
}

/* Apply grayscale effect to completed campaigns */
.campaign-card.completed {
  filter: grayscale(70%);
}

/* Apply both effects if campaign is both inactive and completed */
.campaign-card.inactive.completed {
  filter: blur(2px) grayscale(70%);
}

/* Selected campaign styling */
.campaign-card.selected {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(52, 152, 219, 0.8);
  z-index: 10;
}

.campaign-card.selected .campaign-overlay {
  background: linear-gradient(to right,
  rgba(0, 0, 0, 0.1) 0%,
  rgba(0, 0, 0, 0.5) 50%,
  rgba(52, 152, 219, 0.4) 100%);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .campaign-card {
    width: 280px;
  }

  .campaign-content {
    width: 70%;
  }
}

@media (max-width: 900px) {
  .campaign-card {
    width: 260px;
  }

  .campaign-content {
    width: 75%;
  }
}

@media (max-width: 768px) {
  .campaign-card {
    width: 240px;
    height: 140px;
  }

  .campaign-content {
    width: 70%;
  }

  .campaign-title {
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }

  .campaign-description {
    font-size: 0.8rem;
    -webkit-line-clamp: 2;
  }

  .campaign-status {
    margin-top: 0.5rem;
  }

  .status-badge {
    padding: 0.15rem 0.35rem;
    font-size: 0.7rem;
  }
}
</style>