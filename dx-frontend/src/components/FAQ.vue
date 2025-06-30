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
          "answer": "The game is now public with limited functionality! To play your first campaign, register on the site and reach out to a game master through our Discord. Check our <a href='/faq/newcomers-guide' class='guide-link'>Newcomer's Guide</a> for detailed information on getting started and our <a href='/faq/player-cheatsheet' class='guide-link'>Player Cheat Sheet</a> for quick reference during gameplay. You can also interact with our AI assistant or contact the creator directly for help."
        },
        {
          "question": "Can I switch dimensions?",
          "answer": "Yes! Dimension switching is a core feature of the game, allowing players to explore different dimensions with varying effects on gameplay. Each dimension has unique properties that affect your character's abilities and resources."
        },
        {
          "question": "Who is developing Dimension-X?",
          "answer": "Dimension-X is being developed by a single person who is passionate about creating immersive game experiences."
        },
        {
          "question": "When will Dimension-X be available?",
          "answer": "Dimension-X is now available with limited functionality! We're in an early access phase where players can join campaigns led by game masters. We're continuously adding new features and expanding the game. Stay updated on our progress by subscribing to our newsletter or following us on social media."
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
          "question": "Is the game in beta testing?",
          "answer": "Yes, we're currently in an early access phase! Players can already join campaigns and experience the core gameplay. This phase helps us gather feedback and improve the game. If you're playing now, you're already part of our testing community - thank you for your support!"
        },
        {
          "question": "What platforms is Dimension-X available on?",
          "answer": "Dimension-X is currently available on PC through our web platform. We're focusing on providing the best experience on this platform before considering expansions to other platforms in the future."
        },
        {
          "question": "How can I support the development of Dimension-X?",
          "answer": "The best way to support us now is by playing the game, providing feedback on your experience, and reporting any issues you encounter. You can also help by inviting friends to join campaigns, sharing your gameplay experiences on social media, and engaging with our community on Discord. Your participation during this early access phase is invaluable to our development process!"
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
