import {SkillsGameApi, SchoolGameApi} from "@/api/backendService.js";
import {CacheService} from "@/services/cacheService.js";
import { reactive } from "vue";

const SkillServiceCache = new CacheService("skills");
const SchoolServiceCache = new CacheService("schools");
const PathServiceCache = new CacheService("paths");

/**
 * Service to manage skills, schools, and their business logic including base/non-base categorization.
 */
export class SkillService {
    /**
     * Creates an instance of SkillService.
     * @param {SkillsGameApi} [skillsApi=SkillsGameApi] - The Skills API instance.
     * @param {SchoolGameApi} [schoolApi=SchoolGameApi] - The School API instance.
     * @param {CacheService} [skillCache=SkillServiceCache] - The skills cache service instance.
     * @param {CacheService} [schoolCache=SchoolServiceCache] - The schools cache service instance.
     * @param {CacheService} [pathCache=PathServiceCache] - The paths cache service instance.
     */
    constructor(
        skillsApi = SkillsGameApi, 
        schoolApi = SchoolGameApi, 
        skillCache = SkillServiceCache,
        schoolCache = SchoolServiceCache,
        pathCache = PathServiceCache
    ) {
        this.skillsApi = skillsApi;
        this.schoolApi = schoolApi;
        this.skillCache = skillCache;
        this.schoolCache = schoolCache;
        this.pathCache = pathCache;
        this.state = reactive({ 
            skillsUpdated: false,
            schoolsUpdated: false,
            pathsUpdated: false
        });
    }

    /**
     * Updates the skills cache with the latest data from the School API.
     * @returns {Promise<void>}
     * @throws Will throw an error if the API call fails or the data is invalid.
     */
    async updateSkillsCache() {
        try {
            const response = await this.schoolApi.schoolSchoolsGetAllSkillsRetrieve();
            const skills = response.data;
            console.debug("Retrieved skills data:", {skills});

            if (!Array.isArray(skills)) {
                throw new Error("Invalid data format: Expected an array of skills.");
            }

            // Store master list
            await this.skillCache.acquire('__all__');
            await this.skillCache.set('__all__', skills);
            await this.skillCache.release('__all__');
            
            // Populate the cache with each skill
            for (const skill of skills) {
                await this.skillCache.acquire(skill.id);
                if (skill && skill.id) {
                    await this.skillCache.set(skill.id, skill);
                } else {
                    console.warn("Encountered invalid skill data:", skill);
                }
                await this.skillCache.release(skill.id);
            }
            this.state.skillsUpdated = true;
        } catch (error) {
            console.error("Failed to update skills cache:", error);
            throw error;
        }
    }

    /**
     * Updates the schools cache with the latest data from the School API.
     * @returns {Promise<void>}
     */
    async updateSchoolsCache() {
        try {
            const response = await this.schoolApi.schoolSchoolsGetAllSchoolsRetrieve();
            const schools = response.data;
            console.debug("Retrieved schools data:", {schools});

            if (!Array.isArray(schools)) {
                throw new Error("Invalid data format: Expected an array of schools.");
            }

            // Store master list
            await this.schoolCache.acquire('__all__');
            await this.schoolCache.set('__all__', schools);
            await this.schoolCache.release('__all__');
            
            for (const school of schools) {
                await this.schoolCache.acquire(school.id);
                if (school && school.id) {
                    await this.schoolCache.set(school.id, school);
                } else {
                    console.warn("Encountered invalid school data:", school);
                }
                await this.schoolCache.release(school.id);
            }
            this.state.schoolsUpdated = true;
        } catch (error) {
            console.error("Failed to update schools cache:", error);
            throw error;
        }
    }

    /**
     * Updates the paths cache with the latest data from the School API.
     * @returns {Promise<void>}
     */
    async updatePathsCache() {
        try {
            const response = await this.schoolApi.schoolPathsGetAllPathsRetrieve();
            const paths = response.data;
            console.debug("Retrieved paths data:", {paths});

            if (!Array.isArray(paths)) {
                throw new Error("Invalid data format: Expected an array of paths.");
            }

            // Store master list
            await this.pathCache.acquire('__all__');
            await this.pathCache.set('__all__', paths);
            await this.pathCache.release('__all__');
            
            for (const path of paths) {
                await this.pathCache.acquire(path.id);
                if (path && path.id) {
                    await this.pathCache.set(path.id, path);
                } else {
                    console.warn("Encountered invalid path data:", path);
                }
                await this.pathCache.release(path.id);
            }
            this.state.pathsUpdated = true;
        } catch (error) {
            console.error("Failed to update paths cache:", error);
            throw error;
        }
    }

    /**
     * Updates all caches (skills, schools, paths).
     * @returns {Promise<void>}
     */
    async updateAllCaches() {
        await Promise.all([
            this.updateSkillsCache(),
            this.updateSchoolsCache(),
            this.updatePathsCache()
        ]);
    }

    /**
     * Backward compatibility method - updates skills cache only.
     * @deprecated Use updateSkillsCache() or updateAllCaches() instead.
     * @returns {Promise<void>}
     */
    async updateCache() {
        console.warn('updateCache() is deprecated. Use updateSkillsCache() or updateAllCaches() instead.');
        await this.updateSkillsCache();
    }

