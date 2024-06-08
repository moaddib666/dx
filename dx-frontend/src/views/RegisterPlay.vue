<template>
  <div>
    <Header />
    <main class="register-play">
      <RegisterPlay />
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import RegisterPlay from '@/components/RegisterPlay.vue';
import Footer from '@/components/Footer.vue';

export default {
  components: {
    Header,
    RegisterPlay,
    Footer
  }
};
</script>

<style scoped>
.register-play {
  padding: 60px;
  color: white;
}
</style>
