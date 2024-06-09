import json
import uuid
from datetime import datetime

# Define the paths
paths = {
    "Path of John": "c7b92d32-4c21-4a29-84c2-469e4f888d31",
    "Path of JSon": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
}

# Define the schools
schools = [
    {"name": "Cybernetic Enhancements School",
     "description": "Focuses on integrating cybernetic enhancements for increased physical power.",
     "required_rank_name": "Novice", "path": paths["Path of John"]},
    {"name": "Techno-Mysticism School",
     "description": "Combines technology with mystical flow manipulation for enhanced abilities.",
     "required_rank_name": "Novice", "path": paths["Path of John"]},
    {"name": "Combat Augmentation School",
     "description": "Specializes in augmentations that enhance combat effectiveness.",
     "required_rank_name": "Novice", "path": paths["Path of John"]},
    {"name": "Defensive Systems School",
     "description": "Focuses on advanced defensive technologies and energy shields.", "required_rank_name": "Novice",
     "path": paths["Path of John"]},
    {"name": "RobotoTehniche School", "description": "Mastery of robots and mechanical systems.",
     "required_rank_name": "Novice", "path": paths["Path of John"]},
    {"name": "BufferTech School", "description": "Supportive technologies to enhance allies' abilities.",
     "required_rank_name": "Novice", "path": paths["Path of John"]},
    {"name": "MedTech School", "description": "Advanced medical technologies and healing techniques.",
     "required_rank_name": "Novice", "path": paths["Path of John"]},
    {"name": "Fire School", "description": "Mastery of fire-based attacks and defense.", "required_rank_name": "Novice",
     "path": paths["Path of JSon"]},
    {"name": "Water School", "description": "Control over water for versatile attacks and healing.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Blood School", "description": "Manipulation of blood for powerful and deadly attacks.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "PureEnergy School", "description": "Balanced use of pure energy for attack and defense.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Dark School", "description": "Harnesses the power of darkness for attacks and debuffs.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Light School", "description": "Uses light for powerful attacks and healing.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Mirage School", "description": "Creates illusions and defensive barriers.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Heal School", "description": "Focuses on advanced healing techniques and support magic.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Constructor School", "description": "Masters the construction of magical barriers and golems.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]},
    {"name": "Summon School", "description": "Specializes in summoning creatures and allies for battle.",
     "required_rank_name": "Novice", "path": paths["Path of JSon"]}
]

# Retrieve the ranks generated previously
with open('ranks_fixture.json', 'r') as f:
    ranks_fixture = json.load(f)

# Create a mapping from rank name to rank ID (UUID)
rank_name_to_id = {rank["fields"]["name"]: rank["pk"] for rank in ranks_fixture}


# Generate the school data
def generate_schools(schools):
    school_fixture = []

    def create_school(name, description, required_rank, path):
        return {
            "model": "school.school",
            "pk": str(uuid.uuid4()),
            "fields": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "name": name,
                "description": description,
                "required_rank": required_rank,
                "path": [path]
            }
        }

    for school in schools:
        required_rank_id = rank_name_to_id[school["required_rank_name"]]
        school_fixture.append(create_school(school["name"], school["description"], required_rank_id, school["path"]))

    return school_fixture


# Generate the fixture for schools
schools_fixture = generate_schools(schools)

# Save the fixture to a JSON file
with open('schools_fixture.json', 'w') as f:
    json.dump(schools_fixture, f, indent=2)

# Output the generated fixture for verification
print(json.dumps(schools_fixture, indent=2))
