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
import {GalleryGameApi} from "@/api/backendService.js";

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
    async loadPhotos() {
      const artObjects = (await GalleryGameApi.galleryWorldList()).data;
      this.photos = artObjects.map(artObject => artObject.image);
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
