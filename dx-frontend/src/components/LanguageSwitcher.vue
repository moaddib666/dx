<template>
  <div class="language-switcher">
    <select v-model="currentLocale" @change="changeLocale">
      <option value="en">English</option>
      <option value="uk">Українська</option>
    </select>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'LanguageSwitcher',
  setup() {
    const { locale } = useI18n();
    const currentLocale = ref(locale.value || 'en');

    const changeLocale = () => {
      locale.value = currentLocale.value;
      localStorage.setItem('locale', currentLocale.value);
    };

    onMounted(() => {
      const savedLocale = localStorage.getItem('locale');
      if (savedLocale) {
        currentLocale.value = savedLocale;
        locale.value = savedLocale;
      } else {
        // Ensure English is selected by default
        currentLocale.value = 'en';
        locale.value = 'en';
        localStorage.setItem('locale', 'en');
      }
    });

    return {
      currentLocale,
      changeLocale
    };
  }
};
</script>

<style scoped>
.language-switcher {
  margin: 10px;
}

select {
  width: 100%;
  padding: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  background: rgba(15, 20, 28, 0.8);
  backdrop-filter: blur(8px);
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  transition: all 0.3s ease;
}

select:focus {
  outline: none;
  border-color: rgba(0, 255, 200, 0.6);
  box-shadow: 0 0 8px rgba(0, 255, 200, 0.2);
}

select:hover {
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(15, 20, 28, 0.9);
}

select option {
  background: rgba(15, 20, 28, 0.95);
  color: rgba(255, 255, 255, 0.9);
  padding: 8px;
}
</style>