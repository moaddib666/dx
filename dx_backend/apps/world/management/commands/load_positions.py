import os

from django.core.management.base import BaseCommand, CommandError

from apps.game.services.world.position import PositionLoader
from apps.world.models import SubLocation


class Command(BaseCommand):
    help = "Loads positions and connections from a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the JSON file containing positions and connections.'
        )
        parser.add_argument(
            '--sub_location-id',
            type=str,
            default='867126d4-c41f-4342-848f-bdd12cd41c3a',
            help='The id of the default sub-location to associate with the positions.'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        sub_location_id = kwargs['sub_location_id']

        # Check if the file exists
        if not os.path.exists(file_path):
            raise CommandError(f"The file {file_path} does not exist.")

        # Get the SubLocation object
        try:
            sub_location = SubLocation.objects.get(pk=sub_location_id)
        except SubLocation.DoesNotExist:
            raise CommandError(f"SubLocation with name '{sub_location_id}' does not exist.")

        # Load positions
        self.stdout.write(f"Loading positions from {file_path}...")
        try:
            loader = PositionLoader(file_path, sub_location)
            loader.load()
            self.stdout.write(self.style.SUCCESS("Positions and connections loaded successfully."))
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
