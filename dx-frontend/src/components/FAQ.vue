<template>
  <section class="faq container">
    <h2>Frequently Asked Questions</h2>
    <div v-for="faq in faqs" :key="faq.question" class="faq-item">
      <h3>{{ faq.question }}</h3>
      <p>{{ faq.answer }}</p>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      faqs: [
        {
          question: 'What is Dimension-X?',
          answer: 'Dimension-X is a game where magic and technology collide, offering players a unique multiverse experience.'
        },
        {
          question: 'How do I start playing?',
          answer: 'Click on the "Play Now" button on the homepage to start your journey.'
        },
        {
          question: 'Can I switch dimensions?',
          answer: 'Yes, you can use the dimension switcher on the landing page to explore different dimensions.'
        }
      ]
    };
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
</style>
