from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import CharacterStats, BehaviorModel
from apps.core.utils.models import BaseModel
from apps.character.models.common import Organization, Rank


class NonPlayerCharacterTemplate(BaseModel):
    """
    Template for non-player characters (NPCs).
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    path = models.ForeignKey("school.ThePath", on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    behavior = models.CharField(max_length=20, choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE)
    dimension = models.ForeignKey("world.Dimension", on_delete=models.SET_NULL, null=True, blank=True, default=1)
    campaign = models.ForeignKey('campaign.Campaign', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class NonPlayerCharacterStatsTemplate(BaseModel):
    """
    Template for NPC stats.
    Example of id:
        - magic-attacker-base
        - physical-attacker-base
        - balanced-base
    """
    id = models.CharField(max_length=36, primary_key=True)


class NonPlayerCharacterStatTemplate(BaseModel):
    """
    Template for NPC stats.
    """
    template = models.ForeignKey(NonPlayerCharacterStatsTemplate, on_delete=models.CASCADE, related_name='stats')
    stat = models.CharField(max_length=255, choices=CharacterStats.choices(), default=CharacterStats.PHYSICAL_STRENGTH)
    value = models.IntegerField(default=0)


class NonPlayerCharacterStatsModifierTemplate(BaseModel):
    """
    Template for NPC stats modifiers.
    Example of id:
        - magic-attacker-modifier
        - physical-attacker-modifier
        - balanced-modifier
    """
    id = models.CharField(max_length=36, primary_key=True)


class NonPlayerCharacterStatModifierTemplate(BaseModel):
    """
    Template for NPC stats modifiers.
    """
    template = models.ForeignKey(NonPlayerCharacterStatsModifierTemplate, on_delete=models.CASCADE,
                                 related_name='modifiers')
    stat = models.CharField(max_length=255, choices=CharacterStats.choices(), default=CharacterStats.PHYSICAL_STRENGTH)
    value = models.IntegerField(default=0)


class NonPlayerCharacterBiographyTemplate(BaseModel):
    """
    Template for NPC biography.
    """
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(900)])


class NonPlayerCharacterLearnableSchoolTemplate(BaseModel):
    """
    Template for NPC learnable schools.
    """
    school = models.ForeignKey("school.School", on_delete=models.CASCADE, related_name='npc_learnable_schools')
    template = models.ForeignKey(NonPlayerCharacterStatsTemplate, on_delete=models.CASCADE,
                                 related_name='learnable_schools')

    class Meta:
        unique_together = ('school', 'template')


class NonPlayerCharacterLearnedSkillTemplate(BaseModel):
    """
    Template for NPC learned skills.
    """
    skill = models.ForeignKey("skills.Skill", on_delete=models.CASCADE, related_name='npc_learned_skills')
    template = models.ForeignKey(NonPlayerCharacterTemplate, on_delete=models.CASCADE, related_name='learned_skills')

    class Meta:
        unique_together = ('skill', 'template')