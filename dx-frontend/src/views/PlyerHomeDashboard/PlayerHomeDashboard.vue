<template>
  <div class="player-home-dashboard">
    <!-- Loading overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading dashboard...</div>
    </div>

    <div v-else class="dashboard-content">
      <!-- Top section: Campaign selector with CampaignCardHolder -->
      <section class="campaign-selector-section">
        <h2 class="section-title">Select Campaign</h2>
        <CampaignCardHolder
          :campaigns="campaigns"
          @campaign-selected="selectCampaign"
        />
      </section>

      <!-- Middle section: 90/10 split with characters and selected character info -->
      <section class="characters-section">
        <div class="characters-container">
          <!-- Left side (90%): Available characters -->
          <div class="available-characters">
            <h3 class="subsection-title">Available Characters</h3>
            <div class="characters-grid">
              <!-- Placeholder for character cards -->
              <div class="character-placeholder" v-for="n in 3" :key="n">
                Character {{ n }}
              </div>

              <!-- Placeholder for adding a new character -->
              <div class="add-character-placeholder">
                + Add Character
              </div>
            </div>
          </div>

          <!-- Right side (10%): Selected character info (out of scope for now) -->
          <div class="selected-character-info">
            <h3 class="subsection-title">Selected Character</h3>
            <div class="character-info-placeholder">
              Character details will appear here
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom section: Continue Journey button -->
      <section class="continue-section">
        <LandingButton
          :disabled="!selectedCampaignId || !selectedCharacterId"
          @click="continueJourney"
        >
          Continue Journey
        </LandingButton>
      </section>
    </div>
  </div>
</template>

<script>
import CampaignCardHolder from "@/components/Campaign/CampaignCardHolder.vue";
import LandingButton from "@/components/btn/LandingButton.vue";

export default {
  name: "PlayerHomeDashboard",
  components: {
    CampaignCardHolder,
    LandingButton
  },
  data() {
    return {
      loading: true,
      campaigns: [],
      selectedCampaignId: null,
      selectedCharacterId: null,
      characters: []
    };
  },
  async mounted() {
    try {
      this.loading = true;
      // Fetch campaigns data
      await this.fetchCampaigns();
      // Additional initialization if needed
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async fetchCampaigns() {
      // Mock data for now - would be replaced with actual API call
      this.campaigns = [
        {
          id: "b6de2027-2372-434f-bff4-b799ef5d1cd2",
          name: "First Campaign",
          description: "This is first one",
          is_active: true,
          is_completed: false,
          background_image: "http://localhost:8000/media/campaigns/ele-of-eternity.png"
        },
        {
          id: "c7ef3138-3483-545f-cgg5-c899ef5d2de3",
          name: "Second Campaign",
          description: "The adventure continues",
          is_active: true,
          is_completed: true,
          background_image: "http://localhost:8000/media/campaigns/ele-of-eternity.png"
        },
        {
          id: "d8fg4249-4594-656g-dhh6-d900ef5d3ef4",
          name: "Legacy Campaign",
          description: "An old but gold adventure",
          is_active: false,
          is_completed: false,
          background_image: "http://localhost:8000/media/campaigns/ele-of-eternity.png"
        },
        {
          id: "d8fg4249-4594-656g-dhh6-d900ef5d3ef4",
          name: "Legacy Campaign",
          description: "An old but gold adventure",
          is_active: false,
          is_completed: true,
          background_image: "http://localhost:8000/media/campaigns/ele-of-eternity.png"
        }
      ];
    },
    selectCampaign(campaignId) {
      this.selectedCampaignId = campaignId;
      // Fetch characters for this campaign
      this.fetchCharactersForCampaign(campaignId);
    },
    async fetchCharactersForCampaign(campaignId) {
      // Mock data for now - would be replaced with actual API call
      this.characters = [
        // Character data would go here
      ];
    },
    selectCharacter(characterId) {
      this.selectedCharacterId = characterId;
    },
    continueJourney() {
      if (this.selectedCampaignId && this.selectedCharacterId) {
        // Navigate to game with selected campaign and character
        this.$router.push({
          name: 'Game',
          params: {
            campaignId: this.selectedCampaignId,
            characterId: this.selectedCharacterId
          }
        });
      }
    }
  }
};
</script>

<style scoped>
.player-home-dashboard {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 10px;
  font-size: 16px;
  color: #333;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* Top section: Campaign selector */
.campaign-selector-section {
  width: 100%;
}

.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
  font-weight: 600;
}

/* Middle section: Characters */
.characters-section {
  width: 100%;
}

.characters-container {
  display: flex;
  gap: 20px;
}

.available-characters {
  flex: 9; /* 90% of the space */
}

.selected-character-info {
  flex: 1; /* 10% of the space */
}

.subsection-title {
  font-size: 18px;
  margin-bottom: 15px;
  color: #555;
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.character-placeholder, .add-character-placeholder {
  height: 150px;
  background-color: #f5f5f5;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.character-placeholder:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.add-character-placeholder {
  border: 2px dashed #ccc;
  background-color: transparent;
}

.add-character-placeholder:hover {
  border-color: #3498db;
  color: #3498db;
}

.character-info-placeholder {
  height: 300px;
  background-color: #f5f5f5;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  color: #666;
  padding: 15px;
  text-align: center;
}

/* Bottom section: Continue button */
.continue-section {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .characters-container {
    flex-direction: column;
  }

  .available-characters, .selected-character-info {
    flex: 1 1 100%;
  }

  .characters-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>