<template>
  <div class="page-container">
    <ZoomModal
        :is-visible="isZoomed"
        :image-url="currentZoomedImage"
        @close="closeZoom"
    />
    <HeroBackground @toggle-zoom="toggleZoom" />

    <main class="what-is-it">
      <TitleComponent>{{ t('whatIsIt.title') }}</TitleComponent>
      <p class="subtitle">{{ t('whatIsIt.subtitle') }}</p>



      <IntroductionSection
        :title="t('whatIsIt.introduction.title')"
        :subtitle="t('whatIsIt.introduction.subtitle')"
        :description="t('whatIsIt.introduction.description')"
        :target-audience="t('whatIsIt.introduction.targetAudience')"
        :benefits="t('whatIsIt.introduction.benefits')"
        :main-image="introMainImage"
        :gallery-items="introGalleryItems"
        @toggle-zoom="toggleZoom"
      />

      <RolesSection
        :title="t('whatIsIt.roles.title')"
        :player="playerData"
        :game-master="gameMasterData"
        :tools-gallery-items="toolsGalleryItems"
        @toggle-zoom="toggleZoom"
      />

      <SummarySection
        :title="t('whatIsIt.summary.title')"
        :key-features="keyFeaturesData"
        :getting-started="gettingStartedData"
        :requirements="requirementsData"
        :world-overview="worldOverviewData"
        :inventory-image="inventoryImageData"
        @toggle-zoom="toggleZoom"
      />

      <FooterSection
        :ready-text="t('whatIsIt.footer.readyToBegin')"
        :discord-text="t('whatIsIt.footer.joinDiscord')"
        :discord-link="'https://discord.gg/vC3TvVzK'"
        :additional-links="footerLinks"
      />
    </main>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n';
import TitleComponent from '@/components/TitleComponent.vue';
import HeroBackground from '@/components/WhatIsIt/HeroBackground.vue';
import ZoomModal from '@/components/WhatIsIt/ZoomModal.vue';
import IntroductionSection from '@/components/WhatIsIt/IntroductionSection.vue';
import RolesSection from '@/components/WhatIsIt/RolesSection.vue';
import SummarySection from '@/components/WhatIsIt/SummarySection.vue';
import FooterSection from '@/components/WhatIsIt/FooterSection.vue';

// Import images
import PlayerAreaImg from '@/assets/what-is-it/PlayerArea.png';
import PlayerCharacterCardImg from '@/assets/what-is-it/PlayerCharacterCard.png';
import PlayerActionsImg from '@/assets/what-is-it/PlayerActions.png';
import DiceAreaImg from '@/assets/what-is-it/DiceArea.png';
import GameMasterAreaImg from '@/assets/what-is-it/GameMasterArea.png';
import GameMasterWorldEditImg from '@/assets/what-is-it/GameMasterWorldEdit.png';
import GameMasterWorldEditCharacterInfoImg from '@/assets/what-is-it/GameMasterWorldEditCharacterInfo.png';
import GameMasterCharacterManagemantImg from '@/assets/what-is-it/GameMasterCharacterManagemant.png';
import InventoryItemsImg from '@/assets/what-is-it/InventoryItems.png';

