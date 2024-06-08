<template>
  <footer class="footer">
    <div class="container">
      <p>&copy; 2024 Dimension-X. All rights reserved.</p>
<!--      <ul class="social-media">-->
<!--        <li><a href="#">Facebook</a></li>-->
<!--        <li><a href="#">Twitter</a></li>-->
<!--        <li><a href="#">Instagram</a></li>-->
<!--        <li><a href="#">YouTube</a></li>-->
<!--      </ul>-->
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: var(--dark-slate-gray);
  color: #FFFFFF;
  padding: 20px 0;
  text-align: center;
}

.footer .container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer .social-media {
  list-style: none;
  padding: 0;
  margin: 20px 0 0;
  display: flex;
  gap: 10px;
}

.footer .social-media a {
  color: #FFFFFF;
  text-decoration: none;
}

.footer .social-media a:hover {
  color: var(--cyber-yellow);
}
</style>
