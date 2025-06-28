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
        <CampaignCardHolder
          :campaigns="sortedCampaigns"
          :selectedCampaignId="selectedCampaignId"
          @campaign-selected="selectCampaign"
        />
      </section>

      <!-- Middle section: 90/10 split with characters and selected character info -->
      <section class="characters-section">
        <div class="characters-container">
          <!-- Left side (90%): Available characters -->
          <div class="available-characters">
            <div class="characters-grid">
              <!-- Debug message -->
              <div v-if="characters.length === 0" class="debug-message">
                No characters available. Please select a campaign.
              </div>

              <!-- Debug message showing character count -->
              <div v-else class="debug-message">
                Found {{ characters.length }} characters for the selected campaign.
              </div>

              <!-- Character cards -->
              <div v-for="character in characters" :key="character.id" @click="selectCharacter(character.id)" class="character-card-wrapper">
                <CharacterPreviewCard :character="character" />
              </div>

              <!-- Placeholder for adding a new character -->
              <div class="add-character-placeholder" @click="createCharacter">
                <div class="add-character-content">
                  <div class="add-icon">+</div>
                  <div class="add-text">Add Character</div>
                </div>
                <!-- Flow border effect -->
                <div class="flow-border-add"></div>
                <!-- Hover glow effect -->
                <div class="hover-glow-add"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- No continue button needed as character selection will automatically continue -->
    </div>
  </div>
</template>

<script>
import CampaignCardHolder from "@/components/Campaign/CampaignCardHolder.vue";
import CharacterPreviewCard from "@/components/Character/CharacterPreviewCard.vue";
import ClientManagerService from "@/services/clientManagerService.js";

export default {
  name: "PlayerHomeDashboard",
  components: {
    CampaignCardHolder,
    CharacterPreviewCard
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
  computed: {
    sortedCampaigns() {
      // Sort campaigns by: selected: true, is_active: true, is_completed: false
      return [...this.campaigns].sort((a, b) => {
        // Selected campaigns come first
        if (a.selected && !b.selected) return -1;
        if (!a.selected && b.selected) return 1;

        // Then active campaigns
        if (a.is_active && !b.is_active) return -1;
        if (!a.is_active && b.is_active) return 1;

        // Then incomplete campaigns
        if (!a.is_completed && b.is_completed) return -1;
        if (a.is_completed && !b.is_completed) return 1;

        // If all criteria are equal, sort by name
        return a.name.localeCompare(b.name);
      });
    }
  },
  async mounted() {
    try {
      this.loading = true;
      // Clear the client info cache to ensure fresh data is fetched
      ClientManagerService.clearClientInfoCache();
      // Fetch campaigns data
      await this.fetchCampaigns();
      // Additional initialization if needed

      // For testing, let's automatically select the first campaign
      if (this.campaigns.length > 0) {
        console.log('Auto-selecting first campaign for testing');
        this.selectCampaign(this.campaigns[0].id);
      }
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async fetchCampaigns() {
      try {
        // Get client info from ClientManagerService
        const clientInfo = await ClientManagerService.getCurrentClientInfo();

        // Combine play_campaigns and master_campaigns
        const allCampaigns = [
          ...clientInfo.play_campaigns,
          ...clientInfo.master_campaigns
        ];

        // Remove duplicates (in case a campaign appears in both arrays)
        const uniqueCampaigns = Array.from(new Map(
          allCampaigns.map(campaign => [campaign.id, campaign])
        ).values());

        // Mark the current campaign as selected
        this.campaigns = uniqueCampaigns.map(campaign => ({
          ...campaign,
          selected: campaign.id === clientInfo.current_campaign?.id,
          // Set default values for properties that might not be in the API response
          is_active: campaign.is_active !== undefined ? campaign.is_active : true,
          is_completed: campaign.is_completed !== undefined ? campaign.is_completed : false
        }));

        // If there's a current campaign, set it as selected
        if (clientInfo.current_campaign) {
          this.selectedCampaignId = clientInfo.current_campaign.id;
        }
      } catch (error) {
        console.error("Error fetching campaigns:", error);
        this.campaigns = []; // Set empty array on error
      }
    },
    async selectCampaign(campaignId) {
      console.log('Campaign selected:', campaignId);
      this.selectedCampaignId = campaignId;

      // Update selected status for all campaigns
      this.campaigns.forEach(campaign => {
        campaign.selected = campaign.id === campaignId;
      });

      try {
        // Call the ClientManagerService to set the current campaign
        await ClientManagerService.setCurrentCampaign(campaignId);
      } catch (error) {
        console.error('Error setting current campaign on backend:', error);
      }

      // Fetch characters for this campaign
      this.fetchCharactersForCampaign(campaignId);
    },
    async fetchCharactersForCampaign(campaignId) {
      try {
        console.log('Fetching characters for campaign:', campaignId);

        // Get client info from ClientManagerService
        const clientInfo = await ClientManagerService.getCurrentClientInfo();

        // Filter owned characters to only show those for the selected campaign
        this.characters = clientInfo.owned_characters.filter(character =>
          character.campaign && character.campaign.id === campaignId
        );

        console.log('Characters array after fetch:', this.characters);
      } catch (error) {
        console.error(`Error fetching characters for campaign ${campaignId}:`, error);
        this.characters = []; // Set empty array on error
      }
    },
    async selectCharacter(characterId) {
      try {
        this.loading = true;
        this.selectedCharacterId = characterId;

        // Use the ClientManagerService to select the character
        await ClientManagerService.useCharacter(characterId);

        // Automatically continue journey when character is selected
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
      } catch (error) {
        console.error(`Error selecting character with id ${characterId}:`, error);
        // Show error to user (could be implemented with a toast notification)
      } finally {
        this.loading = false;
      }
    },

    createCharacter() {
      // Navigate to the character submission page
      this.$router.push({ name: 'CharacterSubmit' });
    }
  }
};
</script>

<style scoped>
.player-home-dashboard {
  width: 100%;
  max-width: 90vw;
  margin: 0 auto;
  padding: 20px;
  max-height: 80vh;
  position: relative;
  overflow-y: hidden;
  overflow-x: hidden;
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
  overflow-x: hidden;
}

/* Top section: Campaign selector */
.campaign-selector-section {
  margin-left: 2rem;
  margin-right: 2rem;
}

.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
}

/* Middle section: Characters */
.characters-section {
  width: 100%;
  overflow-x: hidden;
}

.characters-container {
  display: flex;
  gap: 20px;
  overflow-x: hidden;
}

.available-characters {
  flex: 9; /* 90% of the space */
  overflow-x: hidden;
}


.subsection-title {
  font-size: 18px;
  margin-bottom: 15px;
  color: #555;
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
  max-height: 600px;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 10px;
}

/* Scrollbar Styling */
.characters-grid::-webkit-scrollbar {
  width: 6px;
}

.characters-grid::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.characters-grid::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.characters-grid::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Apply same scrollbar styling to the dashboard */
.player-home-dashboard::-webkit-scrollbar {
  width: 6px;
}

.player-home-dashboard::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.player-home-dashboard::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.player-home-dashboard::-webkit-scrollbar-thumb:hover {
  background: #666;
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
  width: 320px;
  height: 200px;
  border-radius: 12px;
  background-color: rgba(10, 10, 10, 0.7);
  border: 1px solid rgba(64, 169, 255, 0.2);
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.add-character-placeholder:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(64, 169, 255, 0.5);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.6),
    0 0 32px rgba(64, 169, 255, 0.3),
    0 0 0 1px rgba(64, 169, 255, 0.4);
}

