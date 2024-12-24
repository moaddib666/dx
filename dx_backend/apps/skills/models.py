from django.db import models

from apps.action.models import CharacterAction
from apps.core.utils.models import BaseModel


class LearnedSkill(BaseModel):
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='learned_skills')
    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE)


class LearnedSchool(BaseModel):
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='learned_schools')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
