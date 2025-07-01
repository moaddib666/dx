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
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #fff;
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: #777;
}
</style>