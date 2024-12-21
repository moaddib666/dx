<template>
  <div class="character-creation">
    <!-- Step Loader -->
    <div class="step-loader">
      <div
          v-for="(step, index) in steps"
          :key="index"
          :class="['step', { active: currentStep === index, completed: index < currentStep }]"
          @click="goToStep(index)"
      >
        <span class="step-number">{{ index + 1 }}</span>
        <span class="step-label">{{ step.label }}</span>
      </div>
    </div>

    <!-- Step Content -->
    <div class="step-content">
      <component :is="steps[currentStep].component"
                 v-if="steps[currentStep] && steps[currentStep].component"
                 v-bind="steps[currentStep].data"
                 @back="goToPreviousStep"
                 @next="goToNextStep"
      />
    </div>

    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <button
          v-if="currentStep > 0"
          class="back-button"
          @click="goToPreviousStep"
      >
        Back
      </button>
      <button
          v-if="currentStep < steps.length - 1"
          class="next-button"
          @click="goToNextStep"
      >
        Next
      </button>
      <button
          v-if="currentStep === steps.length - 1"
          class="finish-button"
          @click="finishCreation"
      >
        Finish
      </button>
    </div>
  </div>
</template>

<script>
import PathSelector from "@/components/Path/Selector.vue";
import BioComponent from "@/components/Player/Bio.vue";
import FeatureSelector from "@/components/Player/FeatureSelector.vue";
import ActionPointAllocator from "@/components/Player/ActionPointsComponent.vue";
import SchoolAndSpellSelector from "@/components/Player/SchoolAndSpellSelector.vue";
import {PlayerGameApi} from "@/api/backendService.js";

