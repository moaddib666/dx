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
    <svg class="django-icon" fill="#000000" preserveAspectRatio="xMidYMid" version="1.1"
         viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
      <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
      <g id="SVGRepo_iconCarrier">
        <g>
          <rect fill="#092E20" height="256" rx="28" width="256" x="0" y="0"></rect>
          <path
              d="M186.377012,94.197636 L186.377012,160.424478 C186.377012,183.243286 184.707519,194.187745 179.699037,203.649406 C175.060358,212.741266 168.937684,218.490548 156.323731,224.798721 L129.794937,212.183571 C142.410087,206.247593 148.531564,201.05481 152.427049,193.074749 C156.509231,184.91278 157.808923,175.451119 157.808923,150.593015 L157.808923,94.197636 L186.377012,94.197636 Z M140.928486,50.0787207 L140.928486,182.316986 C126.272844,185.099476 115.512688,186.212472 103.826231,186.212472 C68.9487718,186.212472 50.7686431,170.445031 50.7686431,140.205054 C50.7686431,111.079269 70.0629644,92.1583404 99.9295492,92.1583404 C104.567032,92.1583404 108.091519,92.5281423 112.359199,93.6411381 L112.359199,50.0787207 L140.928486,50.0787207 Z M102.713236,115.160254 C88.243093,115.160254 79.8944275,124.065418 79.8944275,139.647359 C79.8944275,154.860696 87.8720944,163.208164 102.527736,163.208164 C105.680028,163.208164 108.278215,163.022665 112.359199,162.467364 L112.359199,116.643052 C109.020212,115.531253 106.237722,115.160254 102.713236,115.160254 Z M186.377012,50.2307105 L186.377012,79.5419941 L157.808923,79.5419941 L157.808923,50.2307105 L186.377012,50.2307105 Z"
              fill="#FFFFFD"></path>
        </g>
      </g>
    </svg>
  </button>
</template>

<style scoped>
.django-admin-button {
  /* Size and positioning */
  height: 3vh;
  width: 3vh;
  min-height: 10px;
  min-width: 10px;
  max-height: 48px;
  max-width: 48px;

  /* Button styling */
  border: 2px solid #0c6442;
  border-radius: 8px;
  background: linear-gradient(135deg, #0c6442 0%, #0e8555 100%);
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
  background: linear-gradient(135deg, #095335 0%, #0e8555 100%);
  border-color: #0e8555;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(12, 100, 66, 0.3);
}

.django-admin-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(12, 100, 66, 0.2);
}

.django-admin-button:focus-visible {
  outline: 2px solid #0c6442;
  outline-offset: 2px;
}

.django-icon {
  height: 98%;
  width: 98%;
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
    background: #0c6442;
  }

  .django-admin-button:hover {
    background: #095335;
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
