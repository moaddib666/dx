<script>
export default {
  name: "EditInDjangoAdmin",
  props: {
    app: {
      type: String,
      required: true,
    },
    model: {
      type: String,
      required: true,
    },
    id: {
      type: [String, Number],
      required: true,
    },
    title: {
      type: String,
      default: "Edit in Django Admin",
    },
  },
  computed: {
    adminUrl() {
      return `/admin/${this.app}/${this.model}/${this.id}/change/`;
    }
  }
}
</script>

<template>
  <a :href="adminUrl" :title="title" class="django-admin-icon" target="_blank">
    <svg class="django-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path
          d="M11.146 0h3.924v18.166c-2.013.382-3.491.535-5.096.535-4.791 0-7.288-2.166-7.288-6.32 0-4.002 2.65-6.6 6.753-6.6.637 0 1.121.05 1.707.203zm0 9.143a3.894 3.894 0 00-1.325-.204c-1.988 0-3.134 1.223-3.134 3.365 0 2.09 1.096 3.236 3.109 3.236.433 0 .79-.025 1.35-.102V9.142zM21.314 6.06v9.098c0 3.134-.229 4.638-.917 5.937-.637 1.249-1.478 2.039-3.211 2.905l-3.644-1.733c1.733-.815 2.574-1.53 3.109-2.625.561-1.121.739-2.421.739-5.835V6.059h3.924z"
          fill="currentColor"/>
    </svg>
  </a>
</template>

<style scoped>
.django-admin-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 5vh;
  width: 5vh;
  border-radius: 50%;
  background-color: #092e20;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
}

.django-admin-icon:hover {
  background-color: #0c4b33;
  transform: scale(1.05);
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.django-icon {
  height: 60%;
  width: 60%;
}
</style>