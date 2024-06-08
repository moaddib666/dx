<template>
  <div>
    <Header />
    <main class="story">
      <h1>Story</h1>
      <p>Welcome to the story of Dimension-X. Here, magic and technology collide to create an epic adventure.</p>
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
.story {
  padding: 60px;
  color: white;
}
</style>
