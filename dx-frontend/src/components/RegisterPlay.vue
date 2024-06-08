<template>
  <section class="register-play">
    <h2>Register and Play</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="primary-btn">Register and Play</button>
    </form>
  </section>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    register() {
      // Handle registration logic
    }
  }
};
</script>

<style scoped>
.register-play {
  padding: 60px 0;
  background-color: var(--dark-slate-gray);
  color: #FFFFFF;
  text-align: center;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  color: var(--light-steel-blue);
}
.form-group input {
  width: 100%;
  padding: 10px;
  background-color: #3F4F4F;
  color: #FFFFFF;
  border: 1px solid var(--deep-purple);
  border-radius: 4px;
}
.primary-btn {
  margin: 10px;
  padding: 10px 20px;
  background-color: var(--electric-blue);
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'Roboto', sans-serif;
}
.primary-btn:hover {
  background-color: #1C86EE;
}
</style>
