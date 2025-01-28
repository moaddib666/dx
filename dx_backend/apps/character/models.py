from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import CharacterStats, GenderEnum, GameObject, BehaviorModel
from apps.core.utils.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


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


class CharacterBiography(BaseModel):
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(900)])
    gender = models.CharField(max_length=50, choices=GenderEnum.choices, default=GenderEnum.OTHER)
    background = models.TextField(blank=True)
    appearance = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    character = models.OneToOneField('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                     related_name='biography')


class Character(GameObject):
    owner = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name='available_characters')
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.JSONField(default=list)
    path = models.ForeignKey("school.ThePath", on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.IntegerField(default=0)

    current_health_points = models.IntegerField(default=1)
    current_energy_points = models.IntegerField(default=1)
    current_active_points = models.IntegerField(default=1)

    place_of_birth = models.ForeignKey("world.Location", on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='where_born')
    # FIXME: implement migration moved to GameObject
    # dimension = models.ForeignKey("world.Dimension", on_delete=models.SET_NULL, null=True, blank=True, default=1)
    # is_active = models.BooleanField(default=True)

    fight = models.ForeignKey('fight.Fight', on_delete=models.SET_NULL, null=True, blank=True)

    school_slots = models.PositiveIntegerField(default=2)

    #
    npc = models.BooleanField(default=False)
    behavior = models.CharField(max_length=20, choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE,
                                db_index=True)

    last_safe_position = models.ForeignKey('world.Position', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='characters_in_safe')

    resetting_base_stats = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Stat(BaseModel):
    name = models.CharField(max_length=255, choices=CharacterStats.choices(), default=CharacterStats.PHYSICAL_STRENGTH)
    additional_value = models.IntegerField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='stats')

    base_value = models.IntegerField(default=0)
    dice_rolls = models.ManyToManyField('action.DiceRollResult', related_name='base_stat_results')

    @property
    def value(self) -> int:
        return self.base_value + self.additional_value

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'character'], name='unique_stat_per_character')
        ]
        ordering = ['character', 'name']


class StatModifier(BaseModel):
    """
    name: string
    value: int
    """
    name = models.CharField(max_length=255, choices=CharacterStats.choices(), default=CharacterStats.PHYSICAL_STRENGTH)
    value = models.IntegerField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='stats_modifiers')

    applied_by_effect = models.ForeignKey('effects.ActiveEffect', on_delete=models.CASCADE, null=True, blank=True, related_name='applied_stat_modifiers')

    def __str__(self):
        return f"{self.name} - {self.value}"
