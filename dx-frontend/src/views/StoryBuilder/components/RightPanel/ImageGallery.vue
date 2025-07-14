<template>
  <div class="image-gallery">
    <h3>
      <span class="icon">🖼️</span> Image Gallery
      <button
        v-if="editMode"
        @click="triggerFileUpload"
        class="btn-upload-image"
      >
        <span class="icon">+</span> Add Image
      </button>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="file-input"
        @change="handleFileChange"
      />
    </h3>

    <div v-if="!images.length" class="empty-gallery-message">
      No images available for this chapter.
    </div>

    <div v-else class="gallery-grid">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="image-item"
      >
        <div class="image-container">
          <img :src="image" :alt="`Chapter image ${index + 1}`" class="gallery-image" @click="openImagePreview(image)" />
          <div v-if="editMode" class="image-actions">
            <button @click.stop="deleteImage(image)" class="btn-delete-image">
              <span class="icon">🗑️</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Preview Modal -->
    <div v-if="previewImage" class="image-preview-modal" @click="closeImagePreview">
      <div class="modal-content" @click.stop>
        <img :src="previewImage" alt="Preview" class="preview-image" />
        <button class="btn-close-preview" @click="closeImagePreview">
          <span class="icon">✖</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps<{
  images: string[];
  editMode: boolean;
}>();

const emit = defineEmits<{
  (e: 'upload', imageUrl: string): void;
  (e: 'delete', imageUrl: string): void;
}>();

// Refs
const fileInput = ref<HTMLInputElement | null>(null);
const previewImage = ref<string | null>(null);

// Event handlers
const triggerFileUpload = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length) return;

  const file = target.files[0];
  const reader = new FileReader();

  reader.onload = (e) => {
    if (e.target?.result) {
      // In a real application, you would upload the file to a server
      // and get back a URL. For this demo, we'll use the data URL.
      const imageUrl = e.target.result as string;
      emit('upload', imageUrl);

      // Reset the file input
      if (fileInput.value) {
        fileInput.value.value = '';
      }
    }
  };

  reader.readAsDataURL(file);
};

const deleteImage = (imageUrl: string) => {
  emit('delete', imageUrl);
};

const openImagePreview = (imageUrl: string) => {
  previewImage.value = imageUrl;
};

const closeImagePreview = () => {
  previewImage.value = null;
};
</script>

<style scoped>
.image-gallery {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.image-gallery h3 {
  font-size: 1.3rem;
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.75rem;
}

.image-gallery h3 .icon {
  margin-right: 0.5rem;
}

.btn-upload-image {
  margin-left: auto;
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.btn-upload-image:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.file-input {
  display: none;
}

.empty-gallery-message {
  text-align: center;
  padding: 2rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.image-item {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
}

.image-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.gallery-image:hover {
  transform: scale(1.05);
}

.image-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.image-container:hover .image-actions {
  opacity: 1;
}

.btn-delete-image {
  background: rgba(0, 0, 0, 0.6);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-delete-image:hover {
  background: rgba(255, 0, 0, 0.6);
}

/* Image Preview Modal */
.image-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.preview-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.btn-close-preview {
  position: absolute;
  top: -40px;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: all 0.2s ease;
}

.btn-close-preview:hover {
  background: rgba(255, 255, 255, 0.2);
}

.icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .image-gallery {
    padding: 1rem;
  }

  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.75rem;
  }

  .btn-upload-image {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}
</style>