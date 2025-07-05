<template>
  <div class="character-template-editor">
    <!-- Top Row (1) -->
    <div class="top-row">
      <h1>Character Template Editor</h1>
      <div class="toolbar">
        <button class="save-btn" @click="saveTemplate" :disabled="isLoading">Save Template</button>
        <button class="cancel-btn" @click="cancelEditing" :disabled="isLoading">Cancel</button>
      </div>
    </div>

    <!-- Center Row (8) -->
    <div class="center-row">
      <!-- Center Column (2) -->
      <div class="center-column">
        <!-- Loading overlay -->
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-spinner"></div>
          <p>Loading...</p>
        </div>

        <!-- Error message -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- Validation errors -->
        <div v-if="validationErrors.length > 0" class="validation-errors">
          <h4>Validation Errors:</h4>
          <ul>
            <li v-for="(error, index) in validationErrors" :key="index">
              {{ error.message }}
            </li>
          </ul>
        </div>

        <!-- This column is divided into 1,8 for columns -->
        <div class="center-content">
          <!-- Left part (1) -->
          <div class="template-list">
            <NPCTemplatesList
              class="npc-templates-list"
              title="Available Templates"
              @template-selected="onNPCTemplateSelected"
            />
          </div>

          <!-- Right part (8) -->
          <div class="template-editor" v-if="template">
            <CharacterTemplateDetail
              :template="template"
              :service="service"
              @update="onTemplateUpdate"
            />
          </div>
        </div>
      </div>

      <!-- Right Column (1) -->
      <div class="right-column">
        <div class="sidebar-section">
          <h3>Preview</h3>
          <div class="preview-card" v-if="template">
            <h4>{{ template.data.name || 'Unnamed Template' }}</h4>
            <div class="preview-image">
              [Character Image Placeholder]
            </div>
            <div class="preview-stats">
              <p v-for="stat in template.data.stats" :key="stat.name">
                {{ stat.name.substring(0, 3).toUpperCase() }}: {{ stat.value }}
              </p>
            </div>
            <div class="preview-tags" v-if="template.data.tags.length > 0">
              <span v-for="(tag, index) in template.data.tags" :key="index" class="preview-tag">
                {{ tag }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Bottom Row (1) -->
    <div class="bottom-row">
      <div class="status-bar">
        <span>Last saved: {{ lastSaved ? lastSaved.toLocaleString() : 'Never' }}</span>
        <span>Status: {{ isDirty ? 'Unsaved Changes' : 'Saved' }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { characterTemplateEditorService } from '@/services/CharacterTemplateEditorService.js';
import { characterTemplatesService } from '@/services/CharacterTemplatesService.js';
import { createSampleCharacterTemplate } from '@/models/CharacterTemplateFull.js';
import NPCTemplatesList from '@/components/shared/NPCTemplatesList.vue';
import CharacterTemplateDetail from '@/components/GameMaster/CharacterTemplateDetail.vue';

export default {
  name: 'CharacterTemplateEditor',
  components: {
    NPCTemplatesList,
    CharacterTemplateDetail
  },
  data() {
    return {
      service: characterTemplateEditorService,
      templatesService: characterTemplatesService,
      template: null,
      availableTemplates: [],
      isLoading: false,
      error: null,
      lastSaved: null,
      isDirty: false,
      validationErrors: []
    };
  },
  computed: {
    filteredTemplates() {
      return this.availableTemplates;
    },
    totalStatsPoints() {
      if (!this.template) return 0;
      return this.template.data.stats.reduce((sum, stat) => sum + stat.value, 0);
    },
    maxStatsPoints() {
      if (!this.template) return 100;
      return this.template.validation.max_stats_points_count;
    }
  },
  async created() {
    // Set up event listeners
    this.service.on('templateLoaded', this.onTemplateLoaded);
    this.service.on('templateUpdated', this.onTemplateUpdated);
    this.service.on('loadingFailed', this.onLoadingFailed);
    this.service.on('validationError', this.onValidationError);
    this.service.on('dirtyStateChanged', this.onDirtyStateChanged);

    // Initialize the service
    await this.service.initialize();

    // Load available templates
    await this.loadAvailableTemplates();

    // Load a sample template for now
    this.template = createSampleCharacterTemplate();
  },
  beforeUnmount() {
    // Clean up event listeners
    this.service.off('templateLoaded', this.onTemplateLoaded);
    this.service.off('templateUpdated', this.onTemplateUpdated);
    this.service.off('loadingFailed', this.onLoadingFailed);
    this.service.off('validationError', this.onValidationError);
    this.service.off('dirtyStateChanged', this.onDirtyStateChanged);
  },
  methods: {
    async loadAvailableTemplates() {
      try {
        this.isLoading = true;
        await this.templatesService.initialize();
        this.availableTemplates = this.templatesService.getTemplates();
        this.isLoading = false;
      } catch (error) {
        console.error('Failed to load available templates:', error);
        this.error = 'Failed to load available templates';
        this.isLoading = false;
      }
    },

    async importFromTemplate(templateId) {
      try {
        this.isLoading = true;
        this.error = null;
        this.validationErrors = [];

        await this.service.importFromTemplate(templateId);
        this.isLoading = false;
      } catch (error) {
        console.error('Failed to import template:', error);
        this.error = 'Failed to import template';
        this.isLoading = false;
      }
    },


    selectTemplate(template) {
      if (template && template.id) {
        this.importFromTemplate(template.id);
      }
    },

    updateTemplateName(event) {
      this.service.setName(event.target.value);
    },

    updateStat(statName, event) {
      const value = parseInt(event.target.value, 10);
      if (!isNaN(value)) {
        this.service.updateStat(statName, value);
      }
    },

    saveTemplate() {
      // Validate the template
      const validation = this.service.validate();
      if (!validation.isValid) {
        this.validationErrors = validation.errors;
        return;
      }

      // Export the template
      const exportedTemplate = this.service.export();
      if (exportedTemplate) {
        this.lastSaved = new Date();
        this.isDirty = false;
        console.log('Template saved:', exportedTemplate);
      }
    },

    cancelEditing() {
      if (this.isDirty) {
        if (confirm('You have unsaved changes. Are you sure you want to cancel?')) {
          this.service.reset();
          this.template = this.service.getTemplate();
          this.isDirty = false;
        }
      } else {
        this.service.reset();
        this.template = this.service.getTemplate();
      }
    },

    // Event handlers
    onTemplateLoaded(template) {
      this.template = template;
      this.error = null;
      this.validationErrors = [];
    },

    onTemplateUpdated(template) {
      this.template = template;
    },

    onLoadingFailed(error) {
      console.error('Loading failed:', error);
      this.error = 'Failed to load template';
    },

    onValidationError(errors) {
      this.validationErrors = Array.isArray(errors) ? errors : [errors];
    },

    onDirtyStateChanged(isDirty) {
      this.isDirty = isDirty;
    },

    /**
     * Handle template updates from the CharacterTemplateDetail component
     */
    onTemplateUpdate() {
      // The template will be updated automatically through the service
      // No additional action needed here as the service handles state management
    },

    /**
     * Handle NPC template selection from the NPCTemplatesList component
     * @param {Object} template - The selected NPC template
     */
    onNPCTemplateSelected(template) {
      console.log('NPC template selected:', template);

      // If we already have a template loaded, ask for confirmation before replacing it
      if (this.template && this.isDirty) {
        if (!confirm('You have unsaved changes. Are you sure you want to load a new template?')) {
          return;
        }
      }

      // Import the template data
      if (template && template.id) {
        this.importFromTemplate(template.id);
      }
    }
  }
};
</script>

<style scoped>
.character-template-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background: #1e1e1e;
  color: #ffffff;
  font-family: 'Roboto', sans-serif;
  max-height: 100vh;
}

/* Top Row - 1 part of vertical layout */
.top-row {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #2d2d2d;
  border-bottom: 1px solid #444;
  min-height: 60px;
  color: white;
}

.toolbar {
  display: flex;
  gap: 1rem;
}

.toolbar button {
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn {
  background: #4CAF50;
  color: white;
}

.save-btn:hover {
  background: #3d8b40;
}

.cancel-btn {
  background: #f44336;
  color: white;
}

.cancel-btn:hover {
  background: #d32f2f;
}

/* Center Row - 8 parts of vertical layout */
.center-row {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.template-list h3, .template-editor h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}

.preview-card h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.sidebar-section h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

/* Center Column - 2 parts of horizontal layout */
.center-column {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #1e1e1e;
}

.center-content {
  display: flex;
  height: 100%;
}

/* Left part of center column - 1 part */
.template-list {
  width: 20rem;
  border-right: 1px solid #444;
  overflow-y: auto;
  background: #2d2d2d;
}

.template-item {
  padding: 10px;
  margin: 5px 0;
  background: #444;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.template-item:hover {
  background: #555;
}

/* Right part of center column - 8 parts */
.template-editor {
  flex: 8;
  padding: 20px;
  overflow-y: auto;
  background: #1e1e1e;
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
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.form-group input[type="text"]:focus,
.form-group input[type="number"]:focus,
.form-group textarea:focus {
  border-color: #1E90FF;
  outline: none;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item label {
  margin-bottom: 5px;
  color: #ccc;
}

.stat-item input {
  width: 100%;
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.stat-item input:focus {
  border-color: #1E90FF;
  outline: none;
}

/* Right Column - 1 part of horizontal layout */
.right-column {
  width: 300px;
  background: #2d2d2d;
  border-left: 1px solid #444;
  padding: 20px;
  overflow-y: auto;
}

.preview-card {
  background: #333;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  border: 1px solid #444;
}

.preview-image {
  height: 150px;
  background: #444;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px 0;
  border-radius: 4px;
  color: #ccc;
}

.preview-stats {
  font-size: 14px;
  color: #ccc;
}

.preview-stats p {
  margin: 5px 0;
}

.preview-tags {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.preview-tag {
  background: #444;
  color: #ccc;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* NPC Templates Section */
.npc-templates-section {
  margin-top: 20px;
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.npc-templates-list {
  flex: 1;
  min-height: 300px;
  max-height: 500px;
  border: 1px solid #444;
  border-radius: 4px;
  overflow: hidden;
}

/* Bottom Row - 1 part of vertical layout */
.bottom-row {
  height: 40px;
  background: #2d2d2d;
  color: white;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-top: 1px solid #444;
  min-height: 40px;
  font-size: 0.9rem;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.status-bar span {
  color: #ccc;
}

/* Loading overlay */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 100;
  color: white;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #1E90FF;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error message */
.error-message {
  background: #f44336;
  color: white;
  padding: 10px;
  margin: 10px;
  border-radius: 4px;
}

/* Validation errors */
.validation-errors {
  background: #ff9800;
  color: white;
  padding: 10px;
  margin: 10px;
  border-radius: 4px;
}

.validation-errors h4 {
  margin-top: 0;
  margin-bottom: 5px;
}

.validation-errors ul {
  margin: 0;
  padding-left: 20px;
}

/* No templates message */
.no-templates {
  padding: 10px;
  color: #ccc;
  font-style: italic;
}

/* Tags container */
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

/* Input hint */
.input-hint {
  font-size: 0.8rem;
  color: #ccc;
  margin-left: 5px;
}

/* Bio section */
.bio-section {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.bio-field {
  flex: 1;
}

.bio-field.full-width {
  width: 100%;
  margin-bottom: 10px;
}

.bio-field label {
  display: block;
  margin-bottom: 5px;
  color: #ccc;
}

/* Items, Schools, Spells lists */
.items-list, .schools-list, .spells-list {
  background: #333;
  border-radius: 4px;
  padding: 10px;
  margin-top: 5px;
}

.item, .school, .spell {
  background: #444;
  color: #fff;
  padding: 5px 10px;
  border-radius: 4px;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-remove, .school-remove, .spell-remove {
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
  font-size: 1.2rem;
}

.add-item, .add-school, .add-spell {
  margin-top: 5px;
}

.add-item input, .add-school input, .add-spell input {
  width: 100%;
  padding: 5px;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
}
</style>