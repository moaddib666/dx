from django.core.management import BaseCommand

from apps.game.services.world.position import JsonDumper


class Command(BaseCommand):
    help = 'Dump positions and connections data to a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str, help='The output JSON file path.')

    def handle(self, *args, **options):
        output_file = options['output_file']

        self.stdout.write(self.style.NOTICE(f"Starting data dump to {output_file}..."))

        try:
            dumper = JsonDumper(output_file_path=output_file)
            dumper.dump()
            self.stdout.write(self.style.SUCCESS(f"Data successfully dumped to {output_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))
