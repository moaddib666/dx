<template>
  <div>
    <form class="login-form" @submit.prevent="impersonateUser">
      <h2>Game Master Impersonation</h2>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <div class="form-group">
        <label for="token">User Access Token</label>
        <textarea
          id="token"
          v-model="token"
          placeholder="Paste the user access token here for impersonation"
          required
          rows="5"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit">Impersonate User</button>
      </div>

    </form>
  </div>
</template>

<script>
export default {
  name: "GameMasterImpersonate",
  data() {
    return {
      token: "",
      errorMessage: null,
    };
  },
  methods: {
    async impersonateUser() {
      try {
        if (!this.token.trim()) {
          this.errorMessage = "Please enter a valid user access token.";
          return;
        }

        // Dispatch the login action with the user's token for impersonation
        this.$store.dispatch("login", { token: this.token.trim() });

        // Redirect to the Game Master main page
        this.$router.push({ name: "GameMaster" });
      } catch (error) {
        this.errorMessage = "Invalid token or impersonation failed.";
        console.error("Impersonation error:", error);
      }
    },
  },
};
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: #1c1c1c;
  border: 2px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  max-width: 500px;
  margin: 2rem auto;
}

h2 {
  text-align: center;
  color: #e0e0e0;
  margin-top: 0;
}

.error-message {
  color: #ff4d4d;
  background: #2e2e2e;
  padding: 1rem;
  border-radius: 4px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-size: 1rem;
  font-weight: bold;
  color: #e0e0e0;
}

.form-group textarea {
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background: #292929;
  color: #e0e0e0;
  font-size: 1rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
  resize: vertical;
  font-family: monospace;
}

.form-group textarea:focus {
  outline: 2px solid #e0e0e0;
}

.form-actions {
  display: flex;
  justify-content: center;
}

.form-actions button {
  padding: 0.75rem 1.5rem;
  background: #444;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  transition: background 0.3s ease;
}

.form-actions button:hover {
  background: #555;
}

.alternative-login {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.alternative-login a {
  color: #66aaff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.alternative-login a:hover {
  color: #99ccff;
  text-decoration: underline;
}
</style>
