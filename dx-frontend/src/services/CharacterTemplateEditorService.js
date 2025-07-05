import { GameMasterApi } from '@/api/backendService.js';
import { createEmptyCharacterTemplate } from '@/models/CharacterTemplateFull.js';
import { characterTemplatesService } from '@/services/CharacterTemplatesService.js';

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
            const response = await GameMasterApi.gamemasterCharacterTemplatesRetrieve(templateId);

            if (!response.data) {
                console.warn('Template API response is empty');
                return null;
            }

            // Convert the API response to our CharacterTemplateFull format
            this.template = this.convertApiResponseToTemplate(response.data);
            this.isDirty = false;

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
        // This is a placeholder implementation
        // In a real implementation, you would map the API response to the CharacterTemplateFull format
        const template = createEmptyCharacterTemplate();

        // Map basic properties
        if (apiResponse.name) template.data.name = apiResponse.name;
        if (apiResponse.tags) template.data.tags = [...apiResponse.tags];
        if (apiResponse.rank) template.data.rank = apiResponse.rank;
        if (apiResponse.path) template.data.path = apiResponse.path;

        // Map bio if available
        if (apiResponse.bio) {
            template.data.bio.age = apiResponse.bio.age || 30;
            template.data.bio.gender = apiResponse.bio.gender || '';
            template.data.bio.appearance = apiResponse.bio.appearance || '';
            template.data.bio.background = apiResponse.bio.background || '';
        }

        // Map stats if available
        if (apiResponse.stats && Array.isArray(apiResponse.stats)) {
            template.data.stats = apiResponse.stats.map(stat => ({
                name: stat.name,
                value: stat.value
            }));
        }

        // Map other arrays
        if (apiResponse.modificators) template.data.modificators = [...apiResponse.modificators];
        if (apiResponse.items) template.data.items = [...apiResponse.items];
        if (apiResponse.schools) template.data.schools = [...apiResponse.schools];
        if (apiResponse.spells) template.data.spells = [...apiResponse.spells];

        // Map validation rules if available
        if (apiResponse.validation) {
            Object.assign(template.validation, apiResponse.validation);
        }

        return template;
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

        // Check if we've reached the maximum number of schools
        if (this.template.data.schools.length >= this.template.validation.max_schools_count) {
            console.warn(`Cannot add school: Maximum number of schools (${this.template.validation.max_schools_count}) reached`);
            this.emit('validationError', {
                type: 'schools',
                message: `Maximum number of schools (${this.template.validation.max_schools_count}) reached`
            });
            return;
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

        // Check if we've reached the maximum number of spells
        if (this.template.data.spells.length >= this.template.validation.max_spells_count) {
            console.warn(`Cannot add spell: Maximum number of spells (${this.template.validation.max_spells_count}) reached`);
            this.emit('validationError', {
                type: 'spells',
                message: `Maximum number of spells (${this.template.validation.max_spells_count}) reached`
            });
            return;
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

        // Check spells count
        if (this.template.data.spells.length > validation.max_spells_count) {
            errors.push({
                type: 'spells',
                message: `Spells count (${this.template.data.spells.length}) exceeds maximum (${validation.max_spells_count})`
            });
        }

        // Check rank
        if (this.template.data.rank > validation.max_rank_grade) {
            errors.push({
                type: 'rank',
                message: `Rank (${this.template.data.rank}) exceeds maximum (${validation.max_rank_grade})`
            });
        }

        // Check schools count
        if (this.template.data.schools.length > validation.max_schools_count) {
            errors.push({
                type: 'schools',
                message: `Schools count (${this.template.data.schools.length}) exceeds maximum (${validation.max_schools_count})`
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
        console.log('CharacterTemplateEditorService reset');
        this.emit('reset');
    }

    /**
     * Mark the template as dirty (unsaved changes)
     */
    setDirty() {
        this.isDirty = true;
        this.emit('dirtyStateChanged', this.isDirty);
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