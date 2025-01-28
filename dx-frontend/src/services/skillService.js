import {SkillsGameApi, SchoolGameApi} from "@/api/backendService.js";
import {CacheService} from "@/services/cacheService.js";
import { reactive } from "vue";

const SkillServiceCache = new CacheService("skills");

/**
 * Service to manage skills, including fetching from APIs and caching.
 */
export class SkillService {
    /**
     * Creates an instance of SkillService.
     * @param {SkillsGameApi} [skillsApi=SkillsGameApi] - The Skills API instance.
     * @param {SchoolGameApi} [schoolApi=SchoolGameApi] - The School API instance.
     * @param {CacheService} [cache=SkillServiceCache] - The cache service instance.
     */
    constructor(skillsApi = SkillsGameApi, schoolApi = SchoolGameApi, cache = SkillServiceCache) {
        this.skillsApi = skillsApi;
        this.schoolApi = schoolApi;
        this.cache = cache;
        this.state = reactive({ updated: false }); // Use reactive state
    }

    /**
     * Updates the cache with the latest skills from the School API.
     * Ensures the cache is only updated once unless reset.
     * @returns {Promise<void>}
     * @throws Will throw an error if the API call fails or the data is invalid.
     */
    async updateCache() {
        try {
            // Await the API call first, then access the data
            const response = (await this.schoolApi.schoolSchoolsGetAllSkillsRetrieve());
            const skills = response.data;
            console.debug("Retrieved skills data:", {skills});

            if (!Array.isArray(skills)) {
                throw new Error("Invalid data format: Expected an array of skills.");
            }

            // Populate the cache with each skill
            for (const skill of skills) {
                await this.cache.acquire(skill.id);
                if (skill && skill.id) { // Ensure skill has an id
                    await this.cache.set(skill.id, skill);
                } else {
                    console.warn("Encountered invalid skill data:", skill);
                }
                await this.cache.release(skill.id);
            }
        } catch (error) {
            console.error("Failed to update skills cache:", error);
            throw error; // Re-throw the error after logging
        }
    }

    /**
     * Get a skill by its ID.
     * @param {Number} skillId - The ID of the skill.
     * @returns {OpenaiSkill} The skill data.
     */
    getSkill(skillId) {
        console.debug(`Getting skill ${skillId}...`);
        const skill = this.cache.getInternally(skillId);
        if (!skill) {
            throw new Error(`Skill ${skillId} not found in cache.`);
        }
        console.debug(`Got skill ${skillId}:`, skill);
        return skill;
    }
}

// Exporting a singleton instance of SkillService
const defaultSkillServiceInstance = new SkillService();
export default defaultSkillServiceInstance;
