import { ref, onMounted } from 'vue';

/**
 * Composable that randomly selects a hero background image from the backgrounds/hero folder.
 * Uses import.meta.glob for proper Vite build resolution.
 */
export function useRandomHeroBackground() {
  const backgroundUrl = ref<string>('');

  // Import all images from the backgrounds/hero folder
  // Using eager: true to load them immediately and get resolved URLs
  const images = import.meta.glob('@/assets/images/backgrounds/hero/*.{png,jpg,jpeg,webp}', {
    eager: true,
    import: 'default'
  });

  onMounted(() => {
    // Get all image paths
    const imagePaths = Object.keys(images);

    if (imagePaths.length > 0) {
      // Randomly select one image
      const randomIndex = Math.floor(Math.random() * imagePaths.length);
      const selectedPath = imagePaths[randomIndex];

      // Get the resolved URL from the imported module
      backgroundUrl.value = images[selectedPath] as string;
    }
  });

  return {
    backgroundUrl
  };
}
