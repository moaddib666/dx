from apps.character.models import Character


class BaseStatChangesApplier:
    character_model = Character

    def apply(self):
        characters = self.get_characters()
        characters.update(resetting_base_stats=False)

    def get_characters(self) -> [Character]:
        return self.character_model.objects.filter(resetting_base_stats=True)

