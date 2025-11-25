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
  padding: 2rem 0;
}

.faq-item {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border-left: 3px solid #22d3ee;
  transition: all 0.3s ease;
}

.faq-item:hover {
  background: rgba(0, 0, 0, 0.4);
  border-left-color: #06b6d4;
  transform: translateX(4px);
}

.faq-item h3 {
  font-size: 1.5rem;
  color: #22d3ee;
  margin-bottom: 1rem;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.faq-item p {
  font-size: 1.1rem;
  color: #e0f7fa;
  line-height: 1.8;
  font-weight: 400;
}

.guide-link {
  color: #22d3ee;
  text-decoration: none;
  transition: color 0.3s ease;
  font-weight: 500;
  border-bottom: 1px solid transparent;
}

.guide-link:hover {
  color: #06b6d4;
  border-bottom-color: #06b6d4;
}

@media (max-width: 768px) {
  .faq {
    padding: 1.5rem 0;
  }

  .faq-item {
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .faq-item h3 {
    font-size: 1.35rem;
  }

  .faq-item p {
    font-size: 1.05rem;
  }
}

@media (max-width: 480px) {
  .faq {
    padding: 1rem 0;
  }

  .faq-item {
    padding: 1rem;
    margin-bottom: 1.25rem;
  }

  .faq-item h3 {
    font-size: 1.25rem;
  }

  .faq-item p {
    font-size: 1rem;
  }
}
</style>
