import json

# Sample JSON data
data = '''
{
  "skills": [
    {
      "name": "Fireball",
      "base_damage": 10,
      "required_skills": {
        "fire_magic": 5,
        "intelligence": 3
      },
      "scaling_factors": {
        "fire_magic": 0.6,
        "intelligence": 0.4
      }
    },
    {
      "name": "Ice Spear",
      "base_damage": 12,
      "required_skills": {
        "ice_magic": 4,
        "dexterity": 2
      },
      "scaling_factors": {
        "ice_magic": 0.5,
        "dexterity": 0.5
      }
    }
  ],
  "stats": {
    "fire_magic": 7,
    "intelligence": 6,
    "ice_magic": 5,
    "dexterity": 3
  }
}
'''

# Load JSON data
game_data = json.loads(data)

class SkillService:
    def __init__(self, skills, stats):
        self.skills = {skill["name"]: skill for skill in skills}
        self.stats = stats

    def calculate_damage(self, skill_name):
        skill = self.skills[skill_name]
        base_damage = skill["base_damage"]
        required_skills = skill["required_skills"]
        scaling_factors = skill["scaling_factors"]

        damage = base_damage
        for stat, required_level in required_skills.items():
            scaling_factor = scaling_factors[stat]
            current_level = self.stats.get(stat, 0)
            damage *= (1 + scaling_factor * (current_level - required_level) / required_level)

        return damage

# Example usage
skill_service = SkillService(game_data["skills"], game_data["stats"])

# Process action done by player (example: using Fireball skill)
skill_name = "Fireball"
damage = skill_service.calculate_damage(skill_name)
print(f"Damage for {skill_name}: {damage}")

# You can similarly calculate damage for other skills as needed
skill_name = "Ice Spear"
damage = skill_service.calculate_damage(skill_name)
print(f"Damage for {skill_name}: {damage}")
