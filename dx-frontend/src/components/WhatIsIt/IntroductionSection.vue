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

<script>
import ImageGallery from './ImageGallery.vue';

export default {
  name: 'IntroductionSection',
  components: {
    ImageGallery
  },
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    targetAudience: {
      type: String,
      required: true
    },
    benefits: {
      type: String,
      required: true
    },
    mainImage: {
      type: Object,
      required: true,
      validator: (value) => {
        return typeof value.src === 'string' &&
               typeof value.alt === 'string' &&
               typeof value.caption === 'string';
      }
    },
    galleryItems: {
      type: Array,
      required: true,
      validator: (value) => {
        return value.every(item =>
          typeof item.src === 'string' &&
          typeof item.alt === 'string' &&
          typeof item.caption === 'string'
        );
      }
    }
  },
  emits: ['toggle-zoom']
}
</script>

<style scoped>
.intro-section {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(0, 255, 255, 0.05));
  border: 2px solid rgba(255, 215, 0, 0.3);
}

.content-section {
  margin-bottom: 4rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.section-title {
  font-size: 2rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
}

.subsection-title {
  font-size: 1.5rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1rem;
  font-weight: 600;
}

.intro-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.intro-text {
  font-size: 1rem;
}

.intro-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1.5rem;
}

.intro-detail-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border-left: 3px solid var(--cyber-cyan, #00ffff);
}

.intro-detail-item h4 {
  color: var(--light-steel-blue, #b0c4de);
  font-weight: 500;
  margin: 0;
}

.intro-gallery {
  margin-top: 2rem;
}

.main-image-container {
  text-align: center;
  margin-bottom: 1.5rem;
}

.section-image {
  width: 100%;
  max-width: 450px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.zoomable-image {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 3px solid transparent;
  position: relative;
}

.zoomable-image::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.5), inset 0 0 15px rgba(255, 215, 0, 0.3);
  z-index: 1;
  pointer-events: none;
  animation: borderPulse 3s infinite alternate;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.zoomable-image:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
}

.zoomable-image:hover::before {
  opacity: 1;
}

.image-caption {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
  font-style: italic;
}

@keyframes borderPulse {
  0% {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(255, 215, 0, 0.2);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6), inset 0 0 20px rgba(255, 215, 0, 0.4);
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.5rem;
  }

  .subsection-title {
    font-size: 1.3rem;
  }

  .intro-details {
    grid-template-columns: 1fr;
  }

  .section-image {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.3rem;
  }

  .subsection-title {
    font-size: 1.1rem;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>