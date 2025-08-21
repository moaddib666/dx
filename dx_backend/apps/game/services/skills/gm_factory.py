import typing as t
from abc import abstractmethod

from apps.core.models.skills import BaseSkill
from apps.school.models import Skill


class GmSkillFactoryProto(t.Protocol):
    """
    Factory class for creating game primary skills.
    This class is responsible for creating and managing skills in the game.
    """

    @abstractmethod
    def create_skill(self, skill_data: "BaseSkill") -> Skill:
        """
        Create a new skill based on the provided skill data.

        :param skill_data: The data for the skill to be created.
        :return: The created Skill instance.
        """
        pass


class GmManualSkillCreationFactory(GmSkillFactoryProto):
    """
    Factory class for creating game primary skills manually.
    This class is responsible for creating and managing skills in the game.
    """

    def create_skill(self, skill_data: BaseSkill) -> Skill:
        """
        Create a new skill based on the provided skill data.

        :param skill_data: The data for the skill to be created.
        :return: The created Skill instance.
        """
        try:
            # Convert Pydantic models to dictionaries for JSON fields
            cost_data = [cost.model_dump() for cost in skill_data.cost]
            effect_data = [effect.model_dump() for effect in skill_data.effect]
            impact_data = [impact.model_dump() for impact in skill_data.impact]
            
            skill, _ = Skill.objects.get_or_create(
                name=skill_data.name,
                school_id=skill_data.school,
                defaults={
                    'description': skill_data.description,
                    'type': skill_data.type,  # Fixed: was 'kind'
                    'multi_target': skill_data.multi_target,  # Added missing field
                    'cost': cost_data,  # Fixed: convert to dict
                    'impact': impact_data,  # Fixed: convert to dict
                    'effect': effect_data,  # Fixed: was 'effects'
                    'grade': skill_data.grade
                },
            )
            return skill
        except Exception as e:
            # Add proper error handling
            raise ValueError(f"Failed to create skill '{skill_data.name}': {str(e)}") from e
