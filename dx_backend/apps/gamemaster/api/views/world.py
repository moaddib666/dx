from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.world.api.serializers.openapi import (
    DimensionSerializer, CitySerializer, AreaSerializer, 
    LocationSerializer, PositionSerializer, MapSerializer
)
from apps.gamemaster.api.serializers.world import (
    PlanetSerializer, ContinentSerializer, CountrySerializer
)
from apps.world.models import (
    Dimension, Planet, Continent, Country, 
    City, Area, Location, Position, Map
)


class GameMasterDimensionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage dimensions.
    This viewset provides full CRUD operations for dimensions.
    """
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterPlanetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage planets.
    This viewset provides full CRUD operations for planets.
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterContinentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage continents.
    This viewset provides full CRUD operations for continents.
    """
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterCountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage countries.
    This viewset provides full CRUD operations for countries.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterCityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage cities.
    This viewset provides full CRUD operations for cities.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterAreaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage areas.
    This viewset provides full CRUD operations for areas.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterLocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage locations.
    This viewset provides full CRUD operations for locations.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterPositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage positions.
    This viewset provides full CRUD operations for positions.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterMapViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage maps.
    This viewset provides full CRUD operations for maps.
    """
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
