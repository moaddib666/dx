<template>
  <div class="page-container">
    <div class="hero-background"></div>
    <div class="gallery">
      <PhotoGallery />
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import PhotoGallery from "@/components/PhotoGallery.vue";

export default {
  components: {
    PhotoGallery,
    Header,
    Footer
  }
};
</script>

<style>
.page-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/backgrounds/dx-art-background.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

.gallery {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  position: relative;
  z-index: 1;
  padding: 1rem;
}

.main-content {
  overflow: hidden;
  align-items: center;
  justify-content: center;
}
</style>
