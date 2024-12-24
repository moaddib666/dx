from django.core.management.base import BaseCommand, CommandError
from apps.game.services.character.core import CharacterService
from apps.game.services.character.leveling import LevelingService
from apps.character.models import Character


class Command(BaseCommand):
    help = 'Add experience to a character'

    def add_arguments(self, parser):
        parser.add_argument('character_id', type=str, help='The ID of the character to add experience to')
        parser.add_argument('experience', type=int, help='The amount of experience to add')

    def handle(self, *args, **kwargs):
        character_id = kwargs['character_id']
        experience = kwargs['experience']

        try:
            character = Character.objects.get(pk=character_id)
        except Character.DoesNotExist as e:
            raise CommandError('Character with ID "%s" does not exist' % character_id) from e

        character_service = CharacterService(character)
        leveling_service = LevelingService(character)
        try:
            leveling_service.add_experience(experience)
        except Exception as e:
            raise CommandError('Failed to add experience to character "%s": %s' % (character_id, e)) from e
        self.stdout.write(
            self.style.SUCCESS('Successfully added %s experience to character "%s"' % (experience, character_id)))
