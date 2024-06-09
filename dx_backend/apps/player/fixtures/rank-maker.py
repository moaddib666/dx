import json
import uuid
from datetime import datetime

# Define the base rank structure with variable sub-ranks
base_ranks = [
    {"name": "Only a Human",
     "description": "Regular individuals with no Flow powers or significant combat training. They live ordinary lives, unaware of the mystical and technological complexities of the higher dimensions.",
     "sub_ranks": 0},
    {"name": "Novice",
     "description": "Newly touched by the Flow or just beginning to explore technological enhancements. They possess minimal skills and knowledge, often seeking guidance from more experienced individuals.",
     "sub_ranks": 1},
    {"name": "Initiate",
     "description": "Individuals who have chosen a path (Way of JSon or Way of John) and are learning the basics of their chosen discipline. They are gaining confidence and control over their abilities.",
     "sub_ranks": 2},
    {"name": "Apprentice",
     "description": "Characters who have shown promise and dedication to their path. They have a solid understanding of their abilities and can handle minor challenges independently.",
     "sub_ranks": 3},
    {"name": "Adept",
     "description": "Skilled individuals who have gained significant experience and mastery over their abilities. They are respected within their communities and can take on challenging tasks.",
     "sub_ranks": 3},
    {"name": "Mercenary",
     "description": "Highly skilled fighters, often working as hired guns or protectors. They are adept at both combat and survival, with a reputation for getting the job done.",
     "sub_ranks": 3},
    {"name": "Veteran",
     "description": "Experienced warriors and scholars who have faced numerous battles and challenges. They possess deep knowledge and refined skills, often mentoring novices and apprentices.",
     "sub_ranks": 4},
    {"name": "Master",
     "description": "Elite individuals who have reached the pinnacle of their chosen path. They are renowned for their extraordinary abilities and wisdom, often playing pivotal roles in major events.",
     "sub_ranks": 4},
    {"name": "Grandmaster",
     "description": "Rare and exceptional figures who have surpassed the limits of ordinary mastery. They are revered for their near-mythical prowess and contributions to their disciplines.",
     "sub_ranks": 5},
    {"name": "Legend",
     "description": "Icons whose deeds and abilities have become the stuff of legend. They are celebrated across dimensions, their names etched into the annals of history.",
     "sub_ranks": 6},
    {"name": "God Flow",
     "description": "Beings who have attained a near-divine connection with the Flow, existing beyond the mortal realm. Their power transcends conventional understanding, capable of reshaping reality itself.",
     "sub_ranks": 7}
]


# Define the function to generate ranks
def generate_ranks(base_experience, factor):
    rank_fixture = []

    def create_rank(name, description, experience_needed, grade=0):
        print(f"Creating rank: {name}, {experience_needed} XP grade {grade}")
        return {
            "model": "player.rank",
            "pk": str(uuid.uuid4()),
            "fields": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "name": name,
                "grade": grade,
                "description": description,
                "experience_needed": experience_needed,
                "next_rank": None
            }
        }

    previous_rank_id = None
    current_experience = base_experience
    for i, rank in enumerate(base_ranks):
        main_rank = create_rank(rank["name"], rank["description"], current_experience, grade=i)
        rank_fixture.append(main_rank)
        previous_rank_id = main_rank["pk"]

        for j in range(1, rank["sub_ranks"] + 1):
            current_experience *= factor
            sub_rank_name = f"{rank['name']} {'+' * j}"
            sub_rank = create_rank(sub_rank_name, f"A more experienced version of {rank['name']}.", current_experience, grade=i)
            rank_fixture[-1]["fields"]["next_rank"] = sub_rank["pk"]
            rank_fixture.append(sub_rank)
            previous_rank_id = sub_rank["pk"]

        current_experience *= factor

    # Set the next_rank field correctly
    for i in range(len(rank_fixture) - 1):
        rank_fixture[i]["fields"]["next_rank"] = rank_fixture[i + 1]["pk"]

    return rank_fixture


# Generate the fixture with geometric growth for experience
base_experience = 100
factor = 2
ranks_fixture = generate_ranks(base_experience, factor)

# Save the fixture to a JSON file
with open('ranks_fixture.json', 'w') as f:
    json.dump(ranks_fixture, f, indent=2)

# Output the generated fixture for verification