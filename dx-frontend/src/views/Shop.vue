<template>
  <div>
    <Header />
    <main class="shop">
      <h1>Shop</h1>
      <p>Explore the Dimension-X shop to find exclusive items, gear upgrades, and more.</p>
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
.shop {
  padding: 60px;
  color: white;
}
</style>
