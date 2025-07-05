<template>
  <div id="app">
    <GameHeader v-if="isGameRoute" />
    <Header v-else />
    <div class="main-content">
      <router-view />
    </div>
    <GameFooter v-if="isGameRoute" />
    <Footer v-else />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import GameHeader from './components/GameHeader.vue';
import GameFooter from './components/GameFooter.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'App',
  components: {
    Header,
    Footer,
    GameHeader,
    GameFooter,
  },
  setup() {
    const route = useRoute();

    const isGameRoute = computed(() => {
      return route.meta.game === true;
    });

    return {
      isGameRoute
    };
  },
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: inherit;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow-x: hidden;
  max-width: 100vw;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  position: relative;
  padding: 0;
  margin: 0 auto;
  max-width: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .main-content {
    padding: 0;
  }
}
</style>
