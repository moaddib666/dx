<template>
  <div class="page-container">
    <HeroBackground id="background"></HeroBackground>
    <main class="faq">
      <TitleComponent>{{ t('faq.title') }}</TitleComponent>
      <p class="faq-description">{{ t('faq.description') }}</p>
      <f-a-q></f-a-q>
    </main>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';
import FAQ from '@/components/FAQ.vue';
import HeroBackground from '@/components/WhatIsIt/HeroBackground.vue';
import { useI18n } from 'vue-i18n';

export default {
  components: {
    FAQ,
    TitleComponent,
    HeroBackground
  },
  setup() {
    const { t } = useI18n();
    return { t };
  }
};
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

/* Ensure the background component uses a custom image from common directory */
#background {
  background-image: url('@/assets/images/backgrounds/common/moaddib_Cinematic_wide_shot_of_a_futuristic_cyberpunk-fantasy_23d0abcd-0f8e-4edc-84ab-63db431446f6_2.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.faq {
  max-width: 1200px;
  width: 100%;
  padding: 3rem 2rem;
  color: #e0f7fa;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(2px);
  margin: 0 auto;
  border-radius: 12px;
}

.faq-description {
  font-size: 1.2rem;
  line-height: 1.7;
  color: #b0e7f0;
  text-align: center;
  margin-bottom: 2.5rem;
  margin-top: 1rem;
  font-weight: 400;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 1024px) {
  .faq {
    max-width: 100%;
    padding: 2.5rem 1.5rem;
    padding-top: 80px;
  }

  .faq-description {
    font-size: 1.15rem;
    margin-bottom: 2rem;
  }
}

@media (max-width: 768px) {
  .faq {
    padding: 2rem 1.25rem;
    padding-top: 70px;
  }

  .faq-description {
    font-size: 1.1rem;
    margin-bottom: 1.75rem;
  }
}

@media (max-width: 480px) {
  .faq {
    padding: 1.5rem 1rem;
    padding-top: 60px;
  }

  .faq-description {
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
  }
}
</style>