    /**
     * Get a skill by its ID.
     * @param {Number} skillId - The ID of the skill.
     * @returns {Object|null} The skill data or null if not found.
     */
    getSkill(skillId) {
        console.debug(`Getting skill ${skillId}...`);
        const skill = this.skillCache.getInternally(skillId);
        if (!skill) {
            console.warn(`Skill ${skillId} not found in cache.`);
            return null;
        }
        console.debug(`Got skill ${skillId}:`, skill);
        return skill;
    }

    /**
     * Get a school by its ID.
     * @param {Number} schoolId - The ID of the school.
     * @returns {Object|null} The school data or null if not found.
     */
    getSchool(schoolId) {
        console.debug(`Getting school ${schoolId}...`);
        const school = this.schoolCache.getInternally(schoolId);
        if (!school) {
            console.warn(`School ${schoolId} not found in cache.`);
            return null;
        }
        console.debug(`Got school ${schoolId}:`, school);
        return school;
    }

    /**
     * Get a path by its ID.
     * @param {String} pathId - The ID of the path.
     * @returns {Object|null} The path data or null if not found.
     */
    getPath(pathId) {
        console.debug(`Getting path ${pathId}...`);
        const path = this.pathCache.getInternally(pathId);
        if (!path) {
            console.warn(`Path ${pathId} not found in cache.`);
            return null;
        }
        console.debug(`Got path ${pathId}:`, path);
        return path;
    }

    /**
     * Get all skills from cache.
     * @returns {Array} Array of all skills.
     */
    getAllSkills() {
        // Since we don't have getAllInternally, we'll store a master list
        const masterList = this.skillCache.getInternally('__all__');
        return masterList || [];
    }

    /**
     * Get all schools from cache.
     * @returns {Array} Array of all schools.
     */
    getAllSchools() {
        const masterList = this.schoolCache.getInternally('__all__');
        return masterList || [];
    }

    /**
     * Get all paths from cache.
     * @returns {Array} Array of all paths.
     */
    getAllPaths() {
        const masterList = this.pathCache.getInternally('__all__');
        return masterList || [];
    }

    /**
     * Check if a school is a base school.
     * @param {Object} school - The school object.
     * @returns {Boolean} True if the school is a base school.
     */
    isBaseSchool(school) {
        if (!school) return false;
        return Boolean(school.is_base || school.is_default || school.is_mandatory);
    }

    /**
     * Check if a spell/skill is a base spell.
     * @param {Object} spell - The spell object.
     * @returns {Boolean} True if the spell is a base spell.
     */
    isBaseSpell(spell) {
        if (!spell) return false;
        if (Boolean(spell.is_base || spell.is_default || spell.is_mandatory)) return true;
        
        // Check if spell belongs to a base school
        const spellSchool = this.getSchool(spell.school);
        return this.isBaseSchool(spellSchool);
    }

    /**
     * Get base schools.
     * @returns {Array} Array of base schools.
     */
    getBaseSchools() {
        return this.getAllSchools().filter(school => this.isBaseSchool(school));
    }

    /**
     * Get base skills/spells.
     * @returns {Array} Array of base skills.
     */
    getBaseSkills() {
        return this.getAllSkills().filter(spell => this.isBaseSpell(spell));
    }

    /**
     * Get non-base schools from a list of school IDs.
     * @param {Array} schoolIds - Array of school IDs.
     * @returns {Array} Array of non-base school IDs.
     */
    getNonBaseSchoolIds(schoolIds) {
        return schoolIds.filter(schoolId => {
            const school = this.getSchool(schoolId);
            return school && !this.isBaseSchool(school);
        });
    }

    /**
     * Get non-base spells from a list of spell IDs.
     * @param {Array} spellIds - Array of spell IDs.
     * @returns {Array} Array of non-base spell IDs.
     */
    getNonBaseSpellIds(spellIds) {
        return spellIds.filter(spellId => {
            const spell = this.getSkill(spellId);
            return spell && !this.isBaseSpell(spell);
        });
    }

    /**
     * Get available schools for a specific path (excluding base schools and already selected ones).
     * @param {String} pathId - The path ID.
     * @param {Array} selectedSchoolIds - Array of already selected school IDs.
     * @returns {Array} Array of available schools.
     */
    getAvailableSchoolsForPath(pathId, selectedSchoolIds = []) {
        if (!pathId) return [];
        
        return this.getAllSchools().filter(school => {
            const isFromPath = school.path && school.path.includes(pathId);
            const notSelected = !selectedSchoolIds.includes(school.id);
            const notBase = !this.isBaseSchool(school);
            
            return isFromPath && notSelected && notBase;
        });
    }

    /**
     * Get available spells for a specific school (excluding already selected ones).
     * @param {Number} schoolId - The school ID.
     * @param {Array} selectedSpellIds - Array of already selected spell IDs.
     * @returns {Array} Array of available spells.
     */
    getAvailableSpellsForSchool(schoolId, selectedSpellIds = []) {
        if (!schoolId) return [];
        
        return this.getAllSkills().filter(spell => {
            const isFromSchool = spell.school === schoolId;
            const notSelected = !selectedSpellIds.includes(spell.id);
            
            return isFromSchool && notSelected;
        });
    }

    /**
     * Get the count of base skills from a list of spell IDs.
     * @param {Array} spellIds - Array of spell IDs.
     * @returns {Number} Count of base skills.
     */
    getBaseSkillsCount(spellIds) {
        return spellIds.filter(spellId => {
            const spell = this.getSkill(spellId);
            return spell && this.isBaseSpell(spell);
        }).length;
    }
}

// Exporting a singleton instance of SkillService
const defaultSkillServiceInstance = new SkillService();
export default defaultSkillServiceInstance;
