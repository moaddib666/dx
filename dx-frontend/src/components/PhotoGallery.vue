<template>
  <div class="gallery-content">
    <!-- Loading overlay -->
    <Loader
      v-if="loading"
      text="Loading gallery..."
      message="Please wait while we fetch the images"
    />

    <!-- Error message -->
    <div v-else-if="error" class="error-message">
      <div class="warning-icon">⚠️</div>
      <h2 class="warning-title">Error Loading Gallery</h2>
      <p class="warning-message">{{ errorMessage }}</p>
      <button class="retry-button" @click="loadPhotos">Retry</button>
    </div>

    <!-- Gallery content -->
    <div v-else>
      <div class="gallery-header">
        <TitleComponent>Photo Gallery</TitleComponent>
      </div>

      <!-- No images message -->
      <div v-if="photos.length === 0" class="no-images-message">
        <div class="warning-icon">📷</div>
        <h2 class="warning-title">No Images Available</h2>
        <p class="warning-message">There are currently no images in the gallery.</p>
      </div>

      <!-- Gallery grid -->
      <div v-else class="gallery-section">
        <div class="gallery-grid">
          <div v-for="(photo, index) in photos" :key="index" class="photo-item">
            <div class="photo-card">
              <img :src="photo" :alt="`Gallery image ${index + 1}`" @error="handleImageError(index)" />
              <div class="photo-overlay">
                <span class="photo-number">{{ index + 1 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';
import Loader from '@/components/Loader.vue';
import {GalleryGameApi} from "@/api/backendService.js";

export default {
  data() {
    return {
      photos: [],
      loading: true,
      error: false,
      errorMessage: '',
      failedImages: new Set()
    };
  },
  components: {
    TitleComponent,
    Loader
  },
  created() {
    this.loadPhotos();
  },
  methods: {
    async loadPhotos() {
      this.loading = true;
      this.error = false;
      this.errorMessage = '';

      try {
        const artObjects = (await GalleryGameApi.galleryWorldList()).data;
        this.photos = artObjects.map(artObject => artObject.image);
        console.log('Loaded gallery images:', this.photos);
      } catch (error) {
        console.error('Error loading gallery images:', error);
        this.error = true;
        this.errorMessage = error.message || 'Failed to load gallery images. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    handleImageError(index) {
      console.warn(`Failed to load image at index ${index}`);
      this.failedImages.add(index);
    }
  }
}
</script>

<style scoped>
.gallery-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.gallery-header {
  padding: 1rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.gallery-section {
  width: 100%;
  overflow-x: hidden;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-right: 10px;
}

/* Scrollbar styling is now handled globally in global.css */

.photo-item {
  position: relative;
  transition: transform 0.3s ease;
}

.photo-item:hover {
  transform: translateY(-5px);
}

.photo-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.2);
  background: rgba(255, 255, 255, 0.05);
  height: 250px;
}

.photo-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.photo-card:hover img {
  transform: scale(1.05);
}

.photo-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.5rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  justify-content: flex-end;
}

.photo-number {
  background: var(--cyber-yellow, #ffd700);
  color: black;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* Error and No Images Styling */
.error-message, .no-images-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
  margin: 2rem auto;
  max-width: 600px;
  text-align: center;
}

.warning-icon {
  font-size: 48px;
  margin-bottom: 20px;
  color: var(--cyber-yellow, #ffd700);
}

.warning-title {
  font-size: 24px;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 15px;
  font-weight: 600;
}

.warning-message {
  font-size: 16px;
  color: var(--light-steel-blue, #b0c4de);
  margin-bottom: 25px;
  line-height: 1.5;
}

.retry-button {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: linear-gradient(45deg, var(--cyber-yellow, #ffd700), #00ffff);
  color: #000;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .photo-card {
    height: 180px;
  }
}
</style>
