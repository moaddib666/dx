from django.core.validators import MaxValueValidator, MinValueValidator

from apps.core.utils.models import BaseModel
from django.db import models


class Dimension(BaseModel):
    id = models.IntegerField(primary_key=True)

    speed = models.FloatField()
    energy = models.FloatField()
    shift_cost = models.IntegerField(default=0)

    grade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    is_active = models.BooleanField(default=True)


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

    border_with = models.ManyToManyField('self',)

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

    border_with = models.ManyToManyField('self')

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='countries/', null=True, blank=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    area = models.FloatField()
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self',)

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='cities/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self', )

    def __str__(self):
        return self.name


class Area(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='areas/', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.FloatField()
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self',)

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='locations/', null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self')

    def __str__(self):
        return self.name


class SubLocation(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='sub_locations/', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    border_with = models.ManyToManyField('self')

    def __str__(self):
        return self.name