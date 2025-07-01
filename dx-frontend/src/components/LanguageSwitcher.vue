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
    const currentLocale = ref(locale.value);

    const changeLocale = () => {
      locale.value = currentLocale.value;
      localStorage.setItem('locale', currentLocale.value);
    };

    onMounted(() => {
      const savedLocale = localStorage.getItem('locale');
      if (savedLocale) {
        currentLocale.value = savedLocale;
        locale.value = savedLocale;
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
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #333;
  color: white;
  border: 1px solid #555;
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: #777;
}
</style>