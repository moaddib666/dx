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

<script>
export default {
  name: 'FooterSection',
  props: {
    readyText: {
      type: String,
      required: true
    },
    discordText: {
      type: String,
      required: true
    },
    discordLink: {
      type: String,
      required: true,
      default: 'https://discord.gg/32dwT8EP'
    },
    additionalLinks: {
      type: Array,
      required: true,
      validator: (value) => {
        return value.every(link =>
          typeof link.to === 'string' &&
          typeof link.text === 'string'
        );
      }
    }
  }
}
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
  color: var(--light-steel-blue, #b0c4de);
}

.discord-link {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: linear-gradient(45deg, var(--cyber-yellow, #ffd700), var(--cyber-cyan, #00ffff));
  color: #000;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.discord-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
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
  background: rgba(255, 255, 255, 0.1);
  color: var(--cyber-yellow, #ffd700);
  text-decoration: none;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.additional-link:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
  color: white;
  text-decoration: none;
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