from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model

from apps.core.utils.models import BaseModel, TagsDescriptor


class Dimension(BaseModel):
    id = models.IntegerField(primary_key=True)
    speed = models.FloatField()
    energy = models.FloatField()
    shift_cost = models.IntegerField(default=0)

    grade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dimension {self.id}"


class Planet(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='planets/', null=True, blank=True)
    distance_from_star = models.FloatField()
    diameter = models.FloatField()
    mass = models.FloatField()
    gravity = models.FloatField()
    atmosphere = models.CharField(max_length=255)
    temperature = models.FloatField()
    number_of_moons = models.IntegerField()
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class Continent(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='continents/', null=True, blank=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    area = models.FloatField()
    population = models.IntegerField()
    number_of_countries = models.IntegerField()
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='countries/', null=True, blank=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    area = models.FloatField()
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='cities/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class Area(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='areas/', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.FloatField()
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='locations/', null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class SubLocation(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='sub_locations/', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Position(Model):
    """
    The position is minimal unit of the world.
     It represents 1 cell in the grid
     In common scenario it could be the room, street part, tunnel, etc.
     On the positions game objects can be placed like characters, items, etc.
     The position can be connected with other positions.
     The position is part of the sub-location example: SubLocation is the building, Position is the room.

    """
    id = models.UUIDField(primary_key=True)
    grid_x = models.BigIntegerField(default=0)
    grid_y = models.BigIntegerField(default=0)
    grid_z = models.BigIntegerField(default=0)
    sub_location = models.ForeignKey(SubLocation, on_delete=models.CASCADE)
    labels = models.JSONField(default=list)
    is_safe = models.BooleanField(default=False)
    image = models.ImageField(upload_to='positions/', null=True, blank=True)

    @property
    def coordinates(self) -> str:
        return f"{self.grid_x}x{self.grid_y}x{self.grid_z}"

    class Meta:
        unique_together = ('grid_x', 'grid_y', 'grid_z')
        indexes = [
            models.Index(fields=['grid_x', 'grid_y', 'grid_z'])
        ]

    def __str__(self):
        return f"{self.sub_location.name} - {self.coordinates}"


class PositionConnection(models.Model):
    position_from = models.ForeignKey(
        'Position', on_delete=models.CASCADE, related_name='position_from'
    )
    position_to = models.ForeignKey(
        'Position', on_delete=models.CASCADE, related_name='position_to'
    )
    # TODO: Plan to create the PositionConnectionOverrides model to be able on campaign, organization, character
    #  level override the connection properties
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def is_vertical(self):
        return self.position_to.grid_z != self.position_from.grid_z

    def is_horizontal(self):
        return self.position_to.grid_z == self.position_from.grid_z

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['position_from', 'position_to'],
                name='unique_position_connection',
                condition=models.Q(position_from__lt=models.F('position_to'))
            ),
            models.UniqueConstraint(
                fields=['position_to', 'position_from'],
                name='unique_position_connection_reversed',
                condition=models.Q(position_to__lt=models.F('position_from'))
            ),
        ]
        indexes = [
            models.Index(fields=['position_from', 'position_to']),
            models.Index(fields=['position_to', 'position_from']),
        ]

    def clean(self):
        # Ensure position_from and position_to are not the same
        if self.position_from == self.position_to:
            raise ValidationError("position_from and position_to cannot be the same.")

    def save(self, *args, **kwargs):
        # Enforce consistent ordering for uniqueness
        if self.position_from.id > self.position_to.id:
            self.position_from, self.position_to = self.position_to, self.position_from
        super().save(*args, **kwargs)


class Map(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.OneToOneField('character.Organization', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MapPosition(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='map_positions')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    labels = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        unique_together = ('map', 'position')
        indexes = [
            models.Index(fields=['map', 'position'])
        ]

    def __str__(self):
        return f"{self.map.name} - {self.position.sub_location.name} - {self.position.coordinates}"
