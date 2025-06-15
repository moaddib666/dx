<script>
export default {
  name: "EditInDjangoAdmin",
  props: {
    app: {
      type: String,
      required: true
    },
    model: {
      type: String,
      required: true
    },
    id: {
      type: [String, Number],
      required: true
    },
    baseUrl: {
      type: String,
      default: ''
    }
  },
  computed: {
    adminUrl() {
      const base = this.baseUrl || window.location.origin;
      return `${base}/admin/${this.app}/${this.model}/${this.id}/change/`;
    }
  },
  methods: {
    openDjangoAdmin() {
      window.open(this.adminUrl, '_blank', 'noopener,noreferrer');
    }
  }
}
</script>

<template>
  <button
      :title="`Edit ${model} in Django Admin`"
      class="django-admin-button"
      type="button"
      @click="openDjangoAdmin"
  >
    <!-- Django-style admin icon -->
    <svg
        class="django-icon"
        fill="none"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
    >
      <!-- Gear/Settings icon representing admin -->
      <path
          d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L19 6L17 7V9L19 10L21 9ZM3 9V7L5 6L7 7V9L5 10L3 9ZM12 18C10.9 18 10 18.9 10 20C10 21.1 10.9 22 12 22C13.1 22 14 21.1 14 20C14 18.9 13.1 18 12 18Z"
          fill="currentColor"
      />
      <path
          d="M12 9C13.66 9 15 10.34 15 12C15 13.66 13.66 15 12 15C10.34 15 9 13.66 9 12C9 10.34 10.34 9 12 9Z"
          fill="currentColor"
      />
      <!-- Django-inspired rectangles -->
      <rect fill="currentColor" height="2" rx="1" width="3" x="2" y="11"/>
      <rect fill="currentColor" height="2" rx="1" width="3" x="19" y="11"/>
      <rect fill="currentColor" height="3" rx="1" width="2" x="11" y="2"/>
      <rect fill="currentColor" height="3" rx="1" width="2" x="11" y="19"/>
    </svg>
  </button>
</template>

<style scoped>
.django-admin-button {
  /* Size and positioning */
  height: 5vh;
  width: 5vh;
  min-height: 24px;
  min-width: 24px;
  max-height: 48px;
  max-width: 48px;

  /* Button styling */
  border: 2px solid #79aec8;
  border-radius: 8px;
  background: linear-gradient(135deg, #417690 0%, #79aec8 100%);
  color: white;
  cursor: pointer;

  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;

  /* Transitions */
  transition: all 0.2s ease-in-out;

  /* Accessibility */
  outline: none;
  focus-visible: true;
}

.django-admin-button:hover {
  background: linear-gradient(135deg, #2c5282 0%, #4299e1 100%);
  border-color: #4299e1;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
}

.django-admin-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(66, 153, 225, 0.2);
}

.django-admin-button:focus-visible {
  outline: 2px solid #4299e1;
  outline-offset: 2px;
}

.django-icon {
  height: 60%;
  width: 60%;
  flex-shrink: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .django-admin-button {
    height: 6vh;
    width: 6vh;
    min-height: 32px;
    min-width: 32px;
  }
}

@media (max-width: 480px) {
  .django-admin-button {
    height: 7vh;
    width: 7vh;
    min-height: 36px;
    min-width: 36px;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .django-admin-button {
    border-width: 3px;
    background: #0066cc;
  }

  .django-admin-button:hover {
    background: #004499;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .django-admin-button {
    transition: none;
  }

  .django-admin-button:hover {
    transform: none;
  }
}
</style>