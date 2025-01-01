from django.db import models

from apps.action.models import CharacterAction
from apps.core.utils.models import BaseModel


class LearnedSkill(BaseModel):
    # character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='learned_skills')
    character = models.UUIDField()
    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)


class LearnedSchool(BaseModel):
    # character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='learned_schools')
    character = models.UUIDField()
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)
