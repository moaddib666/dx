<template>
  <div>
    <Header />
    <main class="gameplay">
      <h1>Gameplay</h1>
      <p>Discover the innovative gameplay mechanics of Dimension-X that blend strategy, action, and role-playing elements.</p>
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';

export default {
  components: {
    Header,
    Footer
  }
};
</script>

<style scoped>
.gameplay {
  padding: 60px;
  color: white;
}
</style>
