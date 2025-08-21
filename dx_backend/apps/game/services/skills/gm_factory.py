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
        skill, _ = Skill.objects.get_or_create(
            name=skill_data.name,
            school_id=skill_data.school_id,
            defaults={
                'description': skill_data.description,
                'kind': skill_data.kind,
                'cost': skill_data.cost,
                'impact': skill_data.impact,
                'effects': skill_data.effects,
                'grade': skill_data.grade
            },
        )
        return skill
