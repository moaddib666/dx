<template>
  <div class="abilities-tab">
    <h3>Schools & Spells</h3>

    <div class="abilities-section">
      <div class="form-group">
        <label>Schools ({{ template.data.schools.length }}/{{ template.validation.max_schools_count }})</label>
        <div class="schools-list">
          <div v-for="(schoolId, index) in template.data.schools" :key="index" class="school">
            <span class="school-id">{{ schoolId }}</span>
            <button class="school-remove" @click="removeSchool(schoolId)">×</button>
          </div>
          <div v-if="template.data.schools.length < template.validation.max_schools_count" class="add-school">
            <input
              type="text"
              placeholder="Add school ID"
              v-model="newSchoolId"
              @keydown.enter="addSchool"
            />
            <button class="add-button" @click="addSchool">Add</button>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>Spells ({{ template.data.spells.length }}/{{ template.validation.max_spells_count }})</label>
        <div class="spells-list">
          <div v-for="(spellId, index) in template.data.spells" :key="index" class="spell">
            <span class="spell-id">{{ spellId }}</span>
            <button class="spell-remove" @click="removeSpell(spellId)">×</button>
          </div>
          <div v-if="template.data.spells.length < template.validation.max_spells_count" class="add-spell">
            <input
              type="number"
              placeholder="Add spell ID"
              v-model="newSpellId"
              @keydown.enter="addSpell"
            />
            <button class="add-button" @click="addSpell">Add</button>
          </div>
        </div>
      </div>
    </div>

    <div class="abilities-summary">
      <div class="summary-grid">
        <div class="summary-card">
          <h4>Schools Summary</h4>
          <div class="summary-stats">
            <div class="stat-row">
              <span>Total Schools:</span>
              <span>{{ template.data.schools.length }}</span>
            </div>
            <div class="stat-row">
              <span>Max Schools:</span>
              <span>{{ template.validation.max_schools_count }}</span>
            </div>
            <div class="stat-row">
              <span>Remaining Slots:</span>
              <span>{{ template.validation.max_schools_count - template.data.schools.length }}</span>
            </div>
          </div>
        </div>

        <div class="summary-card">
          <h4>Spells Summary</h4>
          <div class="summary-stats">
            <div class="stat-row">
              <span>Total Spells:</span>
              <span>{{ template.data.spells.length }}</span>
            </div>
            <div class="stat-row">
              <span>Max Spells:</span>
              <span>{{ template.validation.max_spells_count }}</span>
            </div>
            <div class="stat-row">
              <span>Remaining Slots:</span>
              <span>{{ template.validation.max_spells_count - template.data.spells.length }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AbilitiesTab',
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
      newSchoolId: '',
      newSpellId: null
    };
  },
  methods: {
    addSchool() {
      if (this.newSchoolId.trim()) {
        this.service.addSchool(this.newSchoolId.trim());
        this.newSchoolId = '';
        this.$emit('update');
      }
    },
    removeSchool(schoolId) {
      this.service.removeSchool(schoolId);
      this.$emit('update');
    },
    addSpell() {
      if (this.newSpellId !== null && this.newSpellId !== '') {
        this.service.addSpell(parseInt(this.newSpellId, 10));
        this.newSpellId = null;
        this.$emit('update');
      }
    },
    removeSpell(spellId) {
      this.service.removeSpell(spellId);
      this.$emit('update');
    }
  }
};
</script>

<style scoped>
.abilities-tab {
  padding: 20px 0;
}

.abilities-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #ccc;
}

.schools-list, .spells-list {
  background: #333;
  border-radius: 4px;
  padding: 15px;
  margin-top: 10px;
  border: 1px solid #444;
}

.school, .spell {
  background: #444;
  color: #fff;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.school-id, .spell-id {
  font-family: monospace;
  font-size: 0.9rem;
}

.school-remove, .spell-remove {
  background: none;
  border: none;
  color: #f44336;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  margin: 0;
  transition: color 0.3s ease;
}

.school-remove:hover, .spell-remove:hover {
  color: #ff5252;
}

.add-school, .add-spell {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.add-school input, .add-spell input {
  flex: 1;
  padding: 8px;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
}

.add-school input:focus, .add-spell input:focus {
  border-color: #1E90FF;
  outline: none;
}

.add-button {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background: #45a049;
}

.abilities-summary {
  margin-top: 30px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.summary-card {
  background: #2d2d2d;
  padding: 20px;
  border-radius: 4px;
  border: 1px solid #444;
}

.summary-card h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  color: #ccc;
}

.stat-row span:last-child {
  font-weight: bold;
  color: #fff;
}

h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}
</style>