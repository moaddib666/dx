<template>
  <div class="player-create">
    <h1>Character Submission</h1>
    <main class="form-container">
      <PathSelector :paths="paths" @path-selected="selectPath" />
      <form @submit.prevent="submitPlayer">
        <!-- Basic Information Section -->
        <section class="basic-info">
          <h2>Basic Information</h2>
          <label>
            Character Name:
            <input
                v-model="player.characterName"
                type="text"
                placeholder="Enter your character's name"
                required
            />
          </label>
          <label>
            Age:
            <input
                v-model.number="player.age"
                type="number"
                min="10"
                max="99"
                placeholder="Enter age"
                required
            />
          </label>
          <label>
            Gender:
            <select v-model="player.gender" required>
              <option value="" disabled>Select gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </label>
          <label>
            Appearance:
            <textarea
                v-model="player.appearance"
                placeholder="Enter your character's appearance"
                required
            ></textarea>
          </label>
          <label>
            Background:
            <textarea
                v-model="player.background"
                placeholder="Enter your character's background"
                required
            ></textarea>
          </label>
        </section>

        <!-- Feature Selection Section -->
        <section class="feature-selection">
          <h2>Select Your Feature</h2>
          <div class="features">
            <div
                v-for="(feature, key) in features"
                :key="key"
                class="feature-item"
                :class="{ selected: selectedFeature === key }"
                @click="selectFeature(key)"
            >
              <h3>{{ feature.name }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </div>
        </section>

        <!-- Action Points Section -->
        <section class="action-points">
          <h2>Allocate Action Points</h2>
          <AttributesAllocator
              :availablePoints="10"
              :characteristics="characteristics"
              @submit="handleAllocation"
          />
        </section>

        <!-- Submit Button -->
        <button type="submit" :disabled="!isFormComplete">Submit Player</button>
      </form>
    </main>
  </div>
</template>


<script>
import AttributesAllocator from "@/components/Player/AttributesAllocator.vue";
import PathPathSelector from "@/components/Path/PathSelector.vue";

export default {
  components: {
    PathSelector: PathPathSelector,
    AttributesAllocator: AttributesAllocator,
  },
  data() {
    return {
      player: {
        name: "",
        characterName: "",
        age: null,
        gender: "",
      },
      selectedFeature: null,
      paths: [
        {
          "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31",
          "created_at": "2024-06-09T00:00:00Z",
          "updated_at": "2024-12-16T19:02:45.838286Z",
          "name": "Path of John",
          "description": "A path focusing on technical enhancements.",
          "icon": "http://localhost:8000/media/icons/path/john.webp"
        },
        {
          "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6",
          "created_at": "2024-06-09T00:00:00Z",
          "updated_at": "2024-12-16T19:03:00.404469Z",
          "name": "Path of JSon",
          "description": "A path focusing on magical abilities.",
          "icon": "http://localhost:8000/media/icons/path/json.webp"
        }
      ],
      features:
          {
            "TECH_GURU": {
              "name": "Tech Guru",
              "description": "Gifted with technology, adept at repairs and enhancements.",
              "modifiers": {
                "KNOWLEDGE": 1,
                "FLOW_MANIPULATION": 1
              }
            },
            "MYSTIC_SAVANT": {
              "name": "Mystic Savant",
              "description": "A natural connection to the Flow amplifies their magical prowess.",
              "modifiers": {
                "FLOW_CONNECTION": 1,
                "FLOW_RESONANCE": 1
              }
            },
            "SMOOTH_TALKER": {
              "name": "Smooth Talker",
              "description": "Charming and persuasive, capable of winning most arguments.",
              "modifiers": {
                "CHARISMA": 2
              }
            },
            "MEDSERV_EX_WORKER": {
              "name": "Medserv Ex-Worker",
              "description": "A seasoned medic skilled in healing and problem-solving.",
              "modifiers": {
                "MENTAL_STRENGTH": 1,
                "KNOWLEDGE": 1
              }
            },
            "FLOW_ENGINEER": {
              "name": "Flow Engineer",
              "description": "Master of Flow-powered machinery and devices.",
              "modifiers": {
                "FLOW_MANIPULATION": 1,
                "KNOWLEDGE": 1
              }
            },
            "SHADOW_OPERATIVE": {
              "name": "Shadow Operative",
              "description": "A master of stealth and quick reflexes.",
              "modifiers": {
                "SPEED": 1,
                "LUCK": 1
              }
            },
            "STREET_HACKER": {
              "name": "Street Hacker",
              "description": "Skilled in bypassing systems and exploiting weaknesses.",
              "modifiers": {
                "KNOWLEDGE": 1,
                "LUCK": 1
              }
            },
            "EXILED_MERCENARY": {
              "name": "Exiled Mercenary",
              "description": "A hardened fighter with unmatched physical toughness.",
              "modifiers": {
                "PHYSICAL_STRENGTH": 1,
                "MENTAL_STRENGTH": 1
              }
            },
            "SPIRITUAL_MEDIUM": {
              "name": "Spiritual Medium",
              "description": "Sensitive to echoes and deep resonances of the Flow.",
              "modifiers": {
                "FLOW_CONNECTION": 1,
                "FLOW_RESONANCE": 1
              }
            },
            "FLOW_SCAVENGER": {
              "name": "Flow Scavenger",
              "description": "Skilled in finding rare artifacts within Flow anomalies.",
              "modifiers": {
                "LUCK": 1,
                "FLOW_MANIPULATION": 1
              }
            },
            "CORP_FUGITIVE": {
              "name": "Corp Fugitive",
              "description": "A nimble escapee with a silver tongue.",
              "modifiers": {
                "SPEED": 1,
                "CHARISMA": 1
              }
            },
            "UNDERWORLD_BARTENDER": {
              "name": "Underworld Bartender",
              "description": "Knows everyone's secrets and makes useful connections.",
              "modifiers": {
                "CHARISMA": 1,
                "KHARMA": 1
              }
            },
            "BLOOD_RITUALIST": {
              "name": "Blood Ritualist",
              "description": "Practitioner of dark rituals, attuned to Flow energy.",
              "modifiers": {
                "FLOW_RESONANCE": 1,
                "MENTAL_STRENGTH": 1
              }
            },
            "EX_SECURITY_OFFICER": {
              "name": "Ex-Security Officer",
              "description": "An expert in tactical defense and swift action.",
              "modifiers": {
                "PHYSICAL_STRENGTH": 1,
                "SPEED": 1
              }
            },
            "BLACK_MARKET_TRADER": {
              "name": "Black Market Trader",
              "description": "Always knows how to strike a deal or find rare goods.",
              "modifiers": {
                "CHARISMA": 1,
                "LUCK": 1
              }
            },
            "GENETIC_AUGMENTEE": {
              "name": "Genetic Augmentee",
              "description": "Enhanced through science, stronger and more durable.",
              "modifiers": {
                "PHYSICAL_STRENGTH": 1,
                "MENTAL_STRENGTH": 1
              }
            },
            "RELIC_ARCHIVIST": {
              "name": "Relic Archivist",
              "description": "An expert in deciphering ancient Flow artifacts.",
              "modifiers": {
                "KNOWLEDGE": 1,
                "FLOW_CONNECTION": 1
              }
            },
            "WASTELAND_SURVIVOR": {
              "name": "Wasteland Survivor",
              "description": "Tough and resilient, a master of survival.",
              "modifiers": {
                "MENTAL_STRENGTH": 1,
                "PHYSICAL_STRENGTH": 1
              }
            },
            "ARTIFICER_APPRENTICE": {
              "name": "Artificer Apprentice",
              "description": "A budding tinkerer adept at crafting Flow devices.",
              "modifiers": {
                "FLOW_MANIPULATION": 1,
                "KNOWLEDGE": 1
              }
            },
            "LOST_RESEARCHER": {
              "name": "Lost Researcher",
              "description": "Driven by an insatiable hunger for discovery.",
              "modifiers": {
                "KNOWLEDGE": 1,
                "LUCK": 1
              }
            },
            "FLOW_TINKERER": {
              "name": "Flow Tinkerer",
              "description": "Expert at fine-tuning Flow-infused tech.",
              "modifiers": {
                "FLOW_MANIPULATION": 1,
                "CONCENTRATION": 1
              }
            },
            "BRAWLER": {
              "name": "Brawler",
              "description": "A natural fighter skilled in close combat.",
              "modifiers": {
                "PHYSICAL_STRENGTH": 2
              }
            },
            "DRUNKEN_WANDERER": {
              "name": "Drunken Wanderer",
              "description": "Luck always seems to favor this unpredictable soul.",
              "modifiers": {
                "LUCK": 2
              }
            },
            "RUNE_WEAVER": {
              "name": "Rune Weaver",
              "description": "Skilled in aligning runes to enhance Flow potency.",
              "modifiers": {
                "FLOW_RESONANCE": 1,
                "CONCENTRATION": 1
              }
            },
            "CHAOS_AGENT": {
              "name": "Chaos Agent",
              "description": "An unpredictable wildcard who thrives in uncertainty.",
              "modifiers": {
                "LUCK": 1,
                "KHARMA": 1
              }
            },
            "GLITCH_HUNTER": {
              "name": "Glitch Hunter",
              "description": "Tracks anomalies and Flow disturbances with precision.",
              "modifiers": {
                "KNOWLEDGE": 1,
                "CONCENTRATION": 1
              }
            },
            "RESILIENT_OUTCAST": {
              "name": "Resilient Outcast",
              "description": "A survivor hardened by adversity and betrayal.",
              "modifiers": {
                "MENTAL_STRENGTH": 2
              }
            }
          }
      ,
      "characteristics": {
        "PHYSICAL_STRENGTH": {
          "name": "Physical Strength",
          "description": "Influences health and physical damage.",
          "image": "/images/physical_strength.png"
        },
        "MENTAL_STRENGTH": {
          "name": "Mental Strength",
          "description": "Influences energy and mental resilience.",
          "image": "/images/mental_strength.png"
        },
        "LUCK": {
          "name": "Luck",
          "description": "Adds a modifier to various outcomes, often turning the tide in unpredictable situations.",
          "image": "/images/luck.png"
        },
        "SPEED": {
          "name": "Speed",
          "description": "Influences action points and determines turn order during encounters.",
          "image": "/images/speed.png"
        },
        "CONCENTRATION": {
          "name": "Concentration",
          "description": "Ability to maintain spell casting under pressure and focus on precise tasks.",
          "image": "/images/concentration.png"
        },
        "FLOW_MANIPULATION": {
          "name": "Flow Manipulation",
          "description": "Skill in shaping and controlling Flow energy for spells, devices, and abilities.",
          "image": "/images/flow_manipulation.png"
        },
        "FLOW_CONNECTION": {
          "name": "Flow Connection",
          "description": "Depth of bond with the Flow, enhancing spell efficiency and magical awareness.",
          "image": "/images/flow_connection.png"
        },
        "KNOWLEDGE": {
          "name": "Knowledge",
          "description": "Understanding of magical theory, Flow artifacts, and technological applications.",
          "image": "/images/knowledge.png"
        },
        "FLOW_RESONANCE": {
          "name": "Flow Resonance",
          "description": "Ability to align perfectly with the Flow, enhancing the potency and range of spells.",
          "image": "/images/flow_resonance.png"
        },
        "CHARISMA": {
          "name": "Charisma",
          "description": "Ability to influence others, form relationships, and negotiate favorable outcomes.",
          "image": "/images/charisma.png"
        }
      },
      allocatedPoints: {},
    };
  },
  computed: {
    isFormComplete() {
      return (
          this.player.name &&
          this.player.characterName &&
          this.player.age &&
          this.player.gender &&
          this.selectedFeature &&
          Object.keys(this.allocatedPoints).length > 0
      );
    },
  },
  methods: {
    selectPath(pathId) {
      this.player.path = pathId;
    },
    selectFeature(key) {
      this.selectedFeature = key;
    },
    handleAllocation(points) {
      this.allocatedPoints = points;
    },
    submitPlayer() {
      const playerData = {
        ...this.player,
        feature: this.features[this.selectedFeature],
        stats: this.allocatedPoints,
      };
      console.log("Player Submitted:", playerData);
      // Here you can send the data to the server or proceed to the next step
    },
  },
};
</script>

<style scoped>
/* Global Layout */
.player-create {
  background: #1e1e2f; /* Dark cyberpunk background */
  color: #ffffff;
  font-family: "Roboto", sans-serif;
  padding: 20px;
}

h1,
h2 {
  text-align: center;
  color: #4caf50;
}

main {
  max-width: 900px;
  margin: auto;
  padding: 20px;
  background: #23293a; /* Subtle gradient background */
  border-radius: 12px;
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.5);
}

/* Form Elements */
form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

input,
select,
textarea,
button {
  padding: 10px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  outline: none;
  transition: box-shadow 0.2s ease-in-out;
}

input:focus,
select:focus,
textarea:focus {
  box-shadow: 0px 0px 10px #4caf50;
}

textarea {
  resize: vertical;
}

button {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

button:disabled {
  background-color: #555;
  cursor: not-allowed;
}

/* Features Section */
.features {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.feature-item {
  flex: 1 1 calc(33% - 20px);
  background: #2a3142;
  padding: 15px;
  border-radius: 10px;
  border: 2px solid transparent;
  text-align: center;
  transition: border 0.3s ease, transform 0.2s ease;
  cursor: pointer;
}

.feature-item:hover {
  border: 2px solid #4caf50;
  transform: translateY(-5px);
}

.feature-item.selected {
  border: 2px solid #4caf50;
  background: #1f2636;
  transform: translateY(-5px);
}

/* Action Points Section */
.action-points {
  margin-top: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .features {
    flex-direction: column;
    align-items: center;
  }

  .feature-item {
    flex: 1 1 90%;
  }
}
</style>

