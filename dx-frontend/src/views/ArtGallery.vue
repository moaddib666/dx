<template>
  <div class="gallery">
    <PhotoGallery />
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
.gallery {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
