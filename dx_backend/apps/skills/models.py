from django.db import models

from apps.action.models import PlayerAction
from apps.core.utils.models import BaseModel


class LearnedSkill(BaseModel):
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE, related_name='learned_skills')
    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE)


class LearnedSchool(BaseModel):
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE, related_name='learned_schools')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
