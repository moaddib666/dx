import typing
from copy import deepcopy

from django.db import transaction

from apps.character.models import Character, CharacterBiography


class CharacterCloner:

    def __init__(self, char: Character):
        self.char = char

    def clone(self, count: int, template: str = "{base_name} {index}") -> typing.Iterable[Character]:
        new = set()
        for i in range(count):
            with transaction.atomic():
                new_char = deepcopy(self.char)
                new_char.pk = None
                new_char.name = template.format(index=i, base_name=self.char.name)
                new_char.save()
                CharacterBiography.objects.create(
                    character=new_char,
                    age=self.char.biography.age,
                    appearance=self.char.biography.appearance,
                    background=self.char.biography.background,
                    avatar=self.char.biography.avatar
                )
                self.clone_stats(self.char, new_char)
                new.add(new_char)

        return new

    def clone_stats(self, source: Character, target: Character) -> None:
        for stat in source.stats.all():
            target.stats.create(name=stat.name, value=stat.value)
