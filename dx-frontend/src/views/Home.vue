<template>
  <div>
    <Header />
    <HeroSection />
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import HeroSection from '@/components/HeroSection.vue';
import DimensionSwitcher from '@/components/DimensionSwitcher.vue';
import FAQ from '@/components/FAQ.vue';
import RegisterPlay from '@/components/RegisterPlay.vue';
import Footer from '@/components/Footer.vue';

export default {
  components: {
    Header,
    HeroSection,
    DimensionSwitcher,
    FAQ,
    RegisterPlay,
    Footer
  }
};
</script>
