import json
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.school.models import School, Skill, ThePath


class Command(BaseCommand):
    help = 'Load Fire Arts School data from JSON file'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        with open('apps/school/fixtures/schools/FireArtsSchool.json', 'r') as file:
            data = json.load(file)

        # Ensure the path exists or create it
        path_name = data['path']
        path, created = ThePath.objects.get_or_create(name=path_name, defaults={'description': 'Description for Path of JSon'})

        # Create or update the school
        school, created = School.objects.get_or_create(name=data['name'], defaults={'description': 'Description for FireArtsSchool'})
        school.path.add(path)
        school.save()

        # Create or update skills
        for skill_data in data['skills']:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={
                    'grade': skill_data['grade'],
                    'description': skill_data['description'],
                    'multi_target': skill_data['multi_target'],
                    'impact': skill_data['impact'],
                    'cost': skill_data['cost'],
                    'effect': skill_data['effect'],
                }
            )

            # Update skill if already exists
            if not created:
                skill.grade = skill_data['grade']
                skill.description = skill_data['description']
                skill.multi_target = skill_data['multi_target']
                skill.impact = skill_data['impact']
                skill.cost = skill_data['cost']
                skill.effect = skill_data['effect']
                skill.save()

            # Associate skill with the school
            school.skills.add(skill)

        self.stdout.write(self.style.SUCCESS('Successfully loaded Fire Arts School data'))
