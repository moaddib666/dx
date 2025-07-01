<template>
  <header class="header">
    <nav class="navbar container">
      <ul>
        <li v-for="link in links" :key="link.id">
          <a :href="link.url">{{ t(`navigation.${link.id}`) }}</a>
        </li>
      </ul>
      <LanguageSwitcher class="language-switcher" />
    </nav>
  </header>
</template>

<script>
import LanguageSwitcher from './LanguageSwitcher.vue';
import { useI18n } from 'vue-i18n';

export default {
  components: {
    LanguageSwitcher
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      links: [
        { id: 'home', url: '/' },
        // { id: 'story', url: '/story' },
        // { id: 'characters', url: '/characters' },
        // { id: 'gameplay', url: '/gameplay' },
        // { id: 'community', url: '/community' },
        // { id: 'shop', url: '/shop' },
        // { id: 'support', url: '/support' },
        { id: 'faq', url: '/faq' },
        { id: 'artGallery', url: '/art/' }
      ]
    };
  }
};
</script>

<style scoped>
.header {
  background-color: var(--dark-slate-gray);
  padding: 10px 0;
  z-index: 50;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar ul {
  display: flex;
  justify-content: flex-start;
  list-style: none;
  margin: 0;
  padding: 0;
  flex-grow: 1;
}

.navbar a {
  color: #FFFFFF;
  text-decoration: none;
  font-size: 16px;
}

.navbar a:hover {
  color: var(--cyber-yellow);
}

.navbar li {
  margin-right: 20px;
}

.language-switcher {
  margin-right: 20px;
}

</style>
