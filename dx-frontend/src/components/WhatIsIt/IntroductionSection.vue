<template>
  <section class="content-section intro-section">
    <h2 class="section-title">{{ title }}</h2>
    <div class="intro-content">
      <div class="intro-text">
        <h3 class="subsection-title">{{ subtitle }}</h3>
        <p v-html="description"></p>
        <div class="intro-details">
          <div class="intro-detail-item">
            <h4>{{ targetAudience }}</h4>
          </div>
          <div class="intro-detail-item">
            <h4>{{ benefits }}</h4>
          </div>
        </div>
      </div>

      <div class="intro-gallery">
        <div class="main-image-container">
          <img
            :src="mainImage.src"
            :alt="mainImage.alt"
            class="section-image zoomable-image"
            @click="$emit('toggle-zoom', $event)"
          />
          <p class="image-caption">{{ mainImage.caption }}</p>
        </div>

        <ImageGallery
          :items="galleryItems"
          @toggle-zoom="$emit('toggle-zoom', $event)"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import ImageGallery from './ImageGallery.vue'

interface ImageData {
  src: string
  alt: string
  caption: string
}

defineProps<{
  title: string
  subtitle: string
  description: string
  targetAudience: string
  benefits: string
  mainImage: ImageData
  galleryItems: ImageData[]
}>()

defineEmits<{
  (e: 'toggle-zoom', event: Event): void
}>()
</script>

<style scoped>
.intro-section {
  background: linear-gradient(135deg, rgba(99, 247, 255, 0.1), rgba(34, 211, 238, 0.05));
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.content-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(9, 16, 28, 0.55);
  border-radius: 12px;
  border: 1px solid rgba(99, 247, 255, 0.4);
  box-shadow: 0 0 8px rgba(34, 211, 238, 0.15);
}

.section-title {
  font-size: 2rem;
  color: #c7f5ff;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  letter-spacing: 0.2em;
}

.subsection-title {
  font-size: 1.5rem;
  color: #bdf9ff;
  margin-bottom: 1rem;
  font-weight: 600;
  letter-spacing: 0.15em;
}

.intro-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.intro-text {
  font-size: 1rem;
  line-height: 1.7;
}

.intro-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.intro-detail-item {
  padding: 0.75rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.intro-detail-item h4 {
  color: #b7f9ff;
  font-weight: 500;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.6;
}

.intro-gallery {
  margin-top: 1.5rem;
}

.main-image-container {
  text-align: center;
  margin-bottom: 1.5rem;
}

.section-image {
  width: 100%;
  max-width: 600px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.zoomable-image {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.3);
  position: relative;
}

.zoomable-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
  border-color: rgba(99, 247, 255, 0.5);
}

.image-caption {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #9feaff;
  font-style: italic;
  opacity: 0.9;
}

@media (max-width: 1024px) {
  .content-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .subsection-title {
    font-size: 1.4rem;
  }
}

@media (max-width: 768px) {
  .content-section {
    padding: 1.25rem;
  }

  .section-title {
    font-size: 1.5rem;
    letter-spacing: 0.15em;
  }

  .subsection-title {
    font-size: 1.3rem;
    letter-spacing: 0.1em;
  }

  .intro-details {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .section-image {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .content-section {
    padding: 1rem;
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: 1.3rem;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
  }

  .subsection-title {
    font-size: 1.1rem;
    letter-spacing: 0.08em;
  }

  .intro-text {
    font-size: 0.95rem;
  }

  .intro-detail-item {
    padding: 0.75rem;
  }

  .intro-detail-item h4 {
    font-size: 0.9rem;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>