<template>
  <div class="bio-component">
    <h2>{{ t('playerComponents.bio.title') }}</h2>
    <form @submit.prevent="submitBio">
      <div class="form-grid">
        <div class="left-col">
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
        </div>
        <div class="right-col">
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
        </div>
      </div>
    </form>
  </div>
</template>


<script>
import {useI18n} from 'vue-i18n';

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
    const {t} = useI18n();
    return {t};
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
/* Bio Component - Responsive */
.bio-component {
  padding: 1rem;
  border-radius: 0.5rem;
  background: transparent;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* Responsive padding */
@media (min-width: 768px) {
  .bio-component {
    padding: 1.5rem;
    margin: 0 auto;
  }
}

@media (min-width: 1024px) {
  .bio-component {
    padding: 2rem;
  }
}

h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

/* Responsive heading */
@media (min-width: 768px) {
  h2 {
    font-size: 1.75rem;
    margin-bottom: 2rem;
  }
}

.form-group {
  margin-bottom: 1rem;
  width: 100%;
}

/* Responsive form spacing */
@media (min-width: 768px) {
  .form-group {
    margin-bottom: 1.5rem;
  }
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
}

/* Responsive label sizing */
@media (min-width: 768px) {
  label {
    font-size: 1rem;
  }
}

input,
textarea,
select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.25rem;
  background: rgba(0, 0, 0, 0.3);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

/* Responsive input sizing */
@media (min-width: 768px) {
  input,
  textarea,
  select {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: rgba(127, 255, 22, 0.6);
}

input:hover,
textarea:hover,
select:hover {
  border-color: rgba(127, 255, 22, 0.5);
}

textarea {
  resize: vertical;
  min-height: 80px;
}

/* Responsive textarea sizing */
@media (min-width: 768px) {
  textarea {
    min-height: 100px;
  }
}

input::placeholder,
textarea::placeholder {
  color: rgba(250, 218, 149, 0.6);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

select option {
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.form-grid {
  display: flex;
  gap: 1rem;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
}
.left-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
}
.right-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 3;
}
</style>
