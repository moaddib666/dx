<template>
  <div
    class="campaign-card"
    :class="{
      'inactive': !campaign.is_active,
      'completed': campaign.is_completed
    }"
  >
    <div class="campaign-image" :style="{ backgroundImage: `url(${campaign.background_image})` }"></div>
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
        );
      }
    }
  }
};
</script>

<style scoped>
.campaign-card {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 600px;
  height: 160px;
  margin: 0.5rem;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #444;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  background-color: #2d2d2d; /* Secondary Background */
}

.campaign-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  border-color: #555;
}

.campaign-image {
  width: 160px;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: filter 0.3s ease;
  border-right: 1px solid #444;
}

.campaign-content {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #333; /* Panel Background */
}

.campaign-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1E90FF; /* Accent Color */
}

.campaign-description {
  margin: 0;
  font-size: 0.9rem;
  color: #ccc; /* Secondary Text */
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
  background: #444; /* Element Background */
}

.status-badge.active {
  background-color: rgba(46, 125, 50, 0.2);
  color: #4caf50;
}

.status-badge.inactive {
  background-color: rgba(117, 117, 117, 0.2);
  color: #9e9e9e;
}

.status-badge.completed {
  background-color: rgba(21, 101, 192, 0.2);
  color: #64b5f6;
}

/* Apply blur effect to inactive campaigns */
.campaign-card.inactive .campaign-image {
  filter: blur(3px);
}

/* Apply grayscale effect to completed campaigns */
.campaign-card.completed .campaign-image {
  filter: grayscale(100%);
}

/* Apply both effects if campaign is both inactive and completed */
.campaign-card.inactive.completed .campaign-image {
  filter: blur(3px) grayscale(100%);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .campaign-card {
    height: 140px;
  }

  .campaign-image {
    width: 120px;
  }

  .campaign-title {
    font-size: 1rem;
  }

  .campaign-description {
    font-size: 0.8rem;
    -webkit-line-clamp: 2;
  }
}
</style>