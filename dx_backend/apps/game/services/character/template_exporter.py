import uuid
from typing import List, Optional

from django.shortcuts import get_object_or_404

from apps.character.models.npc import CharacterTemplate as DjangoCharacterTemplate
from apps.core.models import (
    CharacterGenericData, CharacterTemplateValidator, CharacterBio,
    CharacterStatHolder, CharacterTemplate, GenderEnum, CharacterStats
)


class CharacterTemplateExporter:
    """
    Exporter for character templates that handles schema directly.
    This class generates a template schema based on the actual models
    rather than using hardcoded values.
    """

    def __init__(self, template: "CharacterTemplate", rank: int = 0):
        self.rank = rank
        self.template = template

    def export_template(self) -> CharacterTemplate:
        """
        Exports a character template with proper schema.
        Returns a CharacterTemplate object with data and validation sections.

        If template_id is provided, exports the existing template.
        Otherwise, creates a new template with default values.
        """
        data = self._create_template_data()
        validation = self._create_template_validation()
        return CharacterTemplate(data=data, validation=validation)

    def _create_template_data(self) -> CharacterGenericData:
        """
        Creates the data section of the character template.

        If a template is available, uses its data to populate the CharacterGenericData object.
        Otherwise, creates a default template.
        """
        if self.template:
            # Use the template's data to populate the CharacterGenericData object
            bio_data = self._get_bio_data()

            return CharacterGenericData(
                name=self.template.name,
                tags=self.template.tags or [],
                bio=bio_data,
                rank=self.template.rank.grade if self.template.rank else self.rank,
                path=self.template.path.id if self.template.path else None,
                stats=self._get_stats_template(),
                modificators=[mod.id for mod in self.template.modifier_templates.all()] if hasattr(self.template,
                                                                                                   'modifier_templates') else [],
                items=[equip.item.id for equip in self.template.equipment_templates.all()] if hasattr(self.template,
                                                                                                      'equipment_templates') else [],
                schools=[school.school.id for school in self.template.school_templates.all()] if hasattr(self.template,
                                                                                                         'school_templates') else [],
                spells=[skill.skill.id for skill in self.template.skill_templates.all()] if hasattr(self.template,
                                                                                                    'skill_templates') else [],
            )
        else:
            # Create a default template
            return CharacterGenericData(
                name="Unnamed Character",
                tags=[],
                bio=CharacterBio(
                    age=0,
                    gender=GenderEnum.OTHER,
                    appearance="Placeholder for appearance...",
                    background="Placeholder for background..."
                ),
                rank=self.rank,
                path=None,
                stats=self._get_stats_template(),
                modificators=[],
                items=[],
                schools=[],
                spells=[],
            )

    def _get_bio_data(self) -> CharacterBio:
        """
        Extracts the biography data from the template.

        If the template has a biography_template, uses its data directly from the database.
        Otherwise, returns default bio data.
        """
        if self.template and self.template.biography_template:
            bio_template = self.template.biography_template

            # Use the template's biography data directly from the database
            return CharacterBio(
                age=bio_template.age_min,  # Use age_min as a fixed value instead of generating
                gender=bio_template.gender,  # Use the stored gender instead of generating
                appearance=bio_template.appearance or "Placeholder for appearance...",
                background=bio_template.background or "Placeholder for background...",
                avatar=str(bio_template.avatar),
            )
        else:
            # Return default bio data
            return CharacterBio(
                age=0,
                gender=GenderEnum.OTHER,
                appearance="Placeholder for appearance...",
                background="Placeholder for background..."
            )

    def _get_stats_template(self) -> List[CharacterStatHolder]:
        """
        Creates a list of CharacterStatHolder objects for all character stats.

        If the template has a stats_template, uses its data.
        Otherwise, returns default stats.
        """
        if self.template and self.template.stats_template:
            stats_template = self.template.stats_template

            # Use the template's stats data
            return [
                CharacterStatHolder(name=stat, value=stats_template.get_stat_value(stat))
                for stat in CharacterStats
            ]
        else:
            # Return default stats
            return [
                CharacterStatHolder(name=stat, value=0) for stat in CharacterStats
            ]

    def _create_template_validation(self) -> CharacterTemplateValidator:
        """
        Creates the validation section of the character template.

        If a template is available, uses its rank for max_rank_grade.
        Otherwise, uses the provided rank.
        """
        rank = self.rank
        if self.template and self.template.rank:
            rank = self.template.rank.grade

        return CharacterTemplateValidator(
            max_stats_points_count=100,
            max_modificators_count=2,
            max_items_count=1,
            max_spells_count=1,
            max_rank_grade=rank,
            max_schools_count=1,
        )
