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

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
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
