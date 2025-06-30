<template>
  <section class="faq container">
    <div v-for="faq in faqs" :key="faq.question" class="faq-item">
      <h3>{{ faq.question }}</h3>
      <p v-html="faq.answer"></p>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      "faqs": [
        {
          "question": "What is Dimension-X?",
          "answer": "Dimension-X is a game where magic and technology collide, offering players a unique multiverse experience."
        },
        {
          "question": "How do I start playing?",
          "answer": "The game is not yet ready for play. However, you can check our <a href='/newcomers-guide' class='guide-link'>Newcomer's Guide</a> for detailed information on how to get started once the game launches. You can also interact with a well-trained AI or contact the creator for further communication."
        },
        {
          "question": "Can I switch dimensions?",
          "answer": "Dimension switching will be a feature in the game, allowing players to explore different dimensions once the game is launched."
        },
        {
          "question": "Who is developing Dimension-X?",
          "answer": "Dimension-X is being developed by a single person who is passionate about creating immersive game experiences."
        },
        {
          "question": "When will Dimension-X be available?",
          "answer": "The release date is not yet set. Stay tuned for updates by subscribing to our newsletter or following us on social media."
        },
        {
          "question": "Can I provide feedback or suggestions?",
          "answer": "Yes, we welcome your feedback and suggestions. Please use the contact form on our website to reach out to the creator."
        },
        {
          "question": "Is there a way to stay updated on the game's progress?",
          "answer": "Absolutely! You can subscribe to our newsletter or follow us on social media for the latest updates and news about Dimension-X."
        },
        {
          "question": "Will there be a beta testing phase?",
          "answer": "Yes, there will be a beta testing phase. Sign up on our website to be considered for early access."
        },
        {
          "question": "What platforms will Dimension-X be available on?",
          "answer": "Dimension-X is being developed with plans to be available on PC initially, with potential expansions to other platforms in the future."
        },
        {
          "question": "How can I support the development of Dimension-X?",
          "answer": "You can support the development by sharing our website with your friends, following us on social media, and providing feedback. Future crowdfunding opportunities may also be available."
        }
      ]
    }
        ;
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
