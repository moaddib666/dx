<script setup lang="ts">
import { ref } from 'vue';
import CharacterToken from '@/components/CharacterToken/CharacterToken.vue';

// Sample character images for testing
const sampleImages = [
  'https://i.pravatar.cc/300?img=1',
  'https://i.pravatar.cc/300?img=2',
  'https://i.pravatar.cc/300?img=3',
  'https://i.pravatar.cc/300?img=4',
];

const customImageUrl = ref('');
</script>

<template>
  <div class="character-token-preview">
    <div class="preview-header">
      <h1>Character Token Preview</h1>
      <p>Test and preview the CharacterToken component</p>
    </div>

    <div class="preview-content">
      <!-- Placeholder token -->
      <div class="token-section">
        <h2>Placeholder (No Image)</h2>
        <div class="token-container">
          <CharacterToken />
        </div>
      </div>

      <!-- Sample tokens with images -->
      <div class="token-section">
        <h2>Sample Character Tokens</h2>
        <div class="token-grid">
          <div v-for="(image, index) in sampleImages" :key="index" class="token-container">
            <CharacterToken :image="image" />
          </div>
        </div>
      </div>

      <!-- Custom image input -->
      <div class="token-section">
        <h2>Custom Image URL</h2>
        <div class="custom-input-group">
          <input
            v-model="customImageUrl"
            type="text"
            placeholder="Enter image URL..."
            class="custom-input"
          />
        </div>
        <div class="token-container" v-if="customImageUrl">
          <CharacterToken :image="customImageUrl" />
        </div>
      </div>

      <!-- Size variations -->
      <div class="token-section">
        <h2>Size Variations (Responsive)</h2>
        <div class="size-variations">
          <div class="size-box small">
            <p>Small (100px)</p>
            <CharacterToken :image="sampleImages[0]" />
          </div>
          <div class="size-box medium">
            <p>Medium (200px)</p>
            <CharacterToken :image="sampleImages[1]" />
          </div>
          <div class="size-box large">
            <p>Large (300px)</p>
            <CharacterToken :image="sampleImages[2]" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.character-token-preview {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.preview-header {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
}

.preview-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.preview-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.preview-content {
  max-width: 1200px;
  margin: 0 auto;
}

.token-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.token-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.token-container {
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.token-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  justify-items: center;
}

.custom-input-group {
  margin-bottom: 1.5rem;
}

.custom-input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.custom-input:focus {
  outline: none;
  border-color: #667eea;
}

.size-variations {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 2rem;
}

.size-box {
  text-align: center;
}

.size-box p {
  margin-bottom: 1rem;
  font-weight: bold;
  color: #555;
}

.size-box.small {
  width: 100px;
  height: 100px;
}

.size-box.medium {
  width: 200px;
  height: 200px;
}

.size-box.large {
  width: 300px;
  height: 300px;
}

@media (max-width: 768px) {
  .character-token-preview {
    padding: 1rem;
  }

  .preview-header h1 {
    font-size: 2rem;
  }

  .token-section {
    padding: 1.5rem;
  }

  .token-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .size-variations {
    flex-direction: column;
    align-items: center;
  }
}
</style>
