from enum import StrEnum


class CharacterStatPresenter:
    """
    Service to present character stats with a name and description based on stat values.
    """

    def __init__(self, stats: type[StrEnum]):
        self.stats = stats

    STAT_DESCRIPTIONS = {
        "Physical Strength": "Influences health and physical damage.",
        "Mental Strength": "Influences energy and mental resilience.",
        "Luck": "Adds a modifier to various outcomes.",
        "Speed": "Influences action points and turn order.",
        "Concentration": "Ability to maintain spell casting under pressure.",
        "Flow Manipulation": "Skill in shaping and controlling Flow energy.",
        "Flow Connection": "Depth of bond with the Flow, affecting spell efficiency.",
        "Knowledge": "Understanding of magical theory and applications.",
        "Flow Resonance": "Ability to align with the Flow, enhancing spell potency.",
        "Kharma": "Balance of good and bad deeds, affecting luck and fate.",
        "Charisma": "Ability to influence others and maintain relationships.",
    }

    def present_stat(self, stat_value: str) -> dict:
        """
        Accepts a character stat value and returns a dictionary representing a CharacterStatItem.

        Args:
            stat_value (str): The value of the character stat (e.g., "Physical Strength").

        Returns:
            dict: A CharacterStatItem containing 'Name' and 'Description'.
        """
        if stat_value not in self.STAT_DESCRIPTIONS:
            return {
                "name": stat_value,
                "description": "No description available.",
            }

        return {
            "name": stat_value,  # Directly use the provided value as the name
            "description": self.STAT_DESCRIPTIONS[stat_value],
        }

    def prest_as_list(self) -> list:
        """
        Accepts a list of character stats and returns a list of dictionaries representing CharacterStatItems.

        Args:
            stats (list): A list of character stats.

        Returns:
            list: A list of CharacterStatItems containing 'Name' and 'Description'.
        """
        return [self.present_stat(stat) for stat in self.stats]

