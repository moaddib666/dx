<template>
  <div class="page-container">
    <div class="hero-background"></div>
    <div class="player-home-dashboard">
      <!-- Loading overlay -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <div class="loading-text">Loading dashboard...</div>
        <div class="loading-message">Preparing your adventure</div>
      </div>

      <!-- No Campaigns Available Overlay -->
      <div v-else-if="!hasCampaigns" class="no-campaigns-overlay">
        <div class="no-campaigns-content">
          <div class="warning-icon">⚠️</div>
          <h2 class="warning-title">No Campaigns Available</h2>
          <p class="warning-message">
            You don't have any campaigns available. Please contact a Game Master via Discord to be added to a campaign.
          </p>
          <div class="action-buttons">
            <a href="#" class="discord-button" @click.prevent="openDiscord">
              <span class="discord-icon">
                <svg width="24" height="24" viewBox="0 0 71 55" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M60.1045 4.8978C55.5792 2.8214 50.7265 1.2916 45.6527 0.41542C45.5603 0.39851 45.468 0.440769 45.4204 0.525289C44.7963 1.6353 44.105 3.0834 43.6209 4.2216C38.1637 3.4046 32.7345 3.4046 27.3892 4.2216C26.905 3.0581 26.1886 1.6353 25.5617 0.525289C25.5141 0.443589 25.4218 0.40133 25.3294 0.41542C20.2584 1.2888 15.4057 2.8186 10.8776 4.8978C10.8384 4.9147 10.8048 4.9429 10.7825 4.9795C1.57795 18.7309 -0.943561 32.1443 0.293408 45.3914C0.299005 45.4562 0.335386 45.5182 0.385761 45.5576C6.45866 50.0174 12.3413 52.7249 18.1147 54.5195C18.2071 54.5477 18.305 54.5139 18.3638 54.4378C19.7295 52.5728 20.9469 50.6063 21.9907 48.5383C22.0523 48.4172 21.9935 48.2735 21.8676 48.2256C19.9366 47.4931 18.0979 46.6 16.3292 45.5858C16.1893 45.5041 16.1781 45.304 16.3068 45.2082C16.679 44.9293 17.0513 44.6391 17.4067 44.3461C17.471 44.2926 17.5606 44.2813 17.6362 44.3151C29.2558 49.6202 41.8354 49.6202 53.3179 44.3151C53.3935 44.2785 53.4831 44.2898 53.5502 44.3433C53.9057 44.6363 54.2779 44.9293 54.6529 45.2082C54.7816 45.304 54.7732 45.5041 54.6333 45.5858C52.8646 46.6197 51.0259 47.4931 49.0921 48.2228C48.9662 48.2707 48.9102 48.4172 48.9718 48.5383C50.038 50.6034 51.2554 52.5699 52.5959 54.435C52.6519 54.5139 52.7526 54.5477 52.845 54.5195C58.6464 52.7249 64.529 50.0174 70.6019 45.5576C70.6551 45.5182 70.6887 45.459 70.6943 45.3942C72.1747 30.0791 68.2147 16.7757 60.1968 4.9823C60.1772 4.9429 60.1437 4.9147 60.1045 4.8978ZM23.7259 37.3253C20.2276 37.3253 17.3451 34.1136 17.3451 30.1693C17.3451 26.225 20.1717 23.0133 23.7259 23.0133C27.308 23.0133 30.1626 26.2532 30.1066 30.1693C30.1066 34.1136 27.28 37.3253 23.7259 37.3253ZM47.3178 37.3253C43.8196 37.3253 40.9371 34.1136 40.9371 30.1693C40.9371 26.225 43.7636 23.0133 47.3178 23.0133C50.9 23.0133 53.7545 26.2532 53.6986 30.1693C53.6986 34.1136 50.9 37.3253 47.3178 37.3253Z" fill="#ffffff"/>
                </svg>
              </span>
              Join Discord
            </a>
            <a href="#" class="faq-button" @click.prevent="goToFaq">
              Read FAQ
            </a>
          </div>
        </div>
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
      characters: [],
      hasCampaigns: false
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

        // Check if there are any campaigns available
        this.hasCampaigns = allCampaigns.length > 0;

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
        this.hasCampaigns = false; // No campaigns available on error
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
      // Check if there are any campaigns available
      if (!this.hasCampaigns) {
        // This should not happen as the overlay should block all interactions
        // But as a fallback, redirect to the same page to refresh
        window.location.reload();
        return;
      }

      // Check if a campaign is selected
      if (!this.selectedCampaignId) {
        // Show alert with Discord contact information
        const goToDiscord = confirm('No Campaign Selected\n\nYou need to select a campaign before creating a character. Please contact a Game Master via Discord to be added to a campaign.\n\nClick OK to join our Discord server.');

        if (goToDiscord) {
          // Open Discord link in a new tab
          window.open('https://discord.gg/32dwT8EP', '_blank');
        }
        return;
      }

      // Navigate to the character submission page
      this.$router.push({ name: 'CharacterSubmit' });
    },

    // Method to open Discord in a new tab
    openDiscord() {
      window.open('https://discord.gg/32dwT8EP', '_blank');
    },

    // Method to navigate to FAQ page
    goToFaq() {
      this.$router.push({ path: '/faq' });
    }
  }
};
</script>

