"""
Factory Boy factories for world models.
"""

import factory
from factory.django import DjangoModelFactory

from apps.world.models import (
    Dimension, Planet, Continent, Country, City, Area,
    Location, SubLocation, Position
)


class DimensionFactory(DjangoModelFactory):
    """Factory for Dimension model."""

    class Meta:
        model = Dimension

    id = factory.Sequence(lambda n: n + 1)
    speed = factory.Faker('pyfloat', positive=True, max_value=100)
    energy = factory.Faker('pyfloat', positive=True, max_value=1000)
    shift_cost = factory.Faker('pyint', min_value=0, max_value=100)
    grade = factory.Faker('pyint', min_value=0, max_value=10)
    is_active = True


class PlanetFactory(DjangoModelFactory):
    """Factory for Planet model."""

    class Meta:
        model = Planet

    name = factory.Sequence(lambda n: f"Test Planet {n}")
    description = factory.Faker('text', max_nb_chars=200)
    distance_from_star = factory.Faker('pyfloat', positive=True, max_value=1000)
    diameter = factory.Faker('pyfloat', positive=True, max_value=50000)
    mass = factory.Faker('pyfloat', positive=True, max_value=1000000)
    gravity = factory.Faker('pyfloat', positive=True, max_value=20)
    atmosphere = factory.Faker('word')
    temperature = factory.Faker('pyfloat', min_value=-100, max_value=100)
    number_of_moons = factory.Faker('pyint', min_value=0, max_value=10)
    is_active = True


class ContinentFactory(DjangoModelFactory):
    """Factory for Continent model."""

    class Meta:
        model = Continent

    name = factory.Sequence(lambda n: f"Test Continent {n}")
    description = factory.Faker('text', max_nb_chars=200)
    planet = factory.SubFactory(PlanetFactory)
    area = factory.Faker('pyfloat', positive=True, max_value=1000000)
    population = factory.Faker('pyint', min_value=1000, max_value=10000000)
    number_of_countries = factory.Faker('pyint', min_value=1, max_value=50)
    is_active = True


class CountryFactory(DjangoModelFactory):
    """Factory for Country model."""

    class Meta:
        model = Country

    name = factory.Sequence(lambda n: f"Test Country {n}")
    description = factory.Faker('text', max_nb_chars=200)
    continent = factory.SubFactory(ContinentFactory)
    area = factory.Faker('pyfloat', positive=True, max_value=100000)
    is_active = True


class CityFactory(DjangoModelFactory):
    """Factory for City model."""

    class Meta:
        model = City

    name = factory.Sequence(lambda n: f"Test City {n}")
    description = factory.Faker('text', max_nb_chars=200)
    country = factory.SubFactory(CountryFactory)
    is_active = True


class AreaFactory(DjangoModelFactory):
    """Factory for Area model."""

    class Meta:
        model = Area

    name = factory.Sequence(lambda n: f"Test Area {n}")
    description = factory.Faker('text', max_nb_chars=200)
    city = factory.SubFactory(CityFactory)
    area = factory.Faker('pyfloat', positive=True, max_value=10000)
    is_active = True


class LocationFactory(DjangoModelFactory):
    """Factory for Location model."""

    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f"Test Location {n}")
    description = factory.Faker('text', max_nb_chars=200)
    area = factory.SubFactory(AreaFactory)
    is_active = True
    is_public = True


class SubLocationFactory(DjangoModelFactory):
    """Factory for SubLocation model."""

    class Meta:
        model = SubLocation

    name = factory.Sequence(lambda n: f"Test SubLocation {n}")
    description = factory.Faker('text', max_nb_chars=200)
    location = factory.SubFactory(LocationFactory)
    is_active = True


class PositionFactory(DjangoModelFactory):
    """Factory for Position model."""

    class Meta:
        model = Position

    grid_x = factory.Sequence(lambda n: n)
    grid_y = factory.Sequence(lambda n: n // 100)
    grid_z = factory.Sequence(lambda n: n % 100)
    sub_location = factory.SubFactory(SubLocationFactory)
    labels = factory.List(['test', 'factory'])
    is_safe = True
