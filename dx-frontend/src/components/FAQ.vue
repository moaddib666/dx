<template>
  <section class="faq container">
    <div v-for="(faq, key) in faqItems" :key="key" class="faq-item">
      <h3>{{ faq.question }}</h3>
      <p v-html="faq.answer"></p>
    </div>
  </section>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
  setup() {
    const { t } = useI18n();

    return { t };
  },
  computed: {
    faqItems() {
      return {
        whatIsDimensionX: {
          question: this.t('faq.questions.whatIsDimensionX.question'),
          answer: this.t('faq.questions.whatIsDimensionX.answer')
        },
        howToStart: {
          question: this.t('faq.questions.howToStart.question'),
          answer: this.t('faq.questions.howToStart.answer')
        },
        canSwitchDimensions: {
          question: this.t('faq.questions.canSwitchDimensions.question'),
          answer: this.t('faq.questions.canSwitchDimensions.answer')
        },
        whoDeveloping: {
          question: this.t('faq.questions.whoDeveloping.question'),
          answer: this.t('faq.questions.whoDeveloping.answer')
        },
        whenAvailable: {
          question: this.t('faq.questions.whenAvailable.question'),
          answer: this.t('faq.questions.whenAvailable.answer')
        },
        provideFeedback: {
          question: this.t('faq.questions.provideFeedback.question'),
          answer: this.t('faq.questions.provideFeedback.answer')
        },
        stayUpdated: {
          question: this.t('faq.questions.stayUpdated.question'),
          answer: this.t('faq.questions.stayUpdated.answer')
        },
        betaTesting: {
          question: this.t('faq.questions.betaTesting.question'),
          answer: this.t('faq.questions.betaTesting.answer')
        },
        platforms: {
          question: this.t('faq.questions.platforms.question'),
          answer: this.t('faq.questions.platforms.answer')
        },
        supportDevelopment: {
          question: this.t('faq.questions.supportDevelopment.question'),
          answer: this.t('faq.questions.supportDevelopment.answer')
        }
      };
    }
  }
};
</script>

<style scoped>
.faq {
  padding: 60px 0;
}

.faq-item {
  margin-bottom: 20px;
}

.faq-item h3 {
  font-size: 24px;
  color: var(--cyber-yellow);
}

.faq-item p {
  font-size: 16px;
  color: var(--light-steel-blue);
}

.guide-link {
  color: var(--cyber-yellow);
  text-decoration: none;
  transition: color 0.3s ease;
}

.guide-link:hover {
  color: white;
  text-decoration: underline;
}
</style>
