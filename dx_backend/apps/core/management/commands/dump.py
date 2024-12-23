from django.apps import apps
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Dump model data in LLM format with field inclusion/exclusion.'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='App.ModelName')
        parser.add_argument('-i', '--include', type=str, help='Comma-separated list of fields to include')
        parser.add_argument('-e', '--exclude', type=str, help='Comma-separated list of fields to exclude')

    def handle(self, *args, **options):
        try:
            app_label, model_name = options['model'].split('.')
            model = apps.get_model(app_label, model_name)
        except (ValueError, LookupError):
            raise CommandError('Invalid model: {}'.format(options['model']))

        queryset = model.objects.all()

        include_fields = options['include'].split(',') if options['include'] else None
        exclude_fields = options['exclude'].split(',') if options['exclude'] else []

        if include_fields:
            fields = include_fields
        else:
            fields = [f.name for f in model._meta.get_fields() if f.name not in exclude_fields]

        data = serializers.serialize('llm', queryset, fields=fields)
        self.stdout.write(data)
