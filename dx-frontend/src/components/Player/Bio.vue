<template>
  <div class="bio-component">
    <h2>{{ t('playerComponents.bio.title') }}</h2>
    <form @submit.prevent="submitBio">
      <!-- Name -->
      <div class="form-group">
        <label for="name">{{ t('playerComponents.bio.name') }}</label>
        <input
            id="name"
            v-model="bio.name"
            :placeholder="t('playerComponents.bio.namePlaceholder')"
            required
            type="text"
        />
      </div>

      <!-- Age -->
      <div class="form-group">
        <label for="age">{{ t('playerComponents.bio.age') }}</label>
        <input
            id="age"
            v-model.number="bio.age"
            min="1"
            :placeholder="t('playerComponents.bio.agePlaceholder')"
            required
            type="number"
        />
      </div>

      <!-- Gender -->
      <div class="form-group">
        <label for="gender">{{ t('playerComponents.bio.gender') }}</label>
        <select id="gender" v-model="bio.gender" required>
          <option disabled value="">{{ t('playerComponents.bio.genderSelect') }}</option>
          <option value="Male">{{ t('playerComponents.bio.male') }}</option>
          <option value="Female">{{ t('playerComponents.bio.female') }}</option>
          <option value="Other">{{ t('playerComponents.bio.other') }}</option>
        </select>
      </div>

      <!-- Appearance -->
      <div class="form-group">
        <label for="appearance">{{ t('playerComponents.bio.appearance') }}</label>
        <textarea
            id="appearance"
            v-model="bio.appearance"
            :placeholder="t('playerComponents.bio.appearancePlaceholder')"
        ></textarea>
      </div>

      <!-- Background -->
      <div class="form-group">
        <label for="background">{{ t('playerComponents.bio.background') }}</label>
        <textarea
            id="background"
            v-model="bio.background"
            :placeholder="t('playerComponents.bio.backgroundPlaceholder')"
        ></textarea>
      </div>
    </form>
  </div>
</template>


<script>
import { useI18n } from 'vue-i18n';

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
  setup() {
    const { t } = useI18n();
    return { t };
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
