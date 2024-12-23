import yaml
from django.core.management.base import BaseCommand, CommandError

from apps.game.services.skills.loader import SchoolLoaderService


class Command(BaseCommand):
    help = "Load or update skill tree data from a YAML file"

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help="Path to the YAML file containing the skill tree data"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
        except Exception as e:
            raise CommandError(f"Failed to load YAML file: {e}")

        service = SchoolLoaderService()
        try:
            service.load_skills(data)
            self.stdout.write(self.style.SUCCESS("Skill tree data loaded successfully"))
        except Exception as e:
            raise CommandError(f"Error while loading skills: {e}")
