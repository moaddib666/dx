<template>
  <div class="page-container">
    <HeroBackground id="background"></HeroBackground>
    <div class="gallery">
      <PhotoGallery />
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import PhotoGallery from "@/components/PhotoGallery.vue";
import HeroBackground from '@/components/WhatIsIt/HeroBackground.vue';

export default {
  components: {
    PhotoGallery,
    Header,
    Footer,
    HeroBackground
  }
};
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
}

/* Ensure the background component uses a custom image from common directory */
#background {
  background-image: url('@/assets/images/backgrounds/common/moaddib_Cinematic_wide_shot_of_a_futuristic_cyberpunk-fantasy_23d0abcd-0f8e-4edc-84ab-63db431446f6_1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.gallery {
  max-width: 1400px;
  width: 100%;
  padding: 3rem 2rem;
  color: #e0f7fa;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(2px);
  margin: 0 auto;
  border-radius: 12px;
}

@media (max-width: 1024px) {
  .gallery {
    max-width: 100%;
    padding: 2.5rem 1.5rem;
    padding-top: 80px;
  }
}

@media (max-width: 768px) {
  .gallery {
    padding: 2rem 1.25rem;
    padding-top: 70px;
  }
}

@media (max-width: 480px) {
  .gallery {
    padding: 1.5rem 1rem;
    padding-top: 60px;
  }
}
</style>
