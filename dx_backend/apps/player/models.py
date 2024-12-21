from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import PlayerStat, GenderEnum
from apps.core.utils.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Rank(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    grade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.TextField()
    experience_needed = models.IntegerField()
    next_rank = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ranks'
        ordering = ['experience_needed']


class Player(BaseModel):
    owner = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name='available_players')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(200)])
    gender = models.CharField(max_length=50, choices=GenderEnum.choices)
    bio = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    path = models.ForeignKey("school.ThePath", on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.IntegerField()

    current_health_points = models.IntegerField()
    current_energy_points = models.IntegerField()
    current_active_points = models.IntegerField()

    place_of_birth = models.ForeignKey("world.Location", on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='where_born')
    current_location = models.ForeignKey("world.Location", on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='players')
    dimension = models.ForeignKey("world.Dimension", on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    fight = models.ForeignKey('fight.Fight', on_delete=models.SET_NULL, null=True, blank=True)

    school_slots = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.name


class Stat(BaseModel):
    name = models.CharField(max_length=255, choices=PlayerStat.choices(), default=PlayerStat.PHYSICAL_STRENGTH)
    value = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'player'], name='unique_stat_per_player')
        ]
        ordering = ['player', 'name']

