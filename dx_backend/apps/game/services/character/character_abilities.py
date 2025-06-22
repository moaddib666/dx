import typing as t

from apps.core.models import CharacterAbility, SkillTypes
from apps.game.services.cost import DefaultCostService
from apps.game.services.skills.power import get_skill_power, SkillPowerComparer

if t.TYPE_CHECKING:
    from apps.game.services.character.core import CharacterService


class CharacterAbilities:

    def can(self, character: "CharacterService", skill_type: "SkillTypes") -> CharacterAbility:
        """
        Check if the character can perform actions of the given skill type.
        Returns skills and items sorted by power (most powerful first).
        """
        learned_skills = character.character.learned_skills.filter(
            character=character.character,
            skill__type=skill_type,
        ).order_by("skill__grade")

        owned_items = character.character.equipped_items.filter(
            world_item__item__skill__type=skill_type
        ).order_by("world_item__item__skill__grade")

        # Filter skills and items that character can afford
        possible_skills = list(filter(
            lambda skill: DefaultCostService.validate(
                cost=skill.skill.cost,
                character_svc=character,
                raise_exception=False
            ),
            learned_skills
        ))

        possible_items = list(filter(
            lambda item: DefaultCostService.validate(
                cost=item.world_item.item.skill.cost,
                character_svc=character,
                raise_exception=False
            ),
            owned_items
        ))

        # Sort skills by power (most powerful first)
        sorted_skills = sorted(
            possible_skills,
            key=lambda skill_obj: get_skill_power(skill_obj.skill),
            reverse=True
        )

        # Sort items by their skill's power (most powerful first)
        sorted_items = sorted(
            possible_items,
            key=lambda item_obj: get_skill_power(item_obj.world_item.item.skill),
            reverse=True
        )

        return CharacterAbility(
            type=skill_type,
            skills=(skill.skill.id for skill in sorted_skills),
            items=(item.world_item.item.id for item in sorted_items)
        )

    def can_with_power_details(self, character: "CharacterService", skill_type: "SkillTypes") -> dict:
        """
        Extended version that returns detailed power information for debugging/UI.
        """
        learned_skills = character.character.learned_skills.filter(
            character=character.character,
            skill__type=skill_type,
        ).order_by("skill__grade")

        owned_items = character.character.equipped_items.filter(
            world_item__item__skill__type=skill_type
        ).order_by("world_item__item__skill__grade")

        # Filter and collect skills with power ratings
        possible_skills = []
        for skill_obj in learned_skills:
            if DefaultCostService.validate(
                    cost=skill_obj.skill.cost,
                    character_svc=character,
                    raise_exception=False
            ):
                power = get_skill_power(skill_obj.skill)
                possible_skills.append({
                    'skill_obj': skill_obj,
                    'skill_id': skill_obj.skill.id,
                    'power_rating': power,
                    'grade': skill_obj.skill.grade
                })

        # Filter and collect items with power ratings
        possible_items = []
        for item_obj in owned_items:
            if DefaultCostService.validate(
                    cost=item_obj.world_item.item.skill.cost,
                    character_svc=character,
                    raise_exception=False
            ):
                power = get_skill_power(item_obj.world_item.item.skill)
                possible_items.append({
                    'item_obj': item_obj,
                    'item_id': item_obj.world_item.item.id,
                    'skill_id': item_obj.world_item.item.skill.id,
                    'power_rating': power,
                    'grade': item_obj.world_item.item.skill.grade
                })

        # Sort by power
        sorted_skills = sorted(possible_skills, key=lambda x: x['power_rating'], reverse=True)
        sorted_items = sorted(possible_items, key=lambda x: x['power_rating'], reverse=True)

        return {
            'type': skill_type,
            'skills': sorted_skills,
            'items': sorted_items,
            'skill_ids': [s['skill_id'] for s in sorted_skills],
            'item_ids': [i['item_id'] for i in sorted_items]
        }

    def get_best_skill(self, character: "CharacterService", skill_type: "SkillTypes"):
        """
        Get the single most powerful skill/item the character can use.
        """
        ability = self.can_with_power_details(character, skill_type)

        # Find the most powerful option between skills and items
        best_skill = ability['skills'][0] if ability['skills'] else None
        best_item = ability['items'][0] if ability['items'] else None

        if not best_skill and not best_item:
            return None
        elif not best_skill:
            return {'type': 'item', 'data': best_item}
        elif not best_item:
            return {'type': 'skill', 'data': best_skill}
        else:
            # Compare power ratings
            if best_skill['power_rating'] >= best_item['power_rating']:
                return {'type': 'skill', 'data': best_skill}
            else:
                return {'type': 'item', 'data': best_item}

    def preload_skill_cache(self, character: "CharacterService"):
        """
        Preload cache for all character's skills to improve performance.
        Call this during character loading or session start.
        """
        # Get all skills from learned skills and equipped items
        all_skills = []

        # Add learned skills
        for learned_skill in character.character.learned_skills.all():
            all_skills.append(learned_skill.skill)

        # Add item skills
        for equipped_item in character.character.equipped_items.all():
            if hasattr(equipped_item.world_item.item, 'skill'):
                all_skills.append(equipped_item.world_item.item.skill)

        # Preload cache for all unique skills
        unique_skills = list(set(all_skills))
        SkillPowerComparer.preload_cache(unique_skills)


default_abilities = CharacterAbilities()


def can(character: "CharacterService", skill_type: "SkillTypes") -> CharacterAbility:
    """
    Check if the character can perform an action of the given skill type.
    Returns skills and items sorted by power (most powerful first).
    """
    return default_abilities.can(character, skill_type)


def can_with_details(character: "CharacterService", skill_type: "SkillTypes") -> dict:
    """
    Extended version with power details for debugging/UI.
    """
    return default_abilities.can_with_power_details(character, skill_type)


def get_best_option(character: "CharacterService", skill_type: "SkillTypes"):
    """
    Get the single best skill or item for the given type.
    """
    return default_abilities.get_best_skill(character, skill_type)
