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

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import TitleComponent from '@/components/TitleComponent.vue'
import HeroBackground from '@/components/WhatIsIt/HeroBackground.vue'
import ZoomModal from '@/components/WhatIsIt/ZoomModal.vue'
import IntroductionSection from '@/components/WhatIsIt/IntroductionSection.vue'
import RolesSection from '@/components/WhatIsIt/RolesSection.vue'
import SummarySection from '@/components/WhatIsIt/SummarySection.vue'
import FooterSection from '@/components/WhatIsIt/FooterSection.vue'

import PlayerAreaImg from '@/assets/what-is-it/PlayerArea.png'
import PlayerCharacterCardImg from '@/assets/what-is-it/PlayerCharacterCard.png'
import PlayerActionsImg from '@/assets/what-is-it/PlayerActions.png'
import DiceAreaImg from '@/assets/what-is-it/DiceArea.png'
import GameMasterAreaImg from '@/assets/what-is-it/GameMasterArea.png'
import GameMasterWorldEditImg from '@/assets/what-is-it/GameMasterWorldEdit.png'
import GameMasterWorldEditCharacterInfoImg from '@/assets/what-is-it/GameMasterWorldEditCharacterInfo.png'
import GameMasterCharacterManagemantImg from '@/assets/what-is-it/GameMasterCharacterManagemant.png'
import InventoryItemsImg from '@/assets/what-is-it/InventoryItems.png'

interface ImageData {
  src: string
  alt: string
  caption: string
}

interface CharacterCreation {
  title: string
  paths: string[]
}

interface DigitalTools {
  title: string
  tools: string[]
}

interface PlayerData {
  title: string
  description: string
  responsibilities: string
  timeCommitment: string
  gameplay: string
  progression: string
  characterCreation: CharacterCreation
  image: Omit<ImageData, 'caption'>
}

interface GameMasterData {
  title: string
  description: string
  responsibilities: string
  skillsDeveloped: string
  timeCommitment: string
  uniqueAspects: string
  digitalTools: DigitalTools
  image: Omit<ImageData, 'caption'>
}

interface KeyFeaturesData {
  title: string
  features: string[]
}

interface GettingStartedData {
  title: string
  steps: string[]
}

interface RequirementsData {
  title: string
  technical: {
    title: string
    items: string[]
  }
  personal: {
    title: string
    items: string[]
  }
}

interface ConflictPath {
  title: string
  description: string
}

interface KeyPlayer {
  name: string
  description: string
}

interface WorldOverviewData {
  title: string
  description: string
  conflict: {
    title: string
    description: string
    paths: ConflictPath[]
  }
  keyPlayers: {
    title: string
    players: KeyPlayer[]
  }
  worldToday: {
    title: string
    description: string
  }
  yourChoice: {
    title: string
    description: string
  }
  conclusion: string
}

interface FooterLink {
  to: string
  text: string
}

const { t } = useI18n()

const isZoomed = ref(false)
const currentZoomedImage = ref('')
const scrollPosition = ref(0)

// Introduction section data
const introMainImage = computed<ImageData>(() => ({
  src: PlayerAreaImg,
  alt: 'Player area interface',
  caption: t('whatIsIt.introduction.imageCaption')
}))

const introGalleryItems: ImageData[] = [
  {
    src: PlayerCharacterCardImg,
    alt: 'Player character card',
    caption: 'Character Card'
  },
  {
    src: DiceAreaImg,
    alt: 'Dice rolling interface',
    caption: 'Dice Rolling System'
  }
]

// Roles section data
const playerData = computed<PlayerData>(() => ({
  title: t('whatIsIt.roles.player.title'),
  description: t('whatIsIt.roles.player.description'),
  responsibilities: t('whatIsIt.roles.player.responsibilities'),
  timeCommitment: t('whatIsIt.roles.player.timeCommitment'),
  gameplay: t('whatIsIt.roles.player.gameplay'),
  progression: t('whatIsIt.roles.player.progression'),
  characterCreation: {
    title: t('whatIsIt.roles.player.characterCreation.title'),
    paths: [
      t('whatIsIt.roles.player.characterCreation.paths.json'),
      t('whatIsIt.roles.player.characterCreation.paths.john'),
      t('whatIsIt.roles.player.characterCreation.paths.human')
    ]
  },
  image: {
    src: PlayerCharacterCardImg,
    alt: 'Player character interface'
  }
}))

const gameMasterData = computed<GameMasterData>(() => ({
  title: t('whatIsIt.roles.gameMaster.title'),
  description: t('whatIsIt.roles.gameMaster.description'),
  responsibilities: t('whatIsIt.roles.gameMaster.responsibilities'),
  skillsDeveloped: t('whatIsIt.roles.gameMaster.skillsDeveloped'),
  timeCommitment: t('whatIsIt.roles.gameMaster.timeCommitment'),
  uniqueAspects: t('whatIsIt.roles.gameMaster.uniqueAspects'),
  digitalTools: {
    title: t('whatIsIt.roles.gameMaster.digitalTools.title'),
    tools: [
      t('whatIsIt.roles.gameMaster.digitalTools.worldEditor'),
      t('whatIsIt.roles.gameMaster.digitalTools.characterManagement'),
      t('whatIsIt.roles.gameMaster.digitalTools.battleSystem')
    ]
  },
  image: {
    src: GameMasterAreaImg,
    alt: 'Game Master dashboard'
  }
}))

const toolsGalleryItems: ImageData[] = [
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
]

