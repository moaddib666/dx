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
  padding: 2rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect */
.bio-component::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 8s ease-in-out infinite;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

h2 {
  margin-bottom: 2rem;
  text-align: center;
  font-size: 1.8rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  position: relative;
  z-index: 2;
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 2;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1rem;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.25rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(2px);
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.05);
  box-shadow: 0 0 10px rgba(127, 255, 22, 0.2);
}

input:hover,
textarea:hover,
select:hover {
  border-color: rgba(127, 255, 22, 0.5);
  background: rgba(127, 255, 22, 0.02);
}

textarea {
  resize: vertical;
  min-height: 100px;
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

.form-actions {
  text-align: center;
  position: relative;
  z-index: 2;
}

button {
  padding: 0.75rem 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 25px;
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.1), rgba(127, 255, 22, 0.1));
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(2px);
}

button:hover {
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.2), rgba(127, 255, 22, 0.2));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
  border-color: #7fff16;
}

button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 5px rgba(127, 255, 22, 0.2);
}
</style>
