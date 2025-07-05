<template>
  <div class="basic-info-tab">
    <h3>Basic Information</h3>

    <div class="form-group">
      <label>Template Name</label>
      <input
        type="text"
        placeholder="Enter template name"
        :value="template.data.name"
        @input="updateTemplateName"
      />
    </div>

    <div class="form-group">
      <label>Tags</label>
      <div class="tags-container">
        <span v-for="(tag, index) in template.data.tags" :key="index" class="tag">
          {{ tag }}
          <button class="tag-remove" @click="service.removeTag(tag)">×</button>
        </span>
        <input
          type="text"
          placeholder="Add tag"
          class="tag-input"
          @keydown.enter="addTag"
          v-model="newTag"
        />
      </div>
    </div>

    <div class="form-group">
      <label>Rank</label>
      <input
        type="number"
        :value="template.data.rank"
        @input="updateRank"
        min="1"
        :max="template.validation.max_rank_grade"
      />
      <span class="input-hint">Max: {{ template.validation.max_rank_grade }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BasicInfoTab',
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
  data() {
    return {
      newTag: ''
    };
  },
  methods: {
    updateTemplateName(event) {
      this.service.setName(event.target.value);
      this.$emit('update');
    },
    updateRank(event) {
      this.service.setRank(parseInt(event.target.value, 10));
      this.$emit('update');
    },
    addTag() {
      if (this.newTag.trim()) {
        this.service.addTag(this.newTag.trim());
        this.newTag = '';
        this.$emit('update');
      }
    }
  }
};
</script>

<style scoped>
.basic-info-tab {
  padding: 20px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #ccc;
}

.form-group input[type="text"],
.form-group input[type="number"] {
  width: 100%;
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.form-group input[type="text"]:focus,
.form-group input[type="number"]:focus {
  border-color: #1E90FF;
  outline: none;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 5px;
}

.tag {
  background: #444;
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.tag-remove {
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0 0 0 5px;
  margin: 0;
}

.tag-input {
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 2px 6px;
  min-width: 100px;
}

.input-hint {
  font-size: 0.8rem;
  color: #ccc;
  margin-left: 5px;
}

h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}
</style>