import { GameMasterApi } from '@/api/backendService.js';
import { createEmptyCharacterTemplate } from '@/models/CharacterTemplateFull.js';
import { characterTemplatesService } from '@/services/CharacterTemplatesService.ts';
import skillService from '@/services/skillService';

/**
 * Character Template Editor Service
 * Handles editing, validation, and management of character templates
 */
export class CharacterTemplateEditorService {
    constructor() {
        this.template = createEmptyCharacterTemplate();
        this.isLoading = false;
        this.lastSaved = null;
        this.eventListeners = new Map();
        this.isDirty = false;
        this.previewData = null;
        this.isGeneratingPreview = false;
    }

    /**
     * Initialize the service
     */
    async initialize() {
        try {
            console.log('Initializing CharacterTemplateEditorService...');
            return true;
        } catch (error) {
            console.error('Failed to initialize CharacterTemplateEditorService:', error);
            throw error;
        }
    }

    /**
     * Import data from an existing template by ID
     * @param {string} templateId - The ID of the template to import
     */
    async importFromTemplate(templateId) {
        if (!templateId) {
            console.error('Template ID is required');
            return null;
        }

        if (this.isLoading) {
            console.log('Template already loading, waiting for completion...');
            return null;
        }

        try {
            this.isLoading = true;
            this.emit('loadingStarted', templateId);

            console.log(`Loading template ${templateId} from server...`);
            const response = await GameMasterApi.gamemasterCharacterTemplatesExportTemplateRetrieve(templateId);

            if (!response.data) {
                console.warn('Template API response is empty');
                return null;
            }

            // Convert the API response to our CharacterTemplateFull format
            this.template = this.convertApiResponseToTemplate(response.data);
            this.isDirty = false;

            // Ensure base schools and skills are added
            await this.ensureBaseSchoolsAndSkills();

            console.log(`Loaded template ${templateId}`);
            this.emit('templateLoaded', this.template);
            return this.template;
        } catch (error) {
            console.error(`Failed to load template ${templateId}:`, error);
            this.emit('loadingFailed', { templateId, error });
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Convert API response to CharacterTemplateFull format
     * @param {Object} apiResponse - The API response data
     * @returns {Object} - The converted template
     */
    convertApiResponseToTemplate(apiResponse) {
        return apiResponse || createEmptyCharacterTemplate();
    }

    /**
     * Get the current template
     * @returns {Object} - The current template
     */
    getTemplate() {
        return this.template;
    }

    /**
     * Set the template name
     * @param {string} name - The new template name
     */
    setName(name) {
        this.template.data.name = name;
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template name
     * @returns {string} - The template name
     */
    getName() {
        return this.template.data.name;
    }

    /**
     * Set the template tags
     * @param {string[]} tags - The new template tags
     */
    setTags(tags) {
        this.template.data.tags = [...tags];
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template tags
     * @returns {string[]} - The template tags
     */
    getTags() {
        return this.template.data.tags;
    }

    /**
     * Add a tag to the template
     * @param {string} tag - The tag to add
     */
    addTag(tag) {
        if (!tag) return;
        if (!this.template.data.tags.includes(tag)) {
            this.template.data.tags.push(tag);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Remove a tag from the template
     * @param {string} tag - The tag to remove
     */
    removeTag(tag) {
        const index = this.template.data.tags.indexOf(tag);
        if (index !== -1) {
            this.template.data.tags.splice(index, 1);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Set the template bio
     * @param {Object} bio - The new template bio
     */
    setBio(bio) {
        this.template.data.bio = { ...bio };
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template bio
     * @returns {Object} - The template bio
     */
    getBio() {
        return this.template.data.bio;
    }

    /**
     * Set the template rank
     * @param {number} rank - The new template rank
     */
    setRank(rank) {
        this.template.data.rank = rank;
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template rank
     * @returns {number} - The template rank
     */
    getRank() {
        return this.template.data.rank;
    }

    /**
     * Set the template path
     * @param {string} path - The new template path
     */
    setPath(path) {
        this.template.data.path = path;
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template path
     * @returns {string} - The template path
     */
    getPath() {
        return this.template.data.path;
    }

    /**
     * Set the template stats
     * @param {Object[]} stats - The new template stats
     */
    setStats(stats) {
        this.template.data.stats = [...stats];
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template stats
     * @returns {Object[]} - The template stats
     */
    getStats() {
        return this.template.data.stats;
    }

    /**
     * Update a specific stat
     * @param {string} statName - The name of the stat to update
     * @param {number} value - The new value for the stat
     */
    updateStat(statName, value) {
        const stat = this.template.data.stats.find(s => s.name === statName);
        if (stat) {
            stat.value = value;
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Set the template modificators
     * @param {Object[]} modificators - The new template modificators
     */
    setModificators(modificators) {
        this.template.data.modificators = [...modificators];
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template modificators
     * @returns {Object[]} - The template modificators
     */
    getModificators() {
        return this.template.data.modificators;
    }

    /**
     * Add a modificator to the template
     * @param {Object} modificator - The modificator to add
     */
    addModificator(modificator) {
        if (!modificator) return;

        // Check if we've reached the maximum number of modificators
        if (this.template.data.modificators.length >= this.template.validation.max_modificators_count) {
            console.warn(`Cannot add modificator: Maximum number of modificators (${this.template.validation.max_modificators_count}) reached`);
            this.emit('validationError', {
                type: 'modificators',
                message: `Maximum number of modificators (${this.template.validation.max_modificators_count}) reached`
            });
            return;
        }

        // Check if the modificator already exists
        const exists = this.template.data.modificators.some(m => m.id === modificator.id);
        if (!exists) {
            this.template.data.modificators.push(modificator);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Remove a modificator from the template
     * @param {string} modificatorId - The ID of the modificator to remove
     */
    removeModificator(modificatorId) {
        const index = this.template.data.modificators.findIndex(m => m.id === modificatorId);
        if (index !== -1) {
            this.template.data.modificators.splice(index, 1);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Set the template items
     * @param {string[]} items - The new template items
     */
    setItems(items) {
        this.template.data.items = [...items];
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template items
     * @returns {string[]} - The template items
     */
    getItems() {
        return this.template.data.items;
    }

    /**
     * Add an item to the template
     * @param {string} itemId - The ID of the item to add
     */
    addItem(itemId) {
        if (!itemId) return;

        // Check if we've reached the maximum number of items
        if (this.template.data.items.length >= this.template.validation.max_items_count) {
            console.warn(`Cannot add item: Maximum number of items (${this.template.validation.max_items_count}) reached`);
            this.emit('validationError', {
                type: 'items',
                message: `Maximum number of items (${this.template.validation.max_items_count}) reached`
            });
            return;
        }

        // Check if the item already exists
        if (!this.template.data.items.includes(itemId)) {
            this.template.data.items.push(itemId);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Remove an item from the template
     * @param {string} itemId - The ID of the item to remove
     */
    removeItem(itemId) {
        const index = this.template.data.items.indexOf(itemId);
        if (index !== -1) {
            this.template.data.items.splice(index, 1);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Set the template schools
     * @param {string[]} schools - The new template schools
     */
    setSchools(schools) {
        this.template.data.schools = [...schools];
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template schools
     * @returns {string[]} - The template schools
     */
    getSchools() {
        return this.template.data.schools;
    }

    /**
     * Add a school to the template
     * @param {string} schoolId - The ID of the school to add
     */
    addSchool(schoolId) {
        if (!schoolId) return;

        const school = skillService.getSchool(schoolId);
        if (!school) {
            console.warn('School not found:', schoolId);
            return;
        }

        // Only check limits for non-base schools
        if (!skillService.isBaseSchool(school)) {
            const nonBaseSchools = skillService.getNonBaseSchoolIds(this.template.data.schools);
            if (nonBaseSchools.length >= this.template.validation.max_schools_count) {
                console.warn(`Cannot add school: Maximum number of non-base schools (${this.template.validation.max_schools_count}) reached`);
                this.emit('validationError', {
                    type: 'schools',
                    message: `Maximum number of non-base schools (${this.template.validation.max_schools_count}) reached`
                });
                return;
            }
        }

        // Check if the school already exists
        if (!this.template.data.schools.includes(schoolId)) {
            this.template.data.schools.push(schoolId);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Remove a school from the template
     * @param {string} schoolId - The ID of the school to remove
     */
    removeSchool(schoolId) {
        const school = skillService.getSchool(schoolId);

        // Prevent removal of base schools
        if (skillService.isBaseSchool(school)) {
            console.warn('Cannot remove base school:', school?.name);
            return;
        }

        const index = this.template.data.schools.indexOf(schoolId);
        if (index !== -1) {
            this.template.data.schools.splice(index, 1);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Set the template spells
     * @param {number[]} spells - The new template spells
     */
    setSpells(spells) {
        this.template.data.spells = [...spells];
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the template spells
     * @returns {number[]} - The template spells
     */
    getSpells() {
        return this.template.data.spells;
    }

    /**
     * Add a spell to the template
     * @param {number} spellId - The ID of the spell to add
     */
    addSpell(spellId) {
        if (spellId === undefined || spellId === null) return;

        const spell = skillService.getSkill(spellId);
        if (!spell) {
            console.warn('Spell not found:', spellId);
            return;
        }

        // Only check limits for non-base spells
        if (!skillService.isBaseSpell(spell)) {
            const nonBaseSpells = skillService.getNonBaseSpellIds(this.template.data.spells);
            if (nonBaseSpells.length >= this.template.validation.max_spells_count) {
                console.warn(`Cannot add spell: Maximum number of non-base spells (${this.template.validation.max_spells_count}) reached`);
                this.emit('validationError', {
                    type: 'spells',
                    message: `Maximum number of non-base spells (${this.template.validation.max_spells_count}) reached`
                });
                return;
            }
        }

        // Check if the spell already exists
        if (!this.template.data.spells.includes(spellId)) {
            this.template.data.spells.push(spellId);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Remove a spell from the template
     * @param {number} spellId - The ID of the spell to remove
     */
    removeSpell(spellId) {
        const spell = skillService.getSkill(spellId);

        // Prevent removal of base spells
        if (skillService.isBaseSpell(spell)) {
            console.warn('Cannot remove base spell:', spell?.name);
            return;
        }

        const index = this.template.data.spells.indexOf(spellId);
        if (index !== -1) {
            this.template.data.spells.splice(index, 1);
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Set the validation rules
     * @param {Object} validation - The new validation rules
     */
    setValidation(validation) {
        this.template.validation = { ...validation };
        this.setDirty();
        this.emit('templateUpdated', this.template);
    }

    /**
     * Get the validation rules
     * @returns {Object} - The validation rules
     */
    getValidation() {
        return this.template.validation;
    }

    /**
     * Validate the current template against the validation rules
     * @returns {Object} - Validation result with errors if any
     */
    validate() {
        const errors = [];
        const validation = this.template.validation;

        // Check stats points total
        const totalStatsPoints = this.template.data.stats.reduce((sum, stat) => sum + stat.value, 0);
        if (totalStatsPoints > validation.max_stats_points_count) {
            errors.push({
                type: 'stats',
                message: `Total stats points (${totalStatsPoints}) exceeds maximum (${validation.max_stats_points_count})`
            });
        }

        // Check modificators count
        if (this.template.data.modificators.length > validation.max_modificators_count) {
            errors.push({
                type: 'modificators',
                message: `Modificators count (${this.template.data.modificators.length}) exceeds maximum (${validation.max_modificators_count})`
            });
        }

        // Check items count
        if (this.template.data.items.length > validation.max_items_count) {
            errors.push({
                type: 'items',
                message: `Items count (${this.template.data.items.length}) exceeds maximum (${validation.max_items_count})`
            });
        }

        // Check spells count (only non-base spells)
        const nonBaseSpells = skillService.getNonBaseSpellIds(this.template.data.spells);
        if (nonBaseSpells.length > validation.max_spells_count) {
            errors.push({
                type: 'spells',
                message: `Non-base spells count (${nonBaseSpells.length}) exceeds maximum (${validation.max_spells_count})`
            });
        }

        // Check rank
        if (this.template.data.rank > validation.max_rank_grade) {
            errors.push({
                type: 'rank',
                message: `Rank (${this.template.data.rank}) exceeds maximum (${validation.max_rank_grade})`
            });
        }

        // Check schools count (only non-base schools)
        const nonBaseSchools = skillService.getNonBaseSchoolIds(this.template.data.schools);
        if (nonBaseSchools.length > validation.max_schools_count) {
            errors.push({
                type: 'schools',
                message: `Non-base schools count (${nonBaseSchools.length}) exceeds maximum (${validation.max_schools_count})`
            });
        }

        // Check required fields
        if (!this.template.data.name) {
            errors.push({
                type: 'name',
                message: 'Template name is required'
            });
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Ensure all base schools and skills are added to the template
     * @returns {Promise<void>}
     */
    async ensureBaseSchoolsAndSkills() {
        let hasChanges = false;

        // Add missing base schools
        const baseSchools = skillService.getBaseSchools();
        for (const school of baseSchools) {
            if (!this.template.data.schools.includes(school.id)) {
                console.log('Auto-adding base school:', school.name);
                this.template.data.schools.push(school.id);
                hasChanges = true;
            }
        }

        // Add missing base skills
        const baseSkills = skillService.getBaseSkills();
        for (const skill of baseSkills) {
            if (!this.template.data.spells.includes(skill.id)) {
                console.log('Auto-adding base skill:', skill.name);
                this.template.data.spells.push(skill.id);
                hasChanges = true;
            }
        }

        if (hasChanges) {
            this.setDirty();
            this.emit('templateUpdated', this.template);
        }
    }

    /**
     * Export the current template
     * @returns {Object} - The exported template data
     */
    export() {
        // Validate the template before exporting
        const validation = this.validate();
        if (!validation.isValid) {
            console.warn('Template validation failed:', validation.errors);
            this.emit('validationError', validation.errors);
            return null;
        }

        // For now, just log the template data
        console.log('Exporting template:', JSON.stringify(this.template, null, 2));

        return this.template;
    }

    /**
     * Reset the template to an empty state
     */
    reset() {
        this.template = createEmptyCharacterTemplate();
        this.isDirty = false;
        this.lastSaved = null;
        this.previewData = null;
        console.log('CharacterTemplateEditorService reset');
        this.emit('reset');
    }

    /**
     * Generate a preview of the current template using the GameMaster API
     * @returns {Promise<Object|null>} - The preview data (GameMasterTools) or null if failed
     */
    async generatePreview() {
        if (this.isGeneratingPreview) {
            console.log('Preview already being generated, waiting for completion...');
            return this.previewData;
        }

        try {
            this.isGeneratingPreview = true;
            this.emit('previewGenerationStarted');

            console.log('Generating template preview...');

            // First validate the template
            const validation = this.validate();
            if (!validation.isValid) {
                console.warn('Template validation failed, cannot generate preview:', validation.errors);
                this.emit('previewGenerationFailed', {
                    error: 'Template validation failed',
                    validationErrors: validation.errors
                });
                return null;
            }

            // Use the GameMaster API to generate preview
            console.log('Generating template preview...', {template: this.template});
            const response = await GameMasterApi.gamemasterCharacterTemplatesPreviewRetrieve(this.template.id);

            if (!response.data) {
                console.warn('Preview API response is empty');
                this.emit('previewGenerationFailed', { error: 'Empty API response' });
                return null;
            }

            // Store the preview data (GameMasterTools)
            this.previewData = response.data;
            console.log('Template preview generated successfully');
            this.emit('previewGenerated', this.previewData);

            return this.previewData;

        } catch (error) {
            console.error('Failed to generate template preview:', error);
            this.emit('previewGenerationFailed', { error: error.message || 'Unknown error' });
            return null;
        } finally {
            this.isGeneratingPreview = false;
        }
    }

    /**
     * Get the current preview data
     * @returns {Object|null} - The preview data (GameMasterTools) or null if not available
     */
    getPreviewData() {
        return this.previewData;
    }

    /**
     * Check if preview is currently being generated
     * @returns {boolean} - Whether preview generation is in progress
     */
    isPreviewGenerating() {
        return this.isGeneratingPreview;
    }

    /**
     * Clear the current preview data
     */
    clearPreview() {
        this.previewData = null;
        this.emit('previewCleared');
    }

    /**
     * Auto-generate preview when template changes (debounced)
     * @param {number} delay - Delay in milliseconds (default: 1000ms)
     */
    autoGeneratePreview(delay = 1000) {
        // Clear existing timeout
        if (this.previewTimeout) {
            clearTimeout(this.previewTimeout);
        }

        // Set new timeout for preview generation
        this.previewTimeout = setTimeout(async () => {
            try {
                await this.generatePreview();
            } catch (error) {
                console.error('Auto preview generation failed:', error);
            }
        }, delay);
    }

    /**
     * Mark the template as dirty (unsaved changes)
     */
    setDirty() {
        this.isDirty = true;
        this.emit('dirtyStateChanged', this.isDirty);

        // Auto-generate preview when template changes
        this.autoGeneratePreview();
    }

    /**
     * Check if the template has unsaved changes
     * @returns {boolean} - Whether the template has unsaved changes
     */
    hasDirtyState() {
        return this.isDirty;
    }

    /**
     * Event system for components to listen to changes
     */
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    /**
     * Remove event listener
     */
    off(event, callback) {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Emit event to listeners
     */
    emit(event, data) {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }
}

// Export singleton instance
export const characterTemplateEditorService = new CharacterTemplateEditorService();