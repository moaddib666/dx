from apps.school.models import School, Skill


class SchoolLoaderService:
    def load_skills(self, data):
        """
        Load or update the school and its associated skills from the YAML data.
        """
        for skill_data in data:
            # Extract school ID and data from the skill entry
            school_id = skill_data['fields']['school']
            school_name = self._get_school_name_by_id(school_id)
            if not school_name:
                raise ValueError(f"School with ID {school_id} not found")

            # Create or update skills for the school
            self._load_skill(skill_data)

    def _get_school_name_by_id(self, school_id):
        """
        Fetch the school name by its ID.
        """
        try:
            school = School.objects.get(pk=school_id)
            return school.name
        except School.DoesNotExist:
            return None

    def _load_skill(self, skill_data):
        """
        Create or update a skill based on the provided YAML data.
        """
        fields = skill_data['fields']
        skill_name = fields['name']

        # Try to fetch the skill by name; otherwise, create a new one
        skill, created = Skill.objects.update_or_create(
            name=skill_name,
            defaults={
                'grade': fields['grade'],
                'description': fields['description'],
                'multi_target': fields['multi_target'],
                'school_id': fields['school'],
                'type': fields['type'],
                'impact': fields['impact'],
                'cost': fields['cost'],
                'effect': fields['effect'],
                # 'icon': fields['icon']
                'icon': '',
            }
        )

        if created:
            print(f"Created new skill: {skill_name}")
        else:
            print(f"Updated existing skill: {skill_name}")
