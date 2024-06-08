<template>
  <div>
    <div class="sub-heading">
      <TitleComponent>Photo Gallery</TitleComponent>
    </div>
    <div class="gallery">
      <div v-for="photo in photos" :key="photo" class="photo-item">
        <img :src="photo" :alt="photo" />
      </div>
    </div>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';

export default {
  data() {
    return {
      photos: []
    };
  },
  components: {
    TitleComponent
  },
  created() {
    this.loadPhotos();
  },
  methods: {
    loadPhotos() {
      // Use Vite's import.meta.glob to dynamically load images
      const importImages = import.meta.glob('@/assets/images/gallery/*.{png,jpg,jpeg,webp}');
      this.photos = Object.keys(importImages).map(path => path.replace(/^@/, ''));
    }
  }
}
</script>

<style>
.sub-heading {
  padding: 20pt;
  text-align: left;
}
.gallery {
  display: flex;
  flex-wrap: wrap;
}

.photo-item {
  margin: 5px;
}

.photo-item img {
  width: 200px;
  height: 200px;
  object-fit: cover;
}
</style>
