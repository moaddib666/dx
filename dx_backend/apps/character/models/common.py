from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import BehaviorModel
from apps.core.utils.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    campaign = models.ForeignKey('game.Campaign', on_delete=models.CASCADE, related_name='organizations')
    behavior = models.CharField(choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE, max_length=20)

    def __str__(self):
        return self.name


class OrganizationRelation(models.Model):
    """
    Represents a relationship between two organizations.
    """
    type = models.CharField(max_length=20, choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE)
    organization_from = models.ForeignKey(Organization, related_name='relations_from', on_delete=models.CASCADE)
    organization_to = models.ForeignKey(Organization, related_name='relations_to', on_delete=models.CASCADE)
    immutable = models.BooleanField(default=False, help_text="If True, the relation cannot be changed or deleted.")

    def __str__(self):
        return f"{self.organization_from} {self.type} {self.organization_to}"

    class Meta:
        verbose_name = "Organization Relation"
        verbose_name_plural = "Organization Relations"


class CharacterRelation(models.Model):
    """
    Represents a relation between two characters.
    """
    type = models.CharField(max_length=20, choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE)
    character_from = models.ForeignKey("character.Character", related_name='relations_from', on_delete=models.CASCADE)
    character_to = models.ForeignKey("character.Character", related_name='relations_to', on_delete=models.CASCADE)
    immutable = models.BooleanField(default=False, help_text="If True, the relation cannot be changed or deleted.")

    def __str__(self):
        return f"{self.character_from} {self.type} {self.character_to}"

    class Meta:
        verbose_name = "Character Relation"
        verbose_name_plural = "Character Relations"


class RankManager(models.Manager):

    def get_skill_points(self, current_grade: int, new_grade: int):
        """
        Get the skill points needed to go from one rank to another.
        0 - max rank
        10 - min rank
        """
        gained_skill_points = Rank.objects.filter(
            grade__lt=current_grade,
            grade__gte=new_grade
        ).aggregate(
            models.Sum('additional_stat_points'))['additional_stat_points__sum']

        return gained_skill_points or 0


class Rank(BaseModel):
    """
    name: string
    grade: int
    description: string
    experience_needed: int
    """
    objects = RankManager()
    name = models.CharField(max_length=255, unique=True)
    grade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    grade_rank = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    additional_stat_points = models.PositiveIntegerField(default=0)
    description = models.TextField()
    experience_needed = models.BigIntegerField(default=0)
    next_rank = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Grade {self.grade}, Rank {self.grade_rank})"

    @property
    def is_max_rank(self):
        """Check if the rank is the highest in its grade."""
        return self.next_rank is None

    class Meta:
        verbose_name = "Rank"
        verbose_name_plural = "Ranks"
        ordering = ["grade", "grade_rank"]
        constraints = [
            models.UniqueConstraint(fields=["grade", "grade_rank"], name="unique_grade_and_rank")
        ]

    def get_full_rank(self):
        """Returns a string representation of the full rank (grade and sub-rank)."""
        return f"Grade {self.grade}, Rank {self.grade_rank}"

    def get_next_rank_name(self):
        """Returns the name of the next rank, if it exists."""
        return self.next_rank.name if self.next_rank else "None"
