<template>
  <div>
    <Header />
    <main class="characters">
      <h1>Characters</h1>
      <p>Meet the diverse and dynamic characters of Dimension-X, each with their unique abilities and stories.</p>
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
.characters {
  padding: 60px;
  color: white;
}
</style>
