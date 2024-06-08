<template>
  <div>
    <Header />
    <main class="community">
      <h1>Community</h1>
      <p>Join the vibrant Dimension-X community and connect with other players, share experiences, and participate in events.</p>
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
.community {
  padding: 60px;
  color: white;
}
</style>
