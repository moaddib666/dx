# Internationalization (i18n) Guide

This project uses Vue I18n (version 9) for internationalization. This guide explains how to use and extend the i18n functionality.

## Available Languages

The application currently supports the following languages:

- English (en) - Default
- Ukrainian (uk)

## Directory Structure

```
src/
├── locales/
│   ├── en.json       # English translations
│   ├── uk.json       # Ukrainian translations
│   └── README.md     # This guide
├── i18n.js           # i18n configuration
└── components/
    └── LanguageSwitcher.vue  # Language selection component
```

## How to Use Translations in Components

### In Templates

Using the Composition API:

```vue
<template>
  <div>
    <h1>{{ t('some.translation.key') }}</h1>
    <p>{{ t('another.key', { param: value }) }}</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>
```

Using the Options API:

```vue
<template>
  <div>
    <h1>{{ $t('some.translation.key') }}</h1>
    <p>{{ $t('another.key', { param: value }) }}</p>
  </div>
</template>

<script>
export default {
  methods: {
    someMethod() {
      return this.$t('some.key');
    }
  }
}
</script>
```

### In JavaScript

```javascript
import { useI18n } from 'vue-i18n';

export default {
  setup() {
    const { t } = useI18n();
    
    const message = t('some.key');
    
    return { message };
  }
}
```

## Adding New Translations

1. Add your new translation keys to `src/locales/en.json` (and other language files)
2. Organize translations in logical categories (e.g., "common", "navigation", "auth")
3. Use the same structure across all language files

Example:

```json
{
  "feature": {
    "title": "Feature Title",
    "description": "Feature description"
  }
}
```

## Adding a New Language

To add a new language:

1. Create a new JSON file in the `src/locales` directory (e.g., `de.json` for German)
2. Copy the structure from `en.json` and translate all values
3. Update the `src/i18n.js` file to import and include the new language
4. Add the language option to the `LanguageSwitcher.vue` component

## Language Switching

The application includes a language switcher component that allows users to change the language. The selected language is stored in localStorage and persists across sessions.