.add-character-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 16px;
  position: relative;
  z-index: 2;
}

.add-icon {
  font-size: 3rem;
  color: rgba(64, 169, 255, 0.7);
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.add-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.add-character-placeholder:hover .add-icon {
  color: rgba(64, 169, 255, 1);
  transform: scale(1.1);
}

/* Flow border effect for add character placeholder */
.flow-border-add {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  background: linear-gradient(45deg,
    transparent,
    rgba(64, 169, 255, 0.1),
    transparent,
    rgba(138, 43, 226, 0.1),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorderAdd 6s ease-in-out infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.add-character-placeholder:hover .flow-border-add {
  opacity: 1;
}

@keyframes flowBorderAdd {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Hover glow effect for add character placeholder */
.hover-glow-add {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 14px;
  background: linear-gradient(45deg,
    rgba(64, 169, 255, 0.3),
    rgba(138, 43, 226, 0.3),
    rgba(64, 169, 255, 0.3)
  );
  background-size: 300% 300%;
  opacity: 0;
  z-index: -1;
  animation: glowPulseAdd 3s ease-in-out infinite;
  transition: opacity 0.3s ease;
}

.add-character-placeholder:hover .hover-glow-add {
  opacity: 1;
}

@keyframes glowPulseAdd {
  0%, 100% {
    background-position: 0% 50%;
    opacity: 0.5;
  }
  50% {
    background-position: 100% 50%;
    opacity: 0.8;
  }
}

.character-card-wrapper {
  width: 100%;
  height: 100%;
  cursor: pointer;
  padding: 10px;
}

.debug-message {
  grid-column: 1 / -1; /* Span all columns */
  padding: 12px;
  margin-bottom: 15px;
  background-color: #2d2d2d;
  color: #e0e0e0;
  border: 1px solid #444;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.9rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
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

/* No continue button section needed */

/* Responsive adjustments */
@media (max-width: 1200px) {
  .add-character-placeholder {
    width: 300px;
    height: 190px;
  }
}

@media (max-width: 900px) {
  .add-character-placeholder {
    width: 280px;
    height: 180px;
  }

  .add-character-content {
    padding: 14px;
  }

  .add-text {
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .characters-container {
    flex-direction: column;
    overflow-x: hidden;
  }

  .available-characters, .selected-character-info {
    flex: 1 1 100%;
    overflow-x: hidden;
  }

  .characters-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    overflow-x: hidden;
  }

  .add-character-placeholder {
    width: 260px;
    height: 170px;
  }

  .add-character-content {
    padding: 12px;
  }

  .add-text {
    font-size: 1rem;
  }

  .add-icon {
    font-size: 2.5rem;
    margin-bottom: 8px;
  }
}
</style>