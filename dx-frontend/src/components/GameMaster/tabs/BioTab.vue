<template>
  <div class="bio-tab">
    <h3>Character Biography</h3>

    <div class="bio-section">
      <div class="bio-field">
        <label>Age</label>
        <input
          type="number"
          :value="template.data.bio.age"
          @input="updateAge"
          min="1"
        />
      </div>
      <div class="bio-field">
        <label>Gender</label>
        <input
          type="text"
          :value="template.data.bio.gender"
          @input="updateGender"
        />
      </div>
    </div>

    <div class="bio-field full-width">
      <label>Appearance</label>
      <textarea
        :value="template.data.bio.appearance"
        @input="updateAppearance"
        placeholder="Enter character appearance"
        rows="4"
      ></textarea>
    </div>

    <div class="bio-field full-width">
      <label>Background</label>
      <textarea
        :value="template.data.bio.background"
        @input="updateBackground"
        placeholder="Enter character background"
        rows="6"
      ></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BioTab',
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  methods: {
    updateAge(event) {
      this.service.setBio({
        ...this.template.data.bio,
        age: parseInt(event.target.value, 10)
      });
      this.$emit('update');
    },
    updateGender(event) {
      this.service.setBio({
        ...this.template.data.bio,
        gender: event.target.value
      });
      this.$emit('update');
    },
    updateAppearance(event) {
      this.service.setBio({
        ...this.template.data.bio,
        appearance: event.target.value
      });
      this.$emit('update');
    },
    updateBackground(event) {
      this.service.setBio({
        ...this.template.data.bio,
        background: event.target.value
      });
      this.$emit('update');
    }
  }
};
</script>

<style scoped>
.bio-tab {
  padding: 20px 0;
}

.bio-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.bio-field {
  flex: 1;
  margin-bottom: 20px;
}

.bio-field.full-width {
  width: 100%;
}

.bio-field label {
  display: block;
  margin-bottom: 5px;
  color: #ccc;
  font-weight: bold;
}

.bio-field input,
.bio-field textarea {
  width: 100%;
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
  resize: vertical;
}

.bio-field input:focus,
.bio-field textarea:focus {
  border-color: #1E90FF;
  outline: none;
}

.bio-field textarea {
  font-family: inherit;
  line-height: 1.4;
}

h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}
</style>