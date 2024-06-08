<template>
  <div>
    <Header />
    <main class="faq">
      <h1>FAQ</h1>
      <p>Find answers to the most frequently asked questions about Dimension-X.</p>
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
.faq {
  padding: 60px;
  color: white;
}
</style>
