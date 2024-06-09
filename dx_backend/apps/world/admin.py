from django.contrib import admin

from .models import Dimension, Planet, Continent, Country, City, Area, Location, SubLocation


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ('id', 'speed', 'energy')
    search_fields = ('id',)
    list_filter = ('speed', 'energy')


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'distance_from_star', 'diameter', 'mass', 'gravity', 'temperature', 'number_of_moons', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'atmosphere')


@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'planet', 'area', 'population', 'number_of_countries', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'planet')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'area', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'continent')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'country')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'area', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'city')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'is_active', 'is_public')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'is_public', 'area')


@admin.register(SubLocation)
class SubLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'location')
