<template>
  <div id="app">
    <Header />
    <div class="main-content">
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import HeroSection from './components/HeroSection.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    Header,
    HeroSection,
    Footer,
  },
};
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

footer {
  background-color: var(--dark-slate-gray);
  color: white;
  padding: 20px;
  text-align: center;
}
</style>