export default {
  name: "CharacterCreation",
  data() {
    return {
      playerData: {
        "data": {
          "name": "string",
          "tags": [],
          "bio": {
            "age": 0,
            "gender": "Male",
            "appearance": "string",
            "background": "string"
          },
          "rank": 0,
          "path": null,
          "stats": [],
          "modificators": [],
          "items": [],
          "schools": [],
          "spells": []
        },
        "validation": {
          "max_stats_points_count": 0,
          "max_modificators_count": 0,
          "max_items_count": 0,
          "max_spells_count": 0,
          "max_rank_grade": 0,
          "max_schools_count": 0
        }
      }, //
      loaded: false,
      currentStep: 0,
      steps: [
        {
          label: "Bio",
          component: BioComponent,
          data: {}
        },
        {
          label: "Path",
          component: PathSelector,
          data: {
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
          }
        },
        {
          label: "Features",
          component: FeatureSelector,
          data: {
            features: {
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
          }
        },
        {
          label: "Action Points",
          component: ActionPointAllocator,
          data: {
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
          }
        },
        {
          label: "School & Spells",
          component: SchoolAndSpellSelector,
          data: {
            schools: [
              {
                "id": "4f9cc24a-52f3-43a3-8e8b-b01a367a504f",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:42:19.566378Z",
                "name": "Cybernetic Enhancements School",
                "description": "Focuses on integrating cybernetic enhancements for increased physical power.",
                "icon": "http://localhost:8000/media/icons/school/Cybernetic_Enhancements_School_q0gevDO.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "de37c984-de4e-437d-ab0a-197fd6eed4c6",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:39:22.829802Z",
                "name": "Techno-Mysticism School",
                "description": "Combines technology with mystical flow manipulation for enhanced abilities.",
                "icon": "http://localhost:8000/media/icons/school/Techno-Mysticism_School.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "684821f8-8cb1-4a70-8273-23a9adcee28d",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:42:07.435502Z",
                "name": "Combat Augmentation School",
                "description": "Specializes in augmentations that enhance combat effectiveness.",
                "icon": "http://localhost:8000/media/icons/school/Combat_Augmentation_School.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "7a7dbdf0-eb61-44df-9ff6-6a099bb0af86",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:41:33.884832Z",
                "name": "Defensive Systems School",
                "description": "Focuses on advanced defensive technologies and energy shields.",
                "icon": "http://localhost:8000/media/icons/school/Defensive_Systems_School.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "8a7ca417-1cfa-4369-9eaf-c6a6bc433f01",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:41:04.695646Z",
                "name": "RobotoTehniche School",
                "description": "Mastery of robots and mechanical systems.",
                "icon": "http://localhost:8000/media/icons/school/RobotoTechniche_School.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "aa531c7f-97ce-4fba-8752-84c90b7cbfdb",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:40:38.399955Z",
                "name": "BufferTech School",
                "description": "Supportive technologies to enhance allies' abilities.",
                "icon": "http://localhost:8000/media/icons/school/BufferTech_School.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "b125adff-1ee0-44f9-bb81-3298c5315001",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:40:22.814781Z",
                "name": "MedTech School",
                "description": "Advanced medical technologies and healing techniques.",
                "icon": "http://localhost:8000/media/icons/school/Heal_School.webp",
                "path": [
                  "c7b92d32-4c21-4a29-84c2-469e4f888d31"
                ]
              },
              {
                "id": "b67d811d-e401-46b5-b13c-6e6e4111a142",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:39:52.322550Z",
                "name": "Fire School",
                "description": "Mastery of fire-based attacks and defense.",
                "icon": "http://localhost:8000/media/icons/school/Fire_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "2be5bff8-4d58-45b9-b995-49a59950a3ac",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:43:21.714365Z",
                "name": "Water School",
                "description": "Control over water for versatile attacks and healing.",
                "icon": "http://localhost:8000/media/icons/school/Water_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "8743f3ee-a8cd-490e-a462-8bb14a5471d8",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:41:13.434108Z",
                "name": "Blood School",
                "description": "Manipulation of blood for powerful and deadly attacks.",
                "icon": "http://localhost:8000/media/icons/school/Blood_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "bb92d487-102d-462c-acf5-d176a26f9ad0",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:39:35.426912Z",
                "name": "PureEnergy School",
                "description": "Balanced use of pure energy for attack and defense.",
                "icon": "http://localhost:8000/media/icons/school/PureEnergy_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "700de899-6ea2-4afd-a9c8-a8c6386a7470",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:41:42.371321Z",
                "name": "Dark School",
                "description": "Harnesses the power of darkness for attacks and debuffs.",
                "icon": "http://localhost:8000/media/icons/school/Dark_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "b62dfea2-3e38-47f3-989b-5c075001b54d",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:40:04.990444Z",
                "name": "Light School",
                "description": "Uses light for powerful attacks and healing.",
                "icon": "http://localhost:8000/media/icons/school/Light_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "962bd011-7908-414f-bdd5-083db28ee763",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:40:49.936840Z",
                "name": "Mirage School",
                "description": "Creates illusions and defensive barriers.",
                "icon": "http://localhost:8000/media/icons/school/Mirage_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "6a55bc8c-d469-4f67-9842-c59a09906864",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:41:51.502367Z",
                "name": "Heal School",
                "description": "Focuses on advanced healing techniques and support magic.",
                "icon": "http://localhost:8000/media/icons/school/Heal_School_3hYKjNZ.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "0896047b-d72d-44cd-9e8c-7653521abe0c",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:43:48.738620Z",
                "name": "Constructor School",
                "description": "Masters the construction of magical barriers and golems.",
                "icon": "http://localhost:8000/media/icons/school/Constructor_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "35d4b270-14f3-42fb-83ab-6cb505c8005d",
                "created_at": "2024-06-09T14:00:24Z",
                "updated_at": "2024-12-16T18:43:05.161314Z",
                "name": "Summon School",
                "description": "Specializes in summoning creatures and allies for battle.",
                "icon": "http://localhost:8000/media/icons/school/Summon_School.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              },
              {
                "id": "43607b12-9f49-4993-99ba-a416daa8da10",
                "created_at": "2024-06-09T16:50:56Z",
                "updated_at": "2024-12-16T18:42:38.341237Z",
                "name": "FireArtsSchool",
                "description": "Description for FireArtsSchool",
                "icon": "http://localhost:8000/media/icons/school/Fire_School_4GpzAH5.webp",
                "path": [
                  "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
                ]
              }
            ],
            spells: [
              {
                "id": 14,
                "name": "Spark",
                "grade": 1,
                "description": "A small spark that ignites the target the skill is built on top of the Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": false,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 15,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 4
                  },
                  {
                    "kind": "Energy",
                    "value": 5
                  }
                ],
                "effect": [
                  {
                    "name": "Burn",
                    "chance": 0.2,
                    "durationSeconds": 60,
                    "description": "5 heat damage per turn for 2 turns with 20% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 15,
                "name": "Ember Burst",
                "grade": 2,
                "description": "A burst of embers that can cause burning, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": false,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 20,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 4
                  },
                  {
                    "kind": "Energy",
                    "value": 5
                  }
                ],
                "effect": [
                  {
                    "name": "Burn",
                    "chance": 0.15,
                    "durationSeconds": 60,
                    "description": "10 heat damage per turn for 2 turns with 15% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 16,
                "name": "Flame Wave",
                "grade": 3,
                "description": "A wave of fire that burns targets in a line, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 30,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 5
                  },
                  {
                    "kind": "Energy",
                    "value": 10
                  }
                ],
                "effect": [
                  {
                    "name": "Burn",
                    "chance": 0.25,
                    "durationSeconds": 60,
                    "description": "5 heat damage per turn for 2 turns with 25% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 17,
                "name": "Inferno Blast",
                "grade": 4,
                "description": "Creates an inferno that causes severe burns, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 40,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 6
                  },
                  {
                    "kind": "Energy",
                    "value": 15
                  }
                ],
                "effect": [
                  {
                    "name": "Defense Reduction",
                    "chance": 0.3,
                    "durationSeconds": 120,
                    "description": "Reduces targets' defense by 10% for 2 turns"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 18,
                "name": "Scorching Ray",
                "grade": 5,
                "description": "A focused ray of intense heat, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": false,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 55,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 6
                  },
                  {
                    "kind": "Energy",
                    "value": 20
                  }
                ],
                "effect": [
                  {
                    "name": "Severe Burn",
                    "chance": 0.35,
                    "durationSeconds": 180,
                    "description": "10 heat damage per turn for 3 turns with 35% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 19,
                "name": "Blazing Shield",
                "grade": 5,
                "description": "A shield of flames that reduces incoming damage, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the defense by 10%.",
                "multi_target": false,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Defense",
                    "type": "Heat",
                    "formula": {
                      "base": 30,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.1
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 5
                  },
                  {
                    "kind": "Energy",
                    "value": 10
                  }
                ],
                "effect": [
                  {
                    "name": "Heat Damage",
                    "chance": 0.2,
                    "durationSeconds": 180,
                    "description": "Deals 10 heat damage to attackers with 20% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 20,
                "name": "Pyroclasm",
                "grade": 6,
                "description": "Unleashes a pyroclasm that engulfs the area in flames, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 70,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 7
                  },
                  {
                    "kind": "Energy",
                    "value": 25
                  }
                ],
                "effect": [
                  {
                    "name": "Ignite",
                    "chance": 0.4,
                    "durationSeconds": 60,
                    "description": "10 heat damage per turn for 2 turns with 40% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 21,
                "name": "Volcanic Eruption",
                "grade": 7,
                "description": "Causes a volcanic eruption that engulfs a large area in flames, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 85,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 8
                  },
                  {
                    "kind": "Energy",
                    "value": 30
                  }
                ],
                "effect": [
                  {
                    "name": "Speed Reduction",
                    "chance": 0.5,
                    "durationSeconds": 120,
                    "description": "Reduces targets' speed by 10% for 2 turns"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 22,
                "name": "Molten Armor",
                "grade": 7,
                "description": "Armor of molten rock that reduces incoming damage, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the defense by 10%.",
                "multi_target": false,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Defense",
                    "type": "Heat",
                    "formula": {
                      "base": 40,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.1
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 7
                  },
                  {
                    "kind": "Energy",
                    "value": 25
                  }
                ],
                "effect": [
                  {
                    "name": "Heat Damage",
                    "chance": 0.3,
                    "durationSeconds": 240,
                    "description": "Deals 15 heat damage to attackers with 30% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 23,
                "name": "Meteor Storm",
                "grade": 8,
                "description": "Summons a storm of meteors that devastate a large area, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 100,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 9
                  },
                  {
                    "kind": "Energy",
                    "value": 35
                  }
                ],
                "effect": [
                  {
                    "name": "Massive Burn",
                    "chance": 0.6,
                    "durationSeconds": 180,
                    "description": "20 heat damage per turn for 3 turns with 60% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 24,
                "name": "Hellfire",
                "grade": 9,
                "description": "Unleashes the flames of the underworld, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 120,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 10
                  },
                  {
                    "kind": "Energy",
                    "value": 40
                  }
                ],
                "effect": [
                  {
                    "name": "Ignite",
                    "chance": 0.7,
                    "durationSeconds": 180,
                    "description": "15 heat damage per turn for 3 turns with 70% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 25,
                "name": "Dragon's Breath",
                "grade": 9,
                "description": "Emulates the breath of a dragon, spewing fire in a cone, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 110,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 9
                  },
                  {
                    "kind": "Energy",
                    "value": 35
                  }
                ],
                "effect": [
                  {
                    "name": "Burning",
                    "chance": 0.5,
                    "durationSeconds": 180,
                    "description": "15 heat damage per turn for 3 turns with 50% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              },
              {
                "id": 26,
                "name": "Fiery Cataclysm",
                "grade": 10,
                "description": "Causes a fiery cataclysm that engulfs the area in intense flames, built on Flow Manipulation and scaled by it. Each point in Flow Manipulation increases the damage by 10%.",
                "multi_target": true,
                "type": "attack",
                "impact": [
                  {
                    "kind": "Damage",
                    "type": "Heat",
                    "formula": {
                      "base": 130,
                      "requires": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 5
                        }
                      ],
                      "scaling": [
                        {
                          "stat": "Flow Manipulation",
                          "value": 0.2
                        }
                      ]
                    }
                  }
                ],
                "cost": [
                  {
                    "kind": "Action Points",
                    "value": 10
                  },
                  {
                    "kind": "Energy",
                    "value": 45
                  }
                ],
                "effect": [
                  {
                    "name": "Catastrophic Burn",
                    "chance": 0.8,
                    "durationSeconds": 180,
                    "description": "20 heat damage per turn for 3 turns with 80% chance"
                  }
                ],
                "icon": null,
                "school": "43607b12-9f49-4993-99ba-a416daa8da10"
              }
            ]
          }
        },
      ],
    };
  },
  async mounted() {
    await this.getPlayerTemplate()
  },
  methods: {
    goToStep(index) {
      if (index >= 0 && index < this.steps.length) {
        this.currentStep = index;
      }
    },
    goToNextStep() {
      if (this.currentStep < this.steps.length - 1) {
        this.currentStep += 1;
      }
    },
    goToPreviousStep() {
      if (this.currentStep > 0) {
        this.currentStep -= 1;
      }
    },
    finishCreation() {
      // Handle character creation completion
      console.log("Character Creation Finished", this.steps.map(step => step.data));
    },
    async getPlayerTemplate() {
      this.playerData = (await PlayerGameApi.playerPlayerTemplateRetrieve()).data;
      this.loaded = true
    },
  },
};
</script>

<style scoped>
/* Step Loader */
.step-loader {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #2d2d2d;
  border-radius: 8px;
}

.step {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.step.completed .step-number {
  background-color: #4caf50; /* Green for completed steps */
}

.step.active .step-number {
  background-color: #2196f3; /* Blue for the active step */
}

.step-number {
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  border-radius: 50%;
  background-color: #757575;
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.step-label {
  color: #ddd;
  font-size: 14px;
}

.step.active .step-label {
  font-weight: bold;
  color: white;
}

/* Step Content */
.step-content {
  margin: 20px 0;
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button {
  background-color: #757575;
  color: white;
}

.back-button:hover {
  background-color: #616161;
}

.next-button, .finish-button {
  background-color: #2196f3;
  color: white;
}

.next-button:hover, .finish-button:hover {
  background-color: #1976d2;
}
</style>
