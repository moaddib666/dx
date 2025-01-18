from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import CharacterStats, GenderEnum, GameObject, BehaviorModel
from apps.core.utils.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Rank(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    grade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.TextField()
    experience_needed = models.BigIntegerField()
    next_rank = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ranks'
        ordering = ['experience_needed']


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
    behavior = models.CharField(max_length=20, choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE, db_index=True)

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