export default {
  name: 'WhatIsIt',
  components: {
    TitleComponent,
    HeroBackground,
    ZoomModal,
    IntroductionSection,
    RolesSection,
    SummarySection,
    FooterSection
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      isZoomed: false,
      currentZoomedImage: '',
      scrollPosition: 0,
      worldOverviewData: null,

      // Introduction section data
      introMainImage: {
        src: PlayerAreaImg,
        alt: 'Player area interface',
        caption: ''
      },
      introGalleryItems: [
        {
          src: PlayerCharacterCardImg,
          alt: 'Player character card',
          caption: 'Character Card'
        },
        {
          src: PlayerActionsImg,
          alt: 'Player actions interface',
          caption: 'Player Actions'
        },
        {
          src: DiceAreaImg,
          alt: 'Dice rolling interface',
          caption: 'Dice Rolling System'
        }
      ],

      // Roles section data
      playerData: {
        title: '',
        description: '',
        responsibilities: '',
        timeCommitment: '',
        gameplay: '',
        progression: '',
        characterCreation: {
          title: '',
          paths: ['', '', '']
        },
        image: {
          src: PlayerCharacterCardImg,
          alt: 'Player character interface'
        }
      },
      gameMasterData: {
        title: '',
        description: '',
        responsibilities: '',
        skillsDeveloped: '',
        timeCommitment: '',
        uniqueAspects: '',
        digitalTools: {
          title: '',
          tools: ['', '', '']
        },
        image: {
          src: GameMasterAreaImg,
          alt: 'Game Master dashboard'
        }
      },
      toolsGalleryItems: [
        {
          src: GameMasterWorldEditImg,
          alt: 'World Editor interface',
          caption: 'World Editor'
        },
        {
          src: GameMasterWorldEditCharacterInfoImg,
          alt: 'Character editing interface',
          caption: 'Character Management'
        },
        {
          src: GameMasterCharacterManagemantImg,
          alt: 'Character management interface',
          caption: 'Character Stats'
        }
      ],

      // Summary section data
      keyFeaturesData: {
        title: '',
        features: ['', '', '', '']
      },
      gettingStartedData: {
        title: '',
        steps: ['', '', '']
      },
      requirementsData: {
        title: '',
        technical: {
          title: '',
          items: ['', '', '']
        },
        personal: {
          title: '',
          items: ['', '', '']
        }
      },
      inventoryImageData: {
        src: InventoryItemsImg,
        alt: 'Inventory system',
        caption: 'Inventory System'
      },

      // Footer section data
      footerLinks: [
        {
          to: '/faq/newcomers-guide',
          text: ''
        },
        {
          to: '/faq/player-cheatsheet',
          text: ''
        }
      ]
    };
  },
  created() {
    // Initialize data that requires translations
    this.introMainImage.caption = this.t('whatIsIt.introduction.imageCaption');

    // Initialize worldOverviewData
    this.worldOverviewData = {
      title: this.t('whatIsIt.summary.worldOverview.title'),
      description: this.t('whatIsIt.summary.worldOverview.description'),
      conflict: {
        title: this.t('whatIsIt.summary.worldOverview.conflict.title'),
        description: this.t('whatIsIt.summary.worldOverview.conflict.description'),
        paths: [
          {
            title: this.t('whatIsIt.summary.worldOverview.conflict.paths.0.title'),
            description: this.t('whatIsIt.summary.worldOverview.conflict.paths.0.description')
          },
          {
            title: this.t('whatIsIt.summary.worldOverview.conflict.paths.1.title'),
            description: this.t('whatIsIt.summary.worldOverview.conflict.paths.1.description')
          }
        ]
      },
      keyPlayers: {
        title: this.t('whatIsIt.summary.worldOverview.keyPlayers.title'),
        players: [
          {
            name: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.0.name'),
            description: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.0.description')
          },
          {
            name: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.1.name'),
            description: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.1.description')
          },
          {
            name: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.2.name'),
            description: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.2.description')
          },
          {
            name: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.3.name'),
            description: this.t('whatIsIt.summary.worldOverview.keyPlayers.players.3.description')
          }
        ]
      },
      worldToday: {
        title: this.t('whatIsIt.summary.worldOverview.worldToday.title'),
        description: this.t('whatIsIt.summary.worldOverview.worldToday.description')
      },
      yourChoice: {
        title: this.t('whatIsIt.summary.worldOverview.yourChoice.title'),
        description: this.t('whatIsIt.summary.worldOverview.yourChoice.description')
      },
      conclusion: this.t('whatIsIt.summary.worldOverview.conclusion')
    };

    // Player data
    this.playerData.title = this.t('whatIsIt.roles.player.title');
    this.playerData.description = this.t('whatIsIt.roles.player.description');
    this.playerData.responsibilities = this.t('whatIsIt.roles.player.responsibilities');
    this.playerData.timeCommitment = this.t('whatIsIt.roles.player.timeCommitment');
    this.playerData.gameplay = this.t('whatIsIt.roles.player.gameplay');
    this.playerData.progression = this.t('whatIsIt.roles.player.progression');
    this.playerData.characterCreation.title = this.t('whatIsIt.roles.player.characterCreation.title');
    this.playerData.characterCreation.paths[0] = this.t('whatIsIt.roles.player.characterCreation.paths.json');
    this.playerData.characterCreation.paths[1] = this.t('whatIsIt.roles.player.characterCreation.paths.john');
    this.playerData.characterCreation.paths[2] = this.t('whatIsIt.roles.player.characterCreation.paths.human');

    // Game Master data
    this.gameMasterData.title = this.t('whatIsIt.roles.gameMaster.title');
    this.gameMasterData.description = this.t('whatIsIt.roles.gameMaster.description');
    this.gameMasterData.responsibilities = this.t('whatIsIt.roles.gameMaster.responsibilities');
    this.gameMasterData.skillsDeveloped = this.t('whatIsIt.roles.gameMaster.skillsDeveloped');
    this.gameMasterData.timeCommitment = this.t('whatIsIt.roles.gameMaster.timeCommitment');
    this.gameMasterData.uniqueAspects = this.t('whatIsIt.roles.gameMaster.uniqueAspects');
    this.gameMasterData.digitalTools.title = this.t('whatIsIt.roles.gameMaster.digitalTools.title');
    this.gameMasterData.digitalTools.tools[0] = this.t('whatIsIt.roles.gameMaster.digitalTools.worldEditor');
    this.gameMasterData.digitalTools.tools[1] = this.t('whatIsIt.roles.gameMaster.digitalTools.characterManagement');
    this.gameMasterData.digitalTools.tools[2] = this.t('whatIsIt.roles.gameMaster.digitalTools.battleSystem');

    // Summary data
    this.keyFeaturesData.title = this.t('whatIsIt.summary.keyFeatures.title');
    this.keyFeaturesData.features[0] = this.t('whatIsIt.summary.keyFeatures.digitalTools');
    this.keyFeaturesData.features[1] = this.t('whatIsIt.summary.keyFeatures.accessibleRules');
    this.keyFeaturesData.features[2] = this.t('whatIsIt.summary.keyFeatures.uniqueSetting');
    this.keyFeaturesData.features[3] = this.t('whatIsIt.summary.keyFeatures.communitySupport');

    this.gettingStartedData.title = this.t('whatIsIt.summary.gettingStarted.title');
    this.gettingStartedData.steps[0] = this.t('whatIsIt.summary.gettingStarted.step1');
    this.gettingStartedData.steps[1] = this.t('whatIsIt.summary.gettingStarted.step2');
    this.gettingStartedData.steps[2] = this.t('whatIsIt.summary.gettingStarted.step3');

    this.requirementsData.title = this.t('whatIsIt.summary.requirements.title');
    this.requirementsData.technical.title = this.t('whatIsIt.summary.requirements.technical.title');
    this.requirementsData.technical.items[0] = this.t('whatIsIt.summary.requirements.technical.computer');
    this.requirementsData.technical.items[1] = this.t('whatIsIt.summary.requirements.technical.browser');
    this.requirementsData.technical.items[2] = this.t('whatIsIt.summary.requirements.technical.discord');
    this.requirementsData.personal.title = this.t('whatIsIt.summary.requirements.personal.title');
    this.requirementsData.personal.items[0] = this.t('whatIsIt.summary.requirements.personal.time');
    this.requirementsData.personal.items[1] = this.t('whatIsIt.summary.requirements.personal.friends');
    this.requirementsData.personal.items[2] = this.t('whatIsIt.summary.requirements.personal.imagination');

    // Footer links
    this.footerLinks[0].text = this.t('whatIsIt.footer.newcomersGuide');
    this.footerLinks[1].text = this.t('whatIsIt.footer.playerCheatSheet');
  },

  methods: {
    toggleZoom(event) {
      // Get the image element from the event
      const imgElement = event.target.tagName === 'IMG' ? event.target : event.target.querySelector('img');

      if (imgElement) {
        // Use the actual resolved src from the DOM
        this.currentZoomedImage = imgElement.src;
        this.isZoomed = true;
        // Store current scroll position
        this.scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        // Prevent body scrolling when modal is open
        document.body.style.overflow = 'hidden';
      } else if (event.target.classList.contains('hero-background')) {
        // Special case for hero background which is a fixed background
        // Get computed style to extract the actual URL
        const style = getComputedStyle(event.target);
        const bgImage = style.backgroundImage;
        // Extract URL from the "url('...')" format
        const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '');
        this.currentZoomedImage = url;
        this.isZoomed = true;
        // Store current scroll position
        this.scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        // Prevent body scrolling when modal is open
        document.body.style.overflow = 'hidden';
      }
    },
    closeZoom() {
      this.isZoomed = false;
      // Re-enable body scrolling
      document.body.style.overflow = '';
      // Restore scroll position
      window.scrollTo(0, this.scrollPosition);
    }
  }
};
</script>

<style scoped>
:root {
  --cyber-yellow: #ffd700;
  --cyber-cyan: #00ffff;
  --light-steel-blue: #b0c4de;
  --dark-overlay: rgba(0, 0, 0, 0.7);
}

.page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.what-is-it {
  padding: 60px;
  color: white;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  padding-top: 120px; /* Changed from margin-top to padding-top for better spacing */
}

.subtitle {
  font-size: 1.2rem;
  color: var(--light-steel-blue);
  font-style: italic;
  text-align: center;
  margin-bottom: 2rem;
}

@media (max-width: 768px) {
  .what-is-it {
    padding: 30px;
    padding-top: 80px; /* Adjusted from margin-top to padding-top */
  }
}

@media (max-width: 480px) {
  .what-is-it {
    padding: 20px;
    padding-top: 60px; /* Adjusted from margin-top to padding-top */
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>