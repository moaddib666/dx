from apps.core.models import CharacterGenericData, CharacterTemplateValidator, CharacterBio, CharacterStatHolder, CharacterTemplate, \
    GenderEnum, CharacterStats


class CharacterTemplateService:
    def __init__(self, rank: int = 0):
        self.rank = rank

    @staticmethod
    def get_stats_template() -> list[CharacterStatHolder]:
        return [
            CharacterStatHolder(name=stat, value=0) for stat in CharacterStats
        ]

    def create_template(self) -> CharacterTemplate:
        """
        Creates a customizable character template with empty slots for dynamic input
        and predefined placeholders for essential fields like background and appearance.
        """
        data = CharacterGenericData(
            name="Unnamed Character",
            tags=[],
            bio=CharacterBio(
                age=0,  # Placeholder for user input
                gender=GenderEnum.OTHER,  # Placeholder for user input
                appearance=(
                    "Placeholder for appearance. Suggestions: 'Tall with an athletic build, "
                    "sharp features, piercing blue eyes.'"
                ),
                background=(
                    "Placeholder for background. Suggestions: 'Born in a small village and trained in combat "
                    "by a retired warrior. Now seeking adventure to uncover the mysteries of the Flow.'"
                ),
            ),
            rank=self.rank,
            path=None,
            stats=self.get_stats_template(),
            modificators=[],
            currencyTokens=[],
            items=[],
            schools=[],
            spells=[],
        )
        validation = self.get_validators()
        return CharacterTemplate(data=data, validation=validation)

    def get_validators(self) -> CharacterTemplateValidator:
        # TODO: add scaling by level
        return CharacterTemplateValidator(
            max_rank_grade=self.rank,
            max_stats_points_count=len(self.get_stats_template()) * 10,
            max_modificators_count=2,
            max_items_count=1,
            max_spells_count=1,
            max_schools_count=1,
        )
