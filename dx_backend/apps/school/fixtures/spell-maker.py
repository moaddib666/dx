import json
import uuid
from datetime import datetime

# Load the JSON data from files
with open('/mnt/data/ranks_fixture.json', 'r') as f:
    ranks_fixture = json.load(f)

with open('/mnt/data/schools_fixture.json', 'r') as f:
    schools_fixture = json.load(f)

with open('/mnt/data/the_path_fixture.json', 'r') as f:
    paths_fixture = json.load(f)

# Define a broader list of skills and impacts
skills_and_impacts = {
    "Cybernetic Enhancements School": {
        "skills": [
            {"name": "Enhanced Strength", "description": "Increases physical attack power.", "impacts": ["Physical"]},
            {"name": "Energy Shield", "description": "Reduces incoming damage by 25% for 3 turns.",
             "impacts": ["Energy"]}
        ],
        "impacts": {
            "Physical": {"base_value": 10, "type": "Physical",
                         "description": "Increased physical strength from enhancements."},
            "Energy": {"base_value": 15, "type": "Energy",
                       "description": "Enhanced energy reserves for longer endurance."}
        }
    },
    "Techno-Mysticism School": {
        "skills": [
            {"name": "Mystic Bolt", "description": "Deals mystical energy damage.", "impacts": ["Energy"]},
            {"name": "Shield of Light", "description": "Creates a shield that absorbs damage.", "impacts": ["Light"]}
        ],
        "impacts": {
            "Energy": {"base_value": 15, "type": "Energy", "description": "Mystical energy damage."},
            "Light": {"base_value": 20, "type": "Light", "description": "Light shield that absorbs damage."}
        }
    },
    "Combat Augmentation School": {
        "skills": [
            {"name": "Combat Reflexes", "description": "Increases reaction time in combat.", "impacts": ["Speed"]},
            {"name": "Augmented Strike", "description": "Powerful physical strike.", "impacts": ["Physical"]}
        ],
        "impacts": {
            "Speed": {"base_value": 10, "type": "Speed", "description": "Increased combat reaction time."},
            "Physical": {"base_value": 15, "type": "Physical", "description": "Powerful physical strike."}
        }
    },
    "Defensive Systems School": {
        "skills": [
            {"name": "Barrier", "description": "Creates a barrier to block attacks.", "impacts": ["Shield"]},
            {"name": "Defensive Stance", "description": "Reduces incoming damage.", "impacts": ["Defense"]}
        ],
        "impacts": {
            "Shield": {"base_value": 20, "type": "Shield", "description": "Barrier to block attacks."},
            "Defense": {"base_value": 10, "type": "Defense", "description": "Reduces incoming damage."}
        }
    },
    "RobotoTehniche School": {
        "skills": [
            {"name": "Robot Command", "description": "Commands a robot to attack.", "impacts": ["Command"]},
            {"name": "Mechanical Repair", "description": "Repairs a robot.", "impacts": ["Repair"]}
        ],
        "impacts": {
            "Command": {"base_value": 15, "type": "Command", "description": "Commands a robot to attack."},
            "Repair": {"base_value": 20, "type": "Repair", "description": "Repairs a robot."}
        }
    },
    "BufferTech School": {
        "skills": [
            {"name": "Power Boost", "description": "Increases allies' power.", "impacts": ["Buff"]},
            {"name": "Energy Transfer", "description": "Transfers energy to an ally.", "impacts": ["Energy"]}
        ],
        "impacts": {
            "Buff": {"base_value": 15, "type": "Buff", "description": "Increases allies' power."},
            "Energy": {"base_value": 10, "type": "Energy", "description": "Transfers energy to an ally."}
        }
    },
    "MedTech School": {
        "skills": [
            {"name": "Healing Wave", "description": "Heals multiple allies.", "impacts": ["Healing"]},
            {"name": "Revitalize", "description": "Revives a fallen ally.", "impacts": ["Revive"]}
        ],
        "impacts": {
            "Healing": {"base_value": 25, "type": "Healing", "description": "Heals multiple allies."},
            "Revive": {"base_value": 30, "type": "Revive", "description": "Revives a fallen ally."}
        }
    },
    "Fire School": {
        "skills": [
            {"name": "Fireball", "description": "Deals fire damage to a single target.", "impacts": ["Heat"]},
            {"name": "Flame Shield", "description": "Creates a shield of fire.", "impacts": ["Heat", "Shield"]}
        ],
        "impacts": {
            "Heat": {"base_value": 20, "type": "Heat", "description": "Deals fire damage."},
            "Shield": {"base_value": 10, "type": "Shield", "description": "Shield of fire."}
        }
    },
    "Water School": {
        "skills": [
            {"name": "Water Blast", "description": "Deals water damage to a single target.", "impacts": ["Cold"]},
            {"name": "Healing Rain", "description": "Heals allies over time.", "impacts": ["Healing"]}
        ],
        "impacts": {
            "Cold": {"base_value": 20, "type": "Cold", "description": "Deals water damage."},
            "Healing": {"base_value": 15, "type": "Healing", "description": "Heals over time."}
        }
    },
    "Blood School": {
        "skills": [
            {"name": "Blood Drain", "description": "Steals health from an enemy.", "impacts": ["Drain"]},
            {"name": "Blood Shield", "description": "Creates a shield from blood.", "impacts": ["Shield", "Drain"]}
        ],
        "impacts": {
            "Drain": {"base_value": 15, "type": "Drain", "description": "Steals health."},
            "Shield": {"base_value": 10, "type": "Shield", "description": "Shield from blood."}
        }
    },
    "PureEnergy School": {
        "skills": [
            {"name": "Energy Blast", "description": "Deals energy damage to a single target.", "impacts": ["Energy"]},
            {"name": "Energy Barrier", "description": "Creates an energy barrier.", "impacts": ["Energy", "Shield"]}
        ],
        "impacts": {
            "Energy": {"base_value": 20, "type": "Energy", "description": "Deals energy damage."},
            "Shield": {"base_value": 10, "type": "Shield", "description": "Energy barrier."}
        }
    },
    "Dark School": {
        "skills": [
            {"name": "Shadow Strike", "description": "Deals dark damage to a single target.", "impacts": ["Darkness"]},
            {"name": "Dark Barrier", "description": "Creates a dark barrier.", "impacts": ["Darkness", "Shield"]}
        ],
        "impacts": {
            "Darkness": {"base_value": 20, "type": "Darkness", "description": "Deals dark damage."},
            "Shield": {"base_value": 10, "type": "Shield", "description": "Dark barrier."}
        }
    },
    "Light School": {
        "skills": [
            {"name": "Light Beam", "description": "Deals light damage to a single target.", "impacts": ["Light"]},
            {"name": "Holy Shield", "description": "Creates a shield of light.", "impacts": ["Light", "Shield"]}
        ],
        "impacts": {
            "Light": {"base_value": 20, "type": "Light", "description": "Deals light damage."},
            "Shield": {"base_value": 10, "type": "Shield", "description": "Shield of light."}
        }
    },
    "Mirage School": {
        "skills": [
            {"name": "Mirage", "description": "Creates an illusion to distract enemies.", "impacts": ["Illusion"]},
            {"name": "Phantom Shield", "description": "Creates a phantom shield.", "impacts": ["Illusion", "Shield"]}
        ],
        "impacts": {
            "Illusion": {"base_value": 15, "type": "Illusion", "description": "Creates an illusion."},
            "Shield": {"base_value": 10, "type": "Shield", "description": "Phantom shield."}
        }
    },
    "Heal School": {
        "skills": [
            {"name": "Greater Healing", "description": "Heals a large amount of health.", "impacts": ["Healing"]},
            {"name": "Resurrect", "description": "Revives a fallen ally.", "impacts": ["Revive"]}
        ],
        "impacts": {
            "Healing": {"base_value": 25, "type": "Healing", "description": "Heals a large amount of health."},
            "Revive": {"base_value": 30, "type": "Revive", "description": "Revives a fallen ally."}
        }
    },
    "Constructor School": {
        "skills": [
            {"name": "Barrier Construction", "description": "Constructs a magical barrier.", "impacts": ["Shield"]},
            {"name": "Golem Summon", "description": "Summons a magical golem.", "impacts": ["Summon"]}
        ],
        "impacts": {
            "Shield": {"base_value": 20, "type": "Shield", "description": "Constructs a barrier."},
            "Summon": {"base_value": 25, "type": "Summon", "description": "Summons a golem."}
        }
    },
    "Summon School": {
        "skills": [
            {"name": "Summon Beast", "description": "Summons a beast to fight for you.", "impacts": ["Summon"]},
            {"name": "Summon Ally", "description": "Summons an ally to assist you.", "impacts": ["Summon"]}
        ],
        "impacts": {
            "Summon": {"base_value": 25, "type": "Summon", "description": "Summons a creature or ally."}
        }
    }
}

