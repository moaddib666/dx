<template>
  <div class="bio-component">
    <h2>Character Bio</h2>
    <form @submit.prevent="submitBio">
      <!-- Name -->
      <div class="form-group">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="bio.name"
            placeholder="Enter character name"
            required
            type="text"
        />
      </div>

      <!-- Age -->
      <div class="form-group">
        <label for="age">Age</label>
        <input
            id="age"
            v-model.number="bio.age"
            min="1"
            placeholder="Enter character age"
            required
            type="number"
        />
      </div>

      <!-- Gender -->
      <div class="form-group">
        <label for="gender">Gender</label>
        <select id="gender" v-model="bio.gender" required>
          <option disabled value="">Select gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Appearance -->
      <div class="form-group">
        <label for="appearance">Appearance</label>
        <textarea
            id="appearance"
            v-model="bio.appearance"
            placeholder="Describe the character's appearance"
        ></textarea>
      </div>

      <!-- Background -->
      <div class="form-group">
        <label for="background">Background</label>
        <textarea
            id="background"
            v-model="bio.background"
            placeholder="Provide the character's background"
        ></textarea>
      </div>
    </form>
  </div>
</template>


<script>
export default {
  name: "BioComponent",
  props: {
    name: {
      type: String,
      default: "",
    },
    age: {
      type: Number,
      default: null,
    },
    gender: {
      type: String,
      default: "",
    },
    appearance: {
      type: String,
      default: "",
    },
    background: {
      type: String,
      default: "",
    },
    setPlayerName: {
      type: Function,
      required: true,
    },
    setPlayerAge: {
      type: Function,
      required: true,
    },
    setPlayerGender: {
      type: Function,
      required: true,
    },
    setPlayerAppearance: {
      type: Function,
      required: true,
    },
    setPlayerBackground: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      bio: {
        name: this.name,
        age: this.age,
        gender: this.gender,
        appearance: this.appearance,
        background: this.background,
      },
    };
  },
  watch: {
    bio: {
      deep: true,
      handler(newBio) {
        this.setPlayerName(newBio.name);
        this.setPlayerAge(newBio.age);
        this.setPlayerGender(newBio.gender);
        this.setPlayerAppearance(newBio.appearance);
        this.setPlayerBackground(newBio.background);
      },
    },
  },
  methods: {
    submitBio() {
      this.$emit("next");
    },
  },
};
</script>


<style scoped>
.bio-component {
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
}

h2 {
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
textarea,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #fff;
}

textarea {
  resize: vertical;
}

input::placeholder,
textarea::placeholder {
  color: #aaa;
}

.form-actions {
  text-align: center;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #2196f3;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1976d2;
}
</style>
