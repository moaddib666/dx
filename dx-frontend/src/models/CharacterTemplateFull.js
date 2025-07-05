/**
 * CharacterTemplateFull Model
 * Represents a full character template with all data needed for editing and creation
 */

/**
 * @typedef {Object} Bio
 * @property {number} age - Character's age
 * @property {string} gender - Character's gender
 * @property {string} appearance - Character's physical appearance description
 * @property {string} background - Character's background story
 */

/**
 * @typedef {Object} Stat
 * @property {string} name - Stat name
 * @property {number} value - Stat value
 */

/**
 * @typedef {Object} Modificator
 * @property {string} id - Modificator ID
 * @property {string} name - Modificator name
 * @property {string} description - Modificator description
 */

/**
 * @typedef {Object} ValidationRules
 * @property {number} max_stats_points_count - Maximum total stat points
 * @property {number} max_modificators_count - Maximum number of modificators
 * @property {number} max_items_count - Maximum number of items
 * @property {number} max_spells_count - Maximum number of spells
 * @property {number} max_rank_grade - Maximum rank grade
 * @property {number} max_schools_count - Maximum number of schools
 */

/**
 * @typedef {Object} CharacterTemplateFull
 * @property {Object} data - Template data
 * @property {string} data.name - Template name
 * @property {string[]} data.tags - Template tags
 * @property {Bio} data.bio - Character bio information
 * @property {number} data.rank - Character rank
 * @property {string} data.path - Character path ID
 * @property {Stat[]} data.stats - Character stats
 * @property {Modificator[]} data.modificators - Character modificators
 * @property {string[]} data.items - Item IDs
 * @property {string[]} data.schools - School IDs
 * @property {number[]} data.spells - Spell IDs
 * @property {ValidationRules} validation - Validation rules for the template
 */

/**
 * Create a new empty CharacterTemplateFull object
 * @returns {CharacterTemplateFull} Empty character template
 */
export function createEmptyCharacterTemplate() {
  return {
    data: {
      name: '',
      tags: [],
      bio: {
        age: 30,
        gender: '',
        appearance: '',
        background: ''
      },
      rank: 1,
      path: '',
      stats: [
        { name: 'Physical Strength', value: 10 },
        { name: 'Mental Strength', value: 10 },
        { name: 'Flow Resonance', value: 10 },
        { name: 'Concentration', value: 10 },
        { name: 'Flow Manipulation', value: 10 },
        { name: 'Flow Connection', value: 10 },
        { name: 'Knowledge', value: 10 },
        { name: 'Speed', value: 10 },
        { name: 'Luck', value: 10 },
        { name: 'Charisma', value: 10 }
      ],
      modificators: [],
      items: [],
      schools: [],
      spells: []
    },
    validation: {
      max_stats_points_count: 100,
      max_modificators_count: 2,
      max_items_count: 1,
      max_spells_count: 1,
      max_rank_grade: 9,
      max_schools_count: 1
    }
  };
}

/**
 * Create a sample CharacterTemplateFull object for testing
 * @returns {CharacterTemplateFull} Sample character template
 */
export function createSampleCharacterTemplate() {
  return {
    data: {
      name: "Mercenary Hex 3 Template",
      tags: [
        "Mercenary",
        "Demolitions Expert",
        "Hired Gun"
      ],
      bio: {
        age: 35,
        gender: "Other",
        appearance: "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
        background: "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing."
      },
      rank: 9,
      path: "c7b92d32-4c21-4a29-84c2-469e4f888d31",
      stats: [
        {
          name: "Physical Strength",
          value: 7
        },
        {
          name: "Mental Strength",
          value: 9
        },
        {
          name: "Flow Resonance",
          value: 13
        },
        {
          name: "Concentration",
          value: 11
        },
        {
          name: "Flow Manipulation",
          value: 14
        },
        {
          name: "Flow Connection",
          value: 15
        },
        {
          name: "Knowledge",
          value: 14
        },
        {
          name: "Speed",
          value: 14
        },
        {
          name: "Luck",
          value: 11
        },
        {
          name: "Charisma",
          value: 12
        }
      ],
      modificators: [],
      items: [
        "28c32381-bd58-4193-8e8c-996411f8dcb0",
        "0e4ebda0-e4db-413b-841d-b02054d47212"
      ],
      schools: [
        "3ea5c283-f8fd-4e24-a7e1-89ff96c8d796",
        "684821f8-8cb1-4a70-8273-23a9adcee28d"
      ],
      spells: [
        29,
        30,
        31,
        32,
        167,
        168,
        58
      ]
    },
    validation: {
      max_stats_points_count: 100,
      max_modificators_count: 2,
      max_items_count: 1,
      max_spells_count: 1,
      max_rank_grade: 9,
      max_schools_count: 1
    }
  };
}