# Create mappings for school and rank IDs
school_name_to_id = {school["fields"]["name"]: school["pk"] for school in schools_fixture}
rank_name_to_id = {rank["fields"]["name"]: rank["pk"] for rank in ranks_fixture}


# Generate the impact data
def generate_impacts(skills_and_impacts):
    impact_fixture = []

    def create_impact(base_value, type, description):
        return {
            "model": "school.impact",
            "pk": str(uuid.uuid4()),
            "fields": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "base_value": base_value,
                "type": type,
                "description": description
            }
        }

    for school in skills_and_impacts.values():
        for impact in school["impacts"].values():
            impact_fixture.append(create_impact(impact["base_value"], impact["type"], impact["description"]))

    return impact_fixture


# Generate the fixture for impacts
impacts_fixture = generate_impacts(skills_and_impacts)

# Create a mapping from impact type to impact ID (UUID)
impact_type_to_id = {impact["fields"]["type"]: impact["pk"] for impact in impacts_fixture}


# Generate the skill data
def generate_skills(skills_and_impacts):
    skill_fixture = []

    def create_skill(name, description, level, school, impacts):
        return {
            "model": "school.skill",
            "pk": str(uuid.uuid4()),
            "fields": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "name": name,
                "description": description,
                "level": level,
                "school": school,
                "impacts": impacts,
                "effects": []
            }
        }

    for school_name, details in skills_and_impacts.items():
        school_id = school_name_to_id[school_name]
        for level, skill in enumerate(details["skills"], start=1):
            impact_ids = [impact_type_to_id[impact] for impact in skill["impacts"]]
            skill_fixture.append(create_skill(skill["name"], skill["description"], level, school_id, impact_ids))

    return skill_fixture


# Generate the fixture for skills
skills_fixture = generate_skills(skills_and_impacts)

# Save the fixtures to JSON files
with open('impacts_fixture.json', 'w') as f:
    json.dump(impacts_fixture, f, indent=2)

with open('skills_fixture.json', 'w') as f:
    json.dump(skills_fixture, f, indent=2)

# Output the generated fixtures for verification
print(json.dumps(impacts_fixture, indent=2))
print(json.dumps(skills_fixture, indent=2))
