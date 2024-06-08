<template>
  <div>
    <Header />
    <main class="support">
      <h1>Support</h1>
      <p>If you need help or have any questions, visit our support page for assistance.</p>
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
.support {
  padding: 60px;
  color: white;
}
</style>