// Summary section data
const keyFeaturesData = computed<KeyFeaturesData>(() => ({
  title: t('whatIsIt.summary.keyFeatures.title'),
  features: [
    t('whatIsIt.summary.keyFeatures.digitalTools'),
    t('whatIsIt.summary.keyFeatures.accessibleRules'),
    t('whatIsIt.summary.keyFeatures.uniqueSetting'),
    t('whatIsIt.summary.keyFeatures.communitySupport')
  ]
}))

const gettingStartedData = computed<GettingStartedData>(() => ({
  title: t('whatIsIt.summary.gettingStarted.title'),
  steps: [
    t('whatIsIt.summary.gettingStarted.step1'),
    t('whatIsIt.summary.gettingStarted.step2'),
    t('whatIsIt.summary.gettingStarted.step3')
  ]
}))

const requirementsData = computed<RequirementsData>(() => ({
  title: t('whatIsIt.summary.requirements.title'),
  technical: {
    title: t('whatIsIt.summary.requirements.technical.title'),
    items: [
      t('whatIsIt.summary.requirements.technical.computer'),
      t('whatIsIt.summary.requirements.technical.browser'),
      t('whatIsIt.summary.requirements.technical.discord')
    ]
  },
  personal: {
    title: t('whatIsIt.summary.requirements.personal.title'),
    items: [
      t('whatIsIt.summary.requirements.personal.time'),
      t('whatIsIt.summary.requirements.personal.friends'),
      t('whatIsIt.summary.requirements.personal.imagination')
    ]
  }
}))

const worldOverviewData = computed<WorldOverviewData>(() => ({
  title: t('whatIsIt.summary.worldOverview.title'),
  description: t('whatIsIt.summary.worldOverview.description'),
  conflict: {
    title: t('whatIsIt.summary.worldOverview.conflict.title'),
    description: t('whatIsIt.summary.worldOverview.conflict.description'),
    paths: [
      {
        title: t('whatIsIt.summary.worldOverview.conflict.paths.0.title'),
        description: t('whatIsIt.summary.worldOverview.conflict.paths.0.description')
      },
      {
        title: t('whatIsIt.summary.worldOverview.conflict.paths.1.title'),
        description: t('whatIsIt.summary.worldOverview.conflict.paths.1.description')
      }
    ]
  },
  keyPlayers: {
    title: t('whatIsIt.summary.worldOverview.keyPlayers.title'),
    players: [
      {
        name: t('whatIsIt.summary.worldOverview.keyPlayers.players.0.name'),
        description: t('whatIsIt.summary.worldOverview.keyPlayers.players.0.description')
      },
      {
        name: t('whatIsIt.summary.worldOverview.keyPlayers.players.1.name'),
        description: t('whatIsIt.summary.worldOverview.keyPlayers.players.1.description')
      },
      {
        name: t('whatIsIt.summary.worldOverview.keyPlayers.players.2.name'),
        description: t('whatIsIt.summary.worldOverview.keyPlayers.players.2.description')
      },
      {
        name: t('whatIsIt.summary.worldOverview.keyPlayers.players.3.name'),
        description: t('whatIsIt.summary.worldOverview.keyPlayers.players.3.description')
      }
    ]
  },
  worldToday: {
    title: t('whatIsIt.summary.worldOverview.worldToday.title'),
    description: t('whatIsIt.summary.worldOverview.worldToday.description')
  },
  yourChoice: {
    title: t('whatIsIt.summary.worldOverview.yourChoice.title'),
    description: t('whatIsIt.summary.worldOverview.yourChoice.description')
  },
  conclusion: t('whatIsIt.summary.worldOverview.conclusion')
}))

const inventoryImageData: ImageData = {
  src: InventoryItemsImg,
  alt: 'Inventory system',
  caption: 'Inventory System'
}

// Footer section data
const footerLinks = computed<FooterLink[]>(() => [
  {
    to: '/faq/newcomers-guide',
    text: t('whatIsIt.footer.newcomersGuide')
  },
  {
    to: '/faq/player-cheatsheet',
    text: t('whatIsIt.footer.playerCheatSheet')
  }
])

function toggleZoom(event: Event) {
  const target = event.target as HTMLElement
  const imgElement = target.tagName === 'IMG' ? target as HTMLImageElement : target.querySelector('img')

  if (imgElement) {
    currentZoomedImage.value = imgElement.src
    isZoomed.value = true
    scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
    document.body.style.overflow = 'hidden'
  } else if (target.classList.contains('hero-background')) {
    const style = getComputedStyle(target)
    const bgImage = style.backgroundImage
    const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '')
    currentZoomedImage.value = url
    isZoomed.value = true
    scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
    document.body.style.overflow = 'hidden'
  }
}

function closeZoom() {
  isZoomed.value = false
  document.body.style.overflow = ''
  window.scrollTo(0, scrollPosition.value)
}
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
}

.what-is-it {
  max-width: 1400px;
  width: 100%;
  padding: 1rem;
  color: #b7f9ff;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  margin: 0 auto;
}

.subtitle {
  font-size: 1.2rem;
  color: #9feaff;
  font-style: italic;
  text-align: center;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

@media (max-width: 1024px) {
  .what-is-it {
    max-width: 100%;
    padding: 1rem;
    padding-top: 70px;
  }
}

@media (max-width: 768px) {
  .what-is-it {
    padding: 1rem;
    padding-top: 60px;
  }

  .subtitle {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }
}

@media (max-width: 480px) {
  .what-is-it {
    padding: 1rem 0.75rem;
    padding-top: 50px;
  }

  .subtitle {
    font-size: 1rem;
    margin-bottom: 1rem;
  }
}
</style>