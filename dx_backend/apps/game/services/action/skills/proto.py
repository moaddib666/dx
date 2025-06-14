import typing as t

if t.TYPE_CHECKING:
    from apps.action.models import CharacterAction
    from apps.school.models import Skill


class SpecialSkillActionPrototype:
    """
    Represents a special skill action in the game.
    This class is used to define the properties and behavior of a special skill action.
    """

    def __init__(self, skill: "Skill"):
        """
        Initializes a SpecialSkillAction instance.
        """
        self.skill = skill

    def perform(self, action: "CharacterAction") -> [t.Any]:
        """
        Executes the skill action on the target. Returns a list of calculated impacts.
        """
        # Implement the logic to perform the skill action on the target
        pass


class SpecialSkillActionFactoryPrototype:
    """
    Factory class to create special skill actions.
    """

    @staticmethod
    def create(skill: "Skill") -> "SpecialSkillAction":
        """
        Creates a SpecialSkillAction instance based on the provided skill.
        """
