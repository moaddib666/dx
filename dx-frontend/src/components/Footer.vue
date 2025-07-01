<template>
  <footer>
    <p><span v-html="t('footer.copyright')"></span> <a href="mailto: moaddib666@gmail.com">{{ t('footer.creator') }}</a></p>
  </footer>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
  name: 'Footer',
  setup() {
    const {t} = useI18n();
    return {t};
  }
}
</script>

<style scoped>
footer {
  background-color: var(--dark-slate-gray);
  color: white;
  padding: 20px;
  text-align: center;
  z-index: 50;
}
</style>
