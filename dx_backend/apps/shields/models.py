from django.db import models

from apps.core.models import ImpactViolationType
from apps.core.utils.models import BaseModel


class ShieldLevelResolver:
    """
    Resolves shield properties (level and efficiency) dynamically based on health.
    """
    LEVELS = [
        (15, 1),
        (40, 2),
        (70, 3),
        (100, 4),
        (150, 5),
        (200, 6),
        (300, 7),
        (400, 8),
        (500, 9),
    ]

    EFFICIENCY_BY_LEVEL = {
        1: 0.5,  # 50%
        2: 0.75,
        3: 0.9,
        4: 1.0,
        5: 1.0,
        6: 1.0,
        7: 1.0,
        8: 1.0,
        9: 1.0,
    }

    def __init__(self, active_shield: 'ActiveShield'):
        self.active_shield = active_shield

    def resolve_shield_level(self) -> int:
        """
        Determine the shield level based on current health.
        """
        for health_threshold, level in self.LEVELS:
            if self.active_shield.health <= health_threshold:
                return level
        return len(self.LEVELS)  # Max level if health exceeds all thresholds

    def resolve_shield_efficiency(self) -> float:
        """
        Determine the efficiency of the shield based on its level.
        """
        level = self.resolve_shield_level()
        return self.EFFICIENCY_BY_LEVEL.get(level, 1.0)  # Default to 100% if level not found


class Shield(BaseModel):
    id = models.CharField(max_length=255, choices=ImpactViolationType.choices, default=ImpactViolationType.NONE,
                          primary_key=True)
    icon = models.ImageField(upload_to='icons/shields/', null=True, blank=True)
    base_health = models.PositiveIntegerField(default=100)
    base_efficiency = models.FloatField(default=1)

    def __str__(self):
        return self.id


class ActiveShieldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cycles_left__gt=0)

    def unsafe_all(self):
        return super().get_queryset()

    def inactive(self):
        return self.unsafe_all().filter(cycles_left__lte=0)


class ActiveShield(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_resolver = ShieldLevelResolver(self)

    objects = ActiveShieldManager()
    shield = models.ForeignKey(Shield, on_delete=models.CASCADE)
    target = models.ForeignKey(
        'character.Character', to_field='gameobject_ptr',
        on_delete=models.CASCADE,
        related_name='shields'
    )
    cycles_left = models.PositiveIntegerField(default=1)
    health = models.PositiveIntegerField(default=1)

    # level = models.PositiveIntegerField(default=1)
    @property
    def level(self) -> int:
        return self.level_resolver.resolve_shield_level()

    @property
    def efficiency(self) -> float:
        return self.level_resolver.resolve_shield_efficiency()

    def __str__(self):
        return f'{self.shield} - {self.target.name}'

    class Meta:
        unique_together = ('shield', 'target')
