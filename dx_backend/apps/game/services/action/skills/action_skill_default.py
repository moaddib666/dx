from .proto import SpecialSkillActionPrototype


class NoActionSkill(SpecialSkillActionPrototype):
    """
    Represents a no-action skill in the game.
    This class is used when no specific action is required.
    """

    def perform(self, action) -> list:
        """
        Executes the no-action skill. Returns an empty list as no impacts are calculated.
        """
        return []
