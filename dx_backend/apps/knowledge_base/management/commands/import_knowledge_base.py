"""
Django management command for importing knowledge base documents from a folder structure.

Usage:
    python manage.py import_knowledge_base /path/to/folder
    python manage.py import_knowledge_base /path/to/folder --dry-run
    python manage.py import_knowledge_base /path/to/folder --verbosity 2
"""

from django.core.management.base import BaseCommand, CommandError
from apps.knowledge_base.services import KnowledgeBaseImporter


class Command(BaseCommand):
    help = (
        'Import knowledge base documents from a folder structure.\n\n'
        'Expected folder structure:\n'
        '  base_folder/\n'
        '    {category}/\n'
        '      {document_name}/\n'
        '        document.json  (required)\n'
        '        image.png      (optional)\n\n'
        'Valid categories: events, rules, lore, stories, guides, items, characters, '
        'locations, places, factions, creatures, skills, spells, abilities, other'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'folder',
            type=str,
            help='Path to the base folder containing category folders'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate files without actually importing them'
        )

    def handle(self, *args, **options):
        folder = options['folder']
        dry_run = options['dry_run']
        verbosity = options['verbosity']

        # Configure logging based on verbosity
        if verbosity >= 2:
            import logging
            logging.basicConfig(level=logging.DEBUG)
        elif verbosity >= 1:
            import logging
            logging.basicConfig(level=logging.INFO)

        # Display header
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('Knowledge Base Importer'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(f'Folder: {folder}')
        self.stdout.write(f'Mode: {"DRY RUN (validation only)" if dry_run else "IMPORT"}')
        self.stdout.write('')

        try:
            # Initialize the importer
            importer = KnowledgeBaseImporter(folder, dry_run=dry_run)
            
            # Run the import
            result = importer.import_all()
            
            # Display results
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 80))
            self.stdout.write(self.style.SUCCESS('Import Results'))
            self.stdout.write(self.style.SUCCESS('=' * 80))
            
            # Success count
            if result.success_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Successfully imported: {result.success_count} documents')
                )
                if verbosity >= 2:
                    for doc_title in result.imported_documents:
                        self.stdout.write(f'  - {doc_title}')
            
            # Error count
            if result.error_count > 0:
                self.stdout.write(
                    self.style.ERROR(f'✗ Errors: {result.error_count}')
                )
                for error in result.errors:
                    self.stdout.write(
                        self.style.ERROR(f'  - {error["path"]}: {error["error"]}')
                    )
            
            # Skipped count
            if result.skipped_count > 0:
                self.stdout.write(
                    self.style.WARNING(f'⊘ Skipped: {result.skipped_count} folders')
                )
            
            self.stdout.write(self.style.SUCCESS('=' * 80))
            
            # Exit with error if there were any errors
            if result.error_count > 0:
                raise CommandError(f'Import completed with {result.error_count} errors')
            
            # Success message
            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Validation completed successfully! '
                        f'{result.success_count} documents are ready to import.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Import completed successfully! '
                        f'{result.success_count} documents imported.'
                    )
                )
        
        except ValueError as e:
            raise CommandError(f'Invalid folder: {e}')
        except Exception as e:
            raise CommandError(f'Import failed: {e}')
