from django.db import models

from apps.action.models import CharacterAction
from apps.core.utils.models import BaseModel, TagsDescriptor


class LearnedSkill(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                  related_name='learned_skills')
    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.skill.name} - {"Base" if self.is_base else "Learned"}'


class LearnedSchool(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                  related_name='learned_schools')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)
