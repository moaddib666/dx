/**
 * Service for handling character stats data and preparing it for display in the radar chart
 */
import {GameMasterApi} from '@/api/backendService';

// Define the fixed stat names as per requirements
const STAT_NAMES = [
    'Charisma',
    'Concentration',
    'Flow Connection',
    'Flow Manipulation',
    'Flow Resonance',
    'Knowledge',
    'Luck',
    'Mental Strength',
    'Physical Strength',
    'Speed'
];

export default {
    /**
     * Fetch character stats for a specific character
     * @param {string} characterId - The ID of the character
     * @returns {Promise<Object>} - The character stats data
     */
    async fetchCharacterStats(characterId) {
        try {
            const response = await GameMasterApi.gamemasterCharactersCharacterStatsCardRetrieve(characterId);
            return response.data;
        } catch (error) {
            console.error('Error fetching character stats:', error);
            throw error;
        }
    },

    /**
     * Process character stats data for the radar chart
     * @param {Object} statsData - The raw stats data from the API
     * @returns {Object} - Processed data ready for the radar chart
     */
    processStatsForRadarChart(statsData) {
        if (!statsData || !statsData.stats || !Array.isArray(statsData.stats)) {
            // Return data in the format expected by the radar chart component
            return {
                stats: STAT_NAMES.map(name => ({name, value: 0})),
                maxValue: 20
            };
        }

        // Create a map of stat names to their values
        const statMap = {};
        statsData.stats.forEach(stat => {
            // Calculate total value (base + additional)
            const totalValue = (stat.base_value || 0) + (stat.additional_value || 0);
            statMap[stat.name] = totalValue;
        });

        // Create an array of stat objects in the format expected by the radar chart
        const stats = STAT_NAMES.map(statName => ({
            name: statName,
            value: statMap[statName] || 0
        }));

        // Determine the maximum value for scaling
        const maxValue = statsData.max_value || 20;

        return {
            stats: stats,
            maxValue: maxValue
        };
    },

    /**
     * Get the fixed stat names
     * @returns {Array<string>} - The fixed stat names
     */
    getStatNames() {
        return STAT_NAMES;
    }
};