<style scoped>
/* Page Container and Background */
.page-container {
  position: relative;
}

.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/dashbaord/dashboard-2.png');
  background-size: cover;
  background-position: center 10%;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

.player-home-dashboard {
  width: 100%;
  max-width: 90vw;
  margin: 0 auto;
  padding: 60px;
  max-height: 80vh;
  min-height: 600px;
  position: relative;
  overflow-y: hidden;
  overflow-x: hidden;
  color: white;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  margin-top: 60px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid transparent;
  border-top: 3px solid var(--cyber-yellow, #ffd700);
  border-right: 3px solid #00ffff;
  border-bottom: 3px solid var(--cyber-yellow, #ffd700);
  border-left: 3px solid #00ffff;
  animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
  box-shadow:
    0 0 15px rgba(255, 215, 0, 0.5),
    0 0 30px rgba(0, 255, 255, 0.3),
    inset 0 0 15px rgba(255, 215, 0, 0.3);
  position: relative;
}

.loading-spinner::before {
  content: '';
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border-radius: 50%;
  border: 1px solid rgba(255, 215, 0, 0.3);
  animation: pulse 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(255, 215, 0, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 215, 0, 0);
  }
}

.loading-text {
  margin-top: 20px;
  font-size: 18px;
  font-weight: 600;
  color: var(--cyber-yellow, #ffd700);
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  letter-spacing: 1px;
  animation: fadeInOut 2s ease-in-out infinite;
}

.loading-message {
  margin-top: 10px;
  font-size: 14px;
  color: #00ffff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
  opacity: 0.8;
  letter-spacing: 0.5px;
  animation: typewriter 4s steps(30, end) infinite;
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid #00ffff;
  max-width: 0;
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

@keyframes typewriter {
  0% { max-width: 0; }
  20% { max-width: 230px; }
  80% { max-width: 230px; }
  100% { max-width: 0; }
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  overflow-x: hidden;
}

/* Top section: Campaign selector */
.campaign-selector-section {
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.section-title {
  font-size: 1.3rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 0.75rem;
  text-align: center;
  font-weight: 600;
}

/* Middle section: Characters */
.characters-section {
  width: 100%;
  overflow-x: hidden;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
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
  gap: 0.75rem;
  margin-bottom: 1.5rem;
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
  background: rgba(45, 45, 45, 0.3);
}

.characters-grid::-webkit-scrollbar-thumb {
  background: rgba(85, 85, 85, 0.5);
  border-radius: 3px;
}

.characters-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 102, 102, 0.7);
}

/* Apply same scrollbar styling to the dashboard */
.player-home-dashboard::-webkit-scrollbar {
  width: 6px;
}

.player-home-dashboard::-webkit-scrollbar-track {
  background: rgba(45, 45, 45, 0.3);
}

.player-home-dashboard::-webkit-scrollbar-thumb {
  background: rgba(85, 85, 85, 0.5);
  border-radius: 3px;
}

.player-home-dashboard::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 102, 102, 0.7);
}

/* No Campaigns Overlay Styles */
.no-campaigns-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  backdrop-filter: blur(3px);
}

.no-campaigns-content {
  max-width: 600px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2.5rem;
  text-align: center;
  border: 1px solid rgba(255, 215, 0, 0.2);
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.warning-icon {
  font-size: 48px;
  margin-bottom: 20px;
  color: var(--cyber-yellow, #ffd700);
}

.warning-title {
  font-size: 24px;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 15px;
  font-weight: 600;
}

.warning-message {
  font-size: 16px;
  color: var(--light-steel-blue, #b0c4de);
  margin-bottom: 25px;
  line-height: 1.5;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  width: 100%;
}

/* Discord button styling */
.discord-button {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: linear-gradient(45deg, var(--cyber-yellow, #ffd700), #00ffff);
  color: #000;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.discord-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
  text-decoration: none;
  color: #000;
}

.discord-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 10px rgba(255, 215, 0, 0.2);
}

/* FAQ button styling */
.faq-button {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  color: var(--cyber-yellow, #ffd700);
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.faq-button:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
  color: white;
  text-decoration: none;
}

.faq-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 5px rgba(255, 215, 0, 0.2);
}

.discord-icon {
  margin-right: 8px;
  display: flex;
  align-items: center;
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
  padding: 0.75rem 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.add-character-placeholder:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.add-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
}

.add-character-placeholder:hover .add-icon {
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
    rgba(255, 215, 0, 0.1),
    transparent,
    rgba(255, 215, 0, 0.1),
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
    rgba(255, 215, 0, 0.3),
    rgba(255, 215, 0, 0.2),
    rgba(255, 215, 0, 0.3)
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
  padding: 0.75rem;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.05);
  color: var(--light-steel-blue, #b0c4de);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
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