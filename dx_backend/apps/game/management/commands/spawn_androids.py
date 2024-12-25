import logging

from django.core.management.base import BaseCommand

from apps.character.models import Character
from apps.game.services.npc.underground_mercenbaries_spawner import Spawner, UndergroundMercenariesSpawnRule, \
    AndroidsSpawnRule

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Spawn creatures based on the SpawnRule."

    def add_arguments(self, parser):
        parser.add_argument(
            '--character_id', type=str, default="7d3ec1b2-d326-476f-abc5-e035fbb73578",
            help="ID of the creatures to clone for spawning."
        )
        parser.add_argument(
            '--min_count', type=int, default=1,
            help="Minimum number of creatures to spawn at each position."
        )
        parser.add_argument(
            '--max_count', type=int, default=10,
            help="Maximum number of creatures to spawn at each position."
        )

    def handle(self, *args, **options):
        character_id = options['character_id']
        min_count = options['min_count']
        max_count = options['max_count']

        # Fetch the character
        try:
            character = Character.objects.get(id=character_id)
            self.stdout.write(
                self.style.SUCCESS(f"Using character {character.name} (ID: {character.id}) for spawning."))
        except Character.DoesNotExist:
            logger.error(f"Character with ID {character_id} does not exist.")
            self.stderr.write(self.style.ERROR(f"Character with ID {character_id} does not exist."))
            return

        # Initialize the spawner
        try:
            spawner = Spawner(
                character=character,
                min_count=min_count,
                max_count=max_count,
                rules=[
                    AndroidsSpawnRule()
                ]
            )
            logger.info(f"Spawner initialized with character {character.name} (ID: {character.id}).")
        except ValueError as e:
            logger.error(f"Failed to initialize spawner: {e}")
            self.stderr.write(self.style.ERROR(f"Failed to initialize spawner: {e}"))
            return

        # Perform the spawn
        try:
            self.stdout.write("Starting spawn process...")
            spawner.spawn()
            self.stdout.write(self.style.SUCCESS("Spawn process completed successfully."))
        except Exception as e:
            logger.error(f"Error during spawn process: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"Error during spawn process: {e}"))
