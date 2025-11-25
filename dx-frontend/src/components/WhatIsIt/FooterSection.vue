<template>
  <div class="footer-section">
    <p>{{ readyText }}</p>
    <a :href="discordLink" target="_blank" class="discord-link">
      {{ discordText }}
    </a>
    <div class="additional-links">
      <router-link
        v-for="(link, index) in additionalLinks"
        :key="index"
        :to="link.to"
        class="additional-link"
      >
        {{ link.text }}
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
interface FooterLink {
  to: string
  text: string
}

withDefaults(defineProps<{
  readyText: string
  discordText: string
  discordLink: string
  additionalLinks: FooterLink[]
}>(), {
  discordLink: 'https://discord.gg/vC3TvVzK'
})
</script>

<style scoped>
.footer-section {
  text-align: center;
  padding: 2rem;
  margin-top: 2rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
}

.footer-section p {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #9feaff;
  opacity: 0.95;
}

.discord-link {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: linear-gradient(45deg, rgba(99, 247, 255, 0.8), rgba(34, 211, 238, 0.8));
  color: #000;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: transform 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.6);
}

.discord-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4);
}

.additional-links {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.additional-link {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: rgba(10, 18, 32, 0.6);
  color: #bdf9ff;
  text-decoration: none;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.4);
}

.additional-link:hover {
  background: rgba(34, 211, 238, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(34, 211, 238, 0.3);
  color: #e8fdff;
  text-decoration: none;
  border-color: rgba(99, 247, 255, 0.6);
}

@media (max-width: 768px) {
  .additional-links {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .discord-link {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
  }
}
</style>