<template>
  <div class="abilities-tab">
    <h3>Schools & Spells Management</h3>
    
    <div v-if="!allSchools || !allSpells" class="loading-placeholder">
      <p>Loading schools and spells data...</p>
    </div>

    <div v-else class="abilities-management">
      <!-- Path Info -->
      <div class="path-info" v-if="characterPath">
        <h4>Character Path: {{ characterPath.name || template.data.path }}</h4>
        <p>Rank: {{ template.data.rank }} ({{ rankDescription }})</p>
      </div>

      <!-- School Management -->
      <div class="school-management">
        <h4>Schools ({{ nonBaseSchools.length }}/{{ template.validation.max_schools_count }} + {{ baseSchools.length }} base)</h4>
        
        <!-- Current Schools -->
        <div class="current-schools" v-if="template.data.schools.length > 0">
          <div class="school-grid">
            <div 
              v-for="schoolId in template.data.schools" 
              :key="schoolId"
              class="current-school-item"
              @click="removeSchool(schoolId)"
              :class="{ 
                'base-item': getSchoolById(schoolId)?.is_base || getSchoolById(schoolId)?.is_default,
                'non-removable': getSchoolById(schoolId)?.is_base || getSchoolById(schoolId)?.is_default
              }"
            >
              <img 
                v-if="getSchoolById(schoolId)?.icon" 
                :src="getSchoolById(schoolId).icon" 
                :alt="getSchoolById(schoolId)?.name"
                class="school-icon"
              />
              <div class="school-name">{{ getSchoolById(schoolId)?.name || schoolId }}</div>
              <div v-if="!(getSchoolById(schoolId)?.is_base || getSchoolById(schoolId)?.is_default)" class="remove-indicator">×</div>
              <div v-else class="base-indicator">BASE</div>
            </div>
          </div>
        </div>

        <!-- Available Schools -->
        <div class="available-schools" v-if="availableSchools.length > 0">
          <h5>Available Schools</h5>
          <div class="school-grid">
            <div 
              v-for="school in availableSchools" 
              :key="school.id"
              class="available-school-item"
              @click="addSchool(school.id)"
              :class="{ disabled: nonBaseSchools.length >= template.validation.max_schools_count }"
            >
              <img 
                v-if="school.icon" 
                :src="school.icon" 
                :alt="school.name"
                class="school-icon"
              />
              <div class="school-name">{{ school.name }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Spell Management -->
      <div class="spell-management" v-if="template.data.schools.length > 0">
        <h4>Spells ({{ nonBaseSpells.length }}/{{ template.validation.max_spells_count }} + {{ baseSkills.length }} base)</h4>
        
        <!-- Current Spells -->
        <div class="current-spells" v-if="template.data.spells.length > 0">
          <div class="spell-grid">
            <div 
              v-for="spellId in template.data.spells" 
              :key="spellId"
              class="current-spell-item"
              @click="removeSpell(spellId)"
              :class="{ 
                'base-item': getSpellById(spellId)?.is_base || getSpellById(spellId)?.is_default,
                'non-removable': getSpellById(spellId)?.is_base || getSpellById(spellId)?.is_default
              }"
            >
              <SkillIcon :skill="getSpellById(spellId)" v-if="getSpellById(spellId)" />
              <div class="spell-name">{{ getSpellById(spellId)?.name || spellId }}</div>
              <div v-if="!(getSpellById(spellId)?.is_base || getSpellById(spellId)?.is_default)" class="remove-indicator">×</div>
              <div v-else class="base-indicator">BASE</div>
            </div>
          </div>
        </div>

        <!-- Available Spells by School -->
        <div class="available-spells">
          <div 
            v-for="schoolId in template.data.schools" 
            :key="schoolId"
            class="spell-group"
          >
            <h5>{{ getSchoolById(schoolId)?.name || schoolId }} Spells</h5>
            <div class="spell-grid">
              <div 
                v-for="spell in getAvailableSpellsForSchool(schoolId)" 
                :key="spell.id"
                class="available-spell-item"
                @click="addSpell(spell.id)"
                :class="{ 
                  disabled: spell.grade < template.data.rank || nonBaseSpells.length >= template.validation.max_spells_count,
                  weak: spell.grade < template.data.rank
                }"
              >
                <SkillIcon :skill="spell" :fade="spell.grade < template.data.rank" />
                <div class="spell-name">{{ spell.name }}</div>
                <div class="spell-grade">Grade {{ spell.grade }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Management Summary -->
      <div class="abilities-summary">
        <div class="summary-grid">
          <div class="summary-card">
            <h4>Schools Summary</h4>
            <div class="summary-stats">
              <div class="stat-row">
                <span>Current Schools:</span>
                <span>{{ template.data.schools.length }}/{{ template.validation.max_schools_count }}</span>
              </div>
              <div class="stat-row">
                <span>Available:</span>
                <span>{{ availableSchools.length }}</span>
              </div>
            </div>
          </div>

          <div class="summary-card">
            <h4>Spells Summary</h4>
            <div class="summary-stats">
              <div class="stat-row">
                <span>Current Spells:</span>
                <span>{{ template.data.spells.length }}/{{ template.validation.max_spells_count }}</span>
              </div>
              <div class="stat-row">
                <span>Character Rank:</span>
                <span>{{ template.data.rank }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SkillIcon from "@/components/Action/ActionIcon.vue";
import { SchoolGameApi } from "@/api/backendService.js";

export default {
  name: 'AbilitiesTab',
  components: {
    SkillIcon
  },
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
      allSchools: null,
      allSpells: null,
      allPaths: null,
      isLoading: false
    };
  },
  computed: {
    characterPath() {
      if (!this.allPaths || !this.template.data.path) return null;
      return this.allPaths.find(path => path.id === this.template.data.path);
    },
    rankDescription() {
      const rank = this.template.data.rank;
      if (rank === 0) return "Top Dog";
      if (rank <= 2) return "Elite";
      if (rank <= 5) return "Experienced";
      if (rank <= 7) return "Competent";
      return "Beginner";
    },
    baseSchools() {
      if (!this.allSchools) return [];
      return this.allSchools.filter(school => school.is_base || school.is_default);
    },
    baseSkills() {
      if (!this.allSpells) return [];
      return this.allSpells.filter(spell => spell.is_base || spell.is_default);
    },
    nonBaseSchools() {
      return this.template.data.schools.filter(schoolId => {
        const school = this.getSchoolById(schoolId);
        return school && !school.is_base && !school.is_default;
      });
    },
    nonBaseSpells() {
      return this.template.data.spells.filter(spellId => {
        const spell = this.getSpellById(spellId);
        return spell && !spell.is_base && !spell.is_default;
      });
    },
    availableSchools() {
      if (!this.allSchools || !this.template.data.path) return [];
      
      return this.allSchools.filter(school => {
        // Only non-base schools from character's path and not already selected
        const isFromPath = school.path && school.path.includes(this.template.data.path);
        const notSelected = !this.template.data.schools.includes(school.id);
        const notBase = !school.is_base && !school.is_default;
        
        return isFromPath && notSelected && notBase;
      });
    }
  },
  async mounted() {
    await this.loadSchoolsAndSpells();
  },
  methods: {
    async loadSchoolsAndSpells() {
      if (this.isLoading) return;
      
      try {
        this.isLoading = true;
        
        // Load schools, spells, and paths in parallel
        const [schoolsResponse, spellsResponse, pathsResponse] = await Promise.all([
          SchoolGameApi.schoolSchoolsGetAllSchoolsRetrieve(),
          SchoolGameApi.schoolSchoolsGetAllSkillsRetrieve(),
          SchoolGameApi.schoolPathsGetAllPathsRetrieve()
        ]);
        
        this.allSchools = schoolsResponse.data || [];
        this.allSpells = spellsResponse.data || [];
        this.allPaths = pathsResponse.data || [];
        
        console.log('Loaded schools:', this.allSchools.length);
        console.log('Loaded spells:', this.allSpells.length);
        console.log('Loaded paths:', this.allPaths.length);
        
        // Auto-add base schools and skills if not already present
        await this.ensureBaseSchoolsAndSkills();
        
      } catch (error) {
        console.error('Failed to load schools and spells:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    async ensureBaseSchoolsAndSkills() {
      let hasChanges = false;
      
      // Add missing base schools
      for (const school of this.baseSchools) {
        if (!this.template.data.schools.includes(school.id)) {
          console.log('Auto-adding base school:', school.name);
          this.service.addSchool(school.id);
          hasChanges = true;
        }
      }
      
      // Add missing base skills
      for (const skill of this.baseSkills) {
        if (!this.template.data.spells.includes(skill.id)) {
          console.log('Auto-adding base skill:', skill.name);
          this.service.addSpell(skill.id);
          hasChanges = true;
        }
      }
      
      if (hasChanges) {
        this.$emit('update');
      }
    },
    
    getSchoolById(schoolId) {
      if (!this.allSchools) return null;
      return this.allSchools.find(school => school.id === schoolId);
    },
    
    getSpellById(spellId) {
      if (!this.allSpells) return null;
      return this.allSpells.find(spell => spell.id === spellId);
    },
    
    getAvailableSpellsForSchool(schoolId) {
      if (!this.allSpells) return [];
      
      return this.allSpells.filter(spell => {
        const isFromSchool = spell.school === schoolId;
        const notSelected = !this.template.data.spells.includes(spell.id);
        
        return isFromSchool && notSelected;
      });
    },
    
    addSchool(schoolId) {
      if (!schoolId) return;
      
      const school = this.getSchoolById(schoolId);
      if (!school) {
        console.warn('School not found:', schoolId);
        return;
      }
      
      // Don't count base schools toward the limit
      if (!school.is_base && !school.is_default) {
        // Check if we've reached the maximum for non-base schools
        if (this.nonBaseSchools.length >= this.template.validation.max_schools_count) {
          console.warn('Maximum non-base schools reached');
          return;
        }
      }
      
      // Check if school is valid (from character's path)
      if (!school.path || !school.path.includes(this.template.data.path)) {
        console.warn('School not from character path:', schoolId);
        return;
      }
      
      this.service.addSchool(schoolId);
      this.$emit('update');
    },
    
    removeSchool(schoolId) {
      const school = this.getSchoolById(schoolId);
      
      // Prevent removal of base schools
      if (school && (school.is_base || school.is_default)) {
        console.warn('Cannot remove base school:', school.name);
        return;
      }
      
      this.service.removeSchool(schoolId);
      
      // Remove all spells from this school when school is removed (except base spells)
      const spellsToRemove = this.allSpells
        .filter(spell => 
          spell.school === schoolId && 
          this.template.data.spells.includes(spell.id) &&
          !spell.is_base && 
          !spell.is_default
        )
        .map(spell => spell.id);
      
      spellsToRemove.forEach(spellId => {
        this.service.removeSpell(spellId);
      });
      
      this.$emit('update');
    },
    
    addSpell(spellId) {
      if (spellId === undefined || spellId === null) return;
      
      const spell = this.getSpellById(spellId);
      if (!spell) {
        console.warn('Spell not found:', spellId);
        return;
      }
      
      // Don't count base spells toward the limit
      if (!spell.is_base && !spell.is_default) {
        // Check if we've reached the maximum for non-base spells
        if (this.nonBaseSpells.length >= this.template.validation.max_spells_count) {
          console.warn('Maximum non-base spells reached');
          return;
        }
      }
      
      // Check rank restriction (spell grade must be >= character rank)
      if (spell.grade < this.template.data.rank) {
        console.warn('Spell grade too low for character rank:', spell.grade, 'vs', this.template.data.rank);
        return;
      }
      
      // Check if spell's school is learned
      if (!this.template.data.schools.includes(spell.school)) {
        console.warn('Spell school not learned:', spell.school);
        return;
      }
      
      this.service.addSpell(spellId);
      this.$emit('update');
    },
    
    removeSpell(spellId) {
      const spell = this.getSpellById(spellId);
      
      // Prevent removal of base spells
      if (spell && (spell.is_base || spell.is_default)) {
        console.warn('Cannot remove base spell:', spell.name);
        return;
      }
      
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

.loading-placeholder {
  text-align: center;
  padding: 40px;
  color: #ccc;
}

.abilities-management {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.path-info {
  background: #2d2d2d;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #444;
}

.path-info h4 {
  color: #1E90FF;
  margin: 0 0 10px 0;
}

.path-info p {
  color: #ccc;
  margin: 0;
}

.school-management, .spell-management {
  background: #333;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #444;
}

.school-management h4, .spell-management h4 {
  color: #1E90FF;
  margin: 0 0 20px 0;
}

.school-management h5, .spell-management h5 {
  color: #fff;
  margin: 15px 0 10px 0;
  font-size: 1rem;
}

/* Grid layouts for schools and spells */
.school-grid, .spell-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

/* Current school items (removable) */
.current-school-item {
  background: #444;
  border: 2px solid #555;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.current-school-item:hover:not(.non-removable) {
  border-color: #f44336;
  background: #4a2626;
}

.current-school-item.base-item {
  background: #2d4a33;
  border-color: #4CAF50;
}

.current-school-item.non-removable {
  cursor: not-allowed;
}

.current-school-item .remove-indicator {
  position: absolute;
  top: 5px;
  right: 5px;
  color: #f44336;
  font-size: 1.2rem;
  font-weight: bold;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.current-school-item:hover .remove-indicator {
  opacity: 1;
}

.base-indicator {
  position: absolute;
  top: 5px;
  right: 5px;
  color: #4CAF50;
  font-size: 0.6rem;
  font-weight: bold;
  background: rgba(76, 175, 80, 0.2);
  padding: 2px 4px;
  border-radius: 3px;
}

/* Available school items (addable) */
.available-school-item {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #555;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.available-school-item:hover:not(.disabled) {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.2);
  transform: translateY(-2px);
}

.available-school-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* School icons and names */
.school-icon {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
}

.school-name {
  font-size: 0.8rem;
  color: #fff;
  line-height: 1.2;
  word-wrap: break-word;
}

/* Current spell items (removable) */
.current-spell-item {
  background: #444;
  border: 2px solid #555;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.current-spell-item:hover:not(.non-removable) {
  border-color: #f44336;
  background: #4a2626;
}

.current-spell-item.base-item {
  background: #2d4a33;
  border-color: #4CAF50;
}

.current-spell-item.non-removable {
  cursor: not-allowed;
}

.current-spell-item .remove-indicator {
  position: absolute;
  top: 5px;
  right: 5px;
  color: #f44336;
  font-size: 1.2rem;
  font-weight: bold;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.current-spell-item:hover .remove-indicator {
  opacity: 1;
}

/* Available spell items (addable) */
.available-spell-item {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #555;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.available-spell-item:hover:not(.disabled) {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.2);
  transform: translateY(-2px);
}

.available-spell-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.available-spell-item.weak {
  opacity: 0.3;
  border-color: #666;
}

.available-spell-item.weak:hover {
  border-color: #666;
  background: rgba(255, 255, 255, 0.05);
  transform: none;
}

/* Spell names and grades */
.spell-name {
  font-size: 0.8rem;
  color: #fff;
  line-height: 1.2;
  word-wrap: break-word;
  margin-top: 5px;
}

.spell-grade {
  font-size: 0.7rem;
  color: #aaa;
  margin-top: 2px;
}

/* Spell groups */
.spell-group {
  margin-bottom: 25px;
}

.spell-group:last-child {
  margin-bottom: 0;
}

/* Summary section */
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
  border-radius: 8px;
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
  font-size: 1.3rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .school-grid, .spell-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }
  
  .school-icon {
    width: 50px;
    height: 50px;
  }
  
  .school-name, .spell-name {
    font-size: 0.7rem;
  }
}
</style>