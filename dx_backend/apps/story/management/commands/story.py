import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.game.services.story import StoryService
from apps.story.models import Story


class Command(BaseCommand):
    help = 'Load and dump stories using the Story service'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='action', help='Available actions')

        # Load command
        load_parser = subparsers.add_parser('load', help='Load a story from JSON file')
        load_parser.add_argument('file', type=str, help='Path to JSON file to load')
        load_parser.add_argument('--validate-only', action='store_true',
                                 help='Only validate the JSON structure without loading')

        # Dump command
        dump_parser = subparsers.add_parser('dump', help='Dump a story to JSON file')
        dump_parser.add_argument('story_id', type=str, help='ID of the story to dump')
        dump_parser.add_argument('file', type=str, help='Path to output JSON file')
        dump_parser.add_argument('--stdout', action='store_true',
                                 help='Output to stdout instead of file')

        # List command
        list_parser = subparsers.add_parser('list', help='List all available stories')
        list_parser.add_argument('--canonical-only', action='store_true',
                                 help='Show only canonical stories')

    def handle(self, *args, **options):
        action = options.get('action')

        if not action:
            self.print_help('manage.py', 'story')
            return

        service = StoryService()

        try:
            if action == 'load':
                self.handle_load(service, options)
            elif action == 'dump':
                self.handle_dump(service, options)
            elif action == 'list':
                self.handle_list(options)
        except Exception as e:
            raise CommandError(f'Error executing {action}: {str(e)}')

    def handle_load(self, service: StoryService, options):
        """Handle story loading from JSON file."""
        file_path = options['file']
        validate_only = options.get('validate_only', False)

        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')

        if validate_only:
            self.stdout.write('Validating JSON structure...')
            is_valid = service.validate_json_structure(file_path)
            if is_valid:
                self.stdout.write(
                    self.style.SUCCESS('✓ JSON structure is valid')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('✗ JSON structure is invalid')
                )
            return

        self.stdout.write(f'Loading story from: {file_path}')

        with transaction.atomic():
            story = service.load_from_file(file_path)

        # Display results
        self.stdout.write(
            self.style.SUCCESS(f'✓ Successfully loaded story: "{story.title}" (ID: {story.id})')
        )

        # Show statistics
        stats = service.get_loader_stats()
        if stats:
            self.stdout.write('\nLoading statistics:')
            for obj_type, count in stats.items():
                if count > 0:
                    self.stdout.write(f'  {obj_type}: {count}')

        # Show custom triggers warning
        custom_count = service.get_custom_triggers_count()
        if custom_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠ Created {custom_count} CUSTOM triggers for unknown types. '
                    'Review and fix these triggers manually.'
                )
            )

    def handle_dump(self, service: StoryService, options):
        """Handle story dumping to JSON file."""
        story_id = options['story_id']
        file_path = options['file']
        to_stdout = options.get('stdout', False)

        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            raise CommandError(f'Story with ID {story_id} not found')

        self.stdout.write(f'Dumping story: "{story.title}" (ID: {story.id})')

        if to_stdout:
            json_output = service.dump_to_json_string(story)
            self.stdout.write('\n' + json_output)
        else:
            service.dump_to_file(story, file_path)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Successfully dumped story to: {file_path}')
            )

        # Show statistics
        stats = service.get_dumper_stats()
        if stats:
            self.stdout.write('\nDumping statistics:')
            for obj_type, count in stats.items():
                if count > 0:
                    self.stdout.write(f'  {obj_type}: {count}')

    def handle_list(self, options):
        """Handle listing available stories."""
        canonical_only = options.get('canonical_only', False)

        queryset = Story.objects.all()
        if canonical_only:
            queryset = queryset.filter(canonical=True)

        stories = queryset.order_by('title')

        if not stories.exists():
            filter_text = ' canonical' if canonical_only else ''
            self.stdout.write(f'No{filter_text} stories found.')
            return

        self.stdout.write(f'Available stories:')
        self.stdout.write('-' * 50)

        for story in stories:
            canonical_mark = ' [CANONICAL]' if story.canonical else ''
            chapters_count = story.chapters.count()

            self.stdout.write(
                f'ID: {str(story.id)} | {story.title}{canonical_mark}'
            )
            self.stdout.write(
                f'      Chapters: {chapters_count} | Tags: {", ".join(story.tags) if story.tags else "None"}')
            self.stdout.write(f'      {story.description[:80]}{"..." if len(story.description) > 80 else ""}')
            self.stdout.write('')
