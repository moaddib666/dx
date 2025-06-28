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
              <div class="add-character-placeholder">
                + Add Character
              </div>
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
import CharacterPreviewCard from "@/components/Character/CharacterPreviewCard.vue";

export default {
  name: "PlayerHomeDashboard",
  components: {
    CampaignCardHolder,
    LandingButton,
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
  async mounted() {
    try {
      this.loading = true;
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
      console.log('Campaign selected:', campaignId);
      this.selectedCampaignId = campaignId;
      // Fetch characters for this campaign
      this.fetchCharactersForCampaign(campaignId);
    },
    async fetchCharactersForCampaign(campaignId) {
      // Mock data for now - would be replaced with actual API call
      console.log('Fetching characters for campaign:', campaignId);
      this.characters = [
        {
          "id": "f3c4216f-cbaa-4792-b6e6-1cedd502defe",
          "name": "The Veiled Arbiter",
          "biography": {
            "id": "012e5d6e-bad2-459c-a7a6-62329ecd7508",
            "created_at": "2024-12-24T14:18:04.753000Z",
            "updated_at": "2024-12-24T14:19:28.959000Z",
            "age": 900,
            "gender": "Other",
            "background": "The Veiled Arbiter exists beyond the bounds of mortal realms, serving as the omniscient overseer of the game world. It appears to inspect, guide, or intervene when the balance of Flow or the integrity of the realm is threatened.",
            "appearance": "A translucent figure cloaked in flowing, dark robes inscribed with glowing blue and silver symbols. Its hood obscures its face, revealing only glowing white eyes.",
            "avatar": "http://localhost:8000/media/avatars/83A73E18-2066-4263-B8F3-F299660160F4.PNG",
            "character": "f3c4216f-cbaa-4792-b6e6-1cedd502defe"
          },
          "npc": false,
          "rank": {
            "name": "Mythical Paragon",
            "grade": 2,
            "experience_needed": 284460
          },
          "path": {
            "name": "Path of JSon",
            "description": "A path focusing on magical abilities.",
            "icon": "http://localhost:8000/media/icons/path/json.webp",
            "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
          },
          "experience": 0,
          "tags": [
            "Game Master",
            "Phantom",
            "Flow Manipulator"
          ],
          "resetting_base_stats": false,
          "is_active": true,
          "campaign": {
            "id": campaignId,
            "name": "First Campaign"
          }
        },
        {
          "id": "a1b2c3d4-e5f6-4792-b6e6-1cedd502defe",
          "name": "Shadow Walker",
          "biography": {
            "id": "e5f6g7h8-i9j0-459c-a7a6-62329ecd7508",
            "created_at": "2024-12-24T14:18:04.753000Z",
            "updated_at": "2024-12-24T14:19:28.959000Z",
            "age": 35,
            "gender": "Female",
            "background": "A mysterious assassin who moves between shadows, Shadow Walker has a dark past and seeks redemption through her adventures. She is known for her stealth and precision.",
            "appearance": "A slender figure dressed in dark leather armor with a hood that partially obscures her face. Her eyes glow with a faint purple light.",
            "avatar": "http://localhost:8000/media/avatars/shadow-walker.PNG",
            "character": "a1b2c3d4-e5f6-4792-b6e6-1cedd502defe"
          },
          "npc": false,
          "rank": {
            "name": "Elite Adventurer",
            "grade": 3,
            "experience_needed": 150000
          },
          "path": {
            "name": "Path of Shadows",
            "description": "A path focusing on stealth and assassination.",
            "icon": "http://localhost:8000/media/icons/path/shadow.webp",
            "id": "8a9b0c1d-2e3f-4g5h-6i7j-8k9l0m1n2o3p"
          },
          "experience": 75000,
          "tags": [
            "Assassin",
            "Rogue",
            "Shadow Magic"
          ],
          "resetting_base_stats": false,
          "is_active": true,
          "campaign": {
            "id": campaignId,
            "name": "First Campaign"
          }
        },
        {
          "id": "q1w2e3r4-t5y6-7u8i-9o0p-a1s2d3f4g5h6",
          "name": "Eldrin Lightbringer",
          "biography": {
            "id": "j1k2l3m4-n5o6-p7q8-r9s0-t1u2v3w4x5y6",
            "created_at": "2024-12-24T14:18:04.753000Z",
            "updated_at": "2024-12-24T14:19:28.959000Z",
            "age": 150,
            "gender": "Male",
            "background": "An ancient elf who has dedicated his life to fighting darkness and spreading light. Eldrin is a powerful healer and a beacon of hope in dark times.",
            "appearance": "A tall, slender elf with long silver hair and glowing golden eyes. He wears white and gold robes adorned with symbols of the sun.",
            "avatar": "http://localhost:8000/media/avatars/eldrin.PNG",
            "character": "q1w2e3r4-t5y6-7u8i-9o0p-a1s2d3f4g5h6"
          },
          "npc": false,
          "rank": {
            "name": "Legendary Hero",
            "grade": 1,
            "experience_needed": 500000
          },
          "path": {
            "name": "Path of Light",
            "description": "A path focusing on healing and light magic.",
            "icon": "http://localhost:8000/media/icons/path/light.webp",
            "id": "z1x2c3v4-b5n6-m7a8-s9d0-f1g2h3j4k5l6"
          },
          "experience": 450000,
          "tags": [
            "Healer",
            "Light Magic",
            "Ancient Elf"
          ],
          "resetting_base_stats": false,
          "is_active": false,
          "campaign": {
            "id": campaignId,
            "name": "First Campaign"
          }
        }
      ];
      console.log('Characters array after fetch:', this.characters);
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

.character-card-wrapper {
  width: 100%;
  height: 100%;
  cursor: pointer;
  padding: 10px;
}

.debug-message {
  grid-column: 1 / -1; /* Span all columns */
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  font-weight: bold;
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