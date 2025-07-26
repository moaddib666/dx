import {SkillsGameApi, SchoolGameApi} from "@/api/backendService.js";
import {CacheService} from "@/services/cacheService.js";
import { reactive } from "vue";
import { OpenaiSkill, OpenaiSchool, OpenaiPathWithSchools } from "@/api/dx-backend";
import { AxiosResponse } from "axios";

const SkillServiceCache = new CacheService("skills");
const SchoolServiceCache = new CacheService("schools");
const PathServiceCache = new CacheService("paths");

/**
 * Service to manage skills, schools, and their business logic including base/non-base categorization.
 */
export class SkillService {
    private skillsApi: typeof SkillsGameApi;
    private schoolApi: typeof SchoolGameApi;
    private skillCache: CacheService;
    private schoolCache: CacheService;
    private pathCache: CacheService;
    public state: {
        skillsUpdated: boolean;
        schoolsUpdated: boolean;
        pathsUpdated: boolean;
    };

    /**
     * Creates an instance of SkillService.
     * @param skillsApi - The Skills API instance.
     * @param schoolApi - The School API instance.
     * @param skillCache - The skills cache service instance.
     * @param schoolCache - The schools cache service instance.
     * @param pathCache - The paths cache service instance.
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
     * @returns Promise<void>
     * @throws Will throw an error if the API call fails or the data is invalid.
     */
    async updateSkillsCache(): Promise<void> {
        try {
            const response: AxiosResponse = await this.schoolApi.schoolSchoolsGetAllSkillsRetrieve();
            const skills: OpenaiSkill[] = response.data;
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
                await this.skillCache.acquire(skill.id.toString());
                if (skill && skill.id) {
                    await this.skillCache.set(skill.id.toString(), skill);
                } else {
                    console.warn("Encountered invalid skill data:", skill);
                }
                await this.skillCache.release(skill.id.toString());
            }
            this.state.skillsUpdated = true;
        } catch (error) {
            console.error("Failed to update skills cache:", error);
            throw error;
        }
    }

    /**
     * Updates the schools cache with the latest data from the School API.
     * @returns Promise<void>
     */
    async updateSchoolsCache(): Promise<void> {
        try {
            const response: AxiosResponse = await this.schoolApi.schoolSchoolsGetAllSchoolsRetrieve();
            const schools: OpenaiSchool[] = response.data;
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
     * @returns Promise<void>
     */
    async updatePathsCache(): Promise<void> {
        try {
            const response: AxiosResponse = await this.schoolApi.schoolPathsGetAllPathsRetrieve();
            const paths: OpenaiPathWithSchools[] = response.data;
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
     * @returns Promise<void>
     */
    async updateAllCaches(): Promise<void> {
        await Promise.all([
            this.updateSkillsCache(),
            this.updateSchoolsCache(),
            this.updatePathsCache()
        ]);
    }

    /**
     * Backward compatibility method - updates skills cache only.
     * @deprecated Use updateSkillsCache() or updateAllCaches() instead.
     * @returns Promise<void>
     */
    async updateCache(): Promise<void> {
        console.warn('updateCache() is deprecated. Use updateSkillsCache() or updateAllCaches() instead.');
        await this.updateSkillsCache();
    }

    /**
     * Get a skill by its ID.
     * @param skillId - The ID of the skill.
     * @returns The skill data or null if not found.
     */
    getSkill(skillId: number): OpenaiSkill | null {
        console.debug(`Getting skill ${skillId}...`);
        const skill = this.skillCache.getInternally(skillId.toString());
        if (!skill) {
            console.warn(`Skill ${skillId} not found in cache.`);
            return null;
        }
        console.debug(`Got skill ${skillId}:`, skill);
        return skill;
    }

    /**
     * Get a school by its ID.
     * @param schoolId - The ID of the school.
     * @returns The school data or null if not found.
     */
    getSchool(schoolId: string): OpenaiSchool | null {
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
     * @param pathId - The ID of the path.
     * @returns The path data or null if not found.
     */
    getPath(pathId: string): OpenaiPathWithSchools | null {
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
     * @returns Array of all skills.
     */
    getAllSkills(): OpenaiSkill[] {
        // Since we don't have getAllInternally, we'll store a master list
        const masterList = this.skillCache.getInternally('__all__');
        return masterList || [];
    }

    /**
     * Get all schools from cache.
     * @returns Array of all schools.
     */
    getAllSchools(): OpenaiSchool[] {
        const masterList = this.schoolCache.getInternally('__all__');
        return masterList || [];
    }

    /**
     * Get all paths from cache.
     * @returns Array of all paths.
     */
    getAllPaths(): OpenaiPathWithSchools[] {
        const masterList = this.pathCache.getInternally('__all__');
        return masterList || [];
    }

    /**
     * Check if a school is a base school.
     * @param school - The school object.
     * @returns True if the school is a base school.
     */
    isBaseSchool(school: OpenaiSchool | null): boolean {
        if (!school) return false;
        return Boolean(school.is_base);
    }

    /**
     * Check if a spell/skill is a base spell.
     * @param spell - The spell object.
     * @returns True if the spell is a base spell.
     */
    isBaseSpell(spell: OpenaiSkill | null): boolean {
        if (!spell) return false;

        // Check if spell has is_base property (not in the interface but might be in the data)
        if ('is_base' in spell && Boolean(spell['is_base'])) return true;
        if ('is_default' in spell && Boolean(spell['is_default'])) return true;
        if ('is_mandatory' in spell && Boolean(spell['is_mandatory'])) return true;

        // Check if spell belongs to a base school
        if (spell.school) {
            const spellSchool = this.getSchool(spell.school);
            return this.isBaseSchool(spellSchool);
        }

        return false;
    }

    /**
     * Get base schools.
     * @returns Array of base schools.
     */
    getBaseSchools(): OpenaiSchool[] {
        return this.getAllSchools().filter(school => this.isBaseSchool(school));
    }

    /**
     * Get base skills/spells.
     * @returns Array of base skills.
     */
    getBaseSkills(): OpenaiSkill[] {
        return this.getAllSkills().filter(spell => this.isBaseSpell(spell));
    }

    /**
     * Get non-base schools from a list of school IDs.
     * @param schoolIds - Array of school IDs.
     * @returns Array of non-base school IDs.
     */
    getNonBaseSchoolIds(schoolIds: string[]): string[] {
        return schoolIds.filter(schoolId => {
            const school = this.getSchool(schoolId);
            return school && !this.isBaseSchool(school);
        });
    }

    /**
     * Get non-base spells from a list of spell IDs.
     * @param spellIds - Array of spell IDs.
     * @returns Array of non-base spell IDs.
     */
    getNonBaseSpellIds(spellIds: number[]): number[] {
        return spellIds.filter(spellId => {
            const spell = this.getSkill(spellId);
            return spell && !this.isBaseSpell(spell);
        });
    }

    /**
     * Get available schools for a specific path (excluding base schools and already selected ones).
     * @param pathId - The path ID.
     * @param selectedSchoolIds - Array of already selected school IDs.
     * @returns Array of available schools.
     */
    getAvailableSchoolsForPath(pathId: string, selectedSchoolIds: string[] = []): OpenaiSchool[] {
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
     * @param schoolId - The school ID.
     * @param selectedSpellIds - Array of already selected spell IDs.
     * @returns Array of available spells.
     */
    getAvailableSpellsForSchool(schoolId: string, selectedSpellIds: number[] = []): OpenaiSkill[] {
        if (!schoolId) return [];

        return this.getAllSkills().filter(spell => {
            const isFromSchool = spell.school === schoolId;
            const notSelected = !selectedSpellIds.includes(spell.id);

            return isFromSchool && notSelected;
        });
    }

    /**
     * Get the count of base skills from a list of spell IDs.
     * @param spellIds - Array of spell IDs.
     * @returns Count of base skills.
     */
    getBaseSkillsCount(spellIds: number[]): number {
        return spellIds.filter(spellId => {
            const spell = this.getSkill(spellId);
            return spell && this.isBaseSpell(spell);
        }).length;
    }
}

// Exporting a singleton instance of SkillService
const defaultSkillServiceInstance = new SkillService();
export default defaultSkillServiceInstance;