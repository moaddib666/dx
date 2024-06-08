<template>
  <header class="header">
    <nav class="navbar container">
      <ul>
        <li v-for="link in links" :key="link.text">
          <a :href="link.url">{{ link.text }}</a>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  data() {
    return {
      links: [
        { text: 'Home', url: '/' },
        // { text: 'Story', url: '/story' },
        // { text: 'Characters', url: '/characters' },
        // { text: 'Gameplay', url: '/gameplay' },
        // { text: 'Community', url: '/community' },
        // { text: 'Shop', url: '/shop' },
        // { text: 'Support', url: '/support' },
        { text: 'FAQ', url: '/faq' },
        { text: 'Art Gallery', url: '/art/' }
      ]
    };
  }
};
</script>

<style scoped>
.header {
  background-color: var(--dark-slate-gray);
  padding: 10px 0;
}

.navbar ul {
  display: flex;
  justify-content: space-around;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar a {
  color: #FFFFFF;
  text-decoration: none;
  font-size: 16px;
}

.navbar a:hover {
  color: var(--cyber-yellow);
}
</style>
