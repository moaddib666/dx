import { createI18n } from 'vue-i18n';
import enLocale from './locales/en.json';
import ukLocale from './locales/uk.json';

const messages = {
  en: enLocale,
  uk: ukLocale
};

// Get the saved locale from localStorage or use 'en' as default
const savedLocale = localStorage.getItem('locale') || 'en';

const i18n = createI18n({
  legacy: false, // you must set `false`, to use Composition API
  locale: savedLocale, // use saved locale or default
  fallbackLocale: 'en', // set fallback locale
  messages, // set locale messages
  silentTranslationWarn: true, // suppress warnings when translation is missing
  silentFallbackWarn: true, // suppress warnings when falling back to fallback locale
  missingWarn: false, // suppress warnings of missing keys
  fallbackWarn: false // suppress warnings of fallback translations
});

export default i18n;