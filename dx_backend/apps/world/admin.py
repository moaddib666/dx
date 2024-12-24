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


from django.contrib import admin
from django.forms import ModelForm, ValidationError
from .models import Position, PositionConnection


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        grid_x = cleaned_data.get("grid_x")
        grid_y = cleaned_data.get("grid_y")
        grid_z = cleaned_data.get("grid_z")
        sub_location = cleaned_data.get("sub_location")

        if Position.objects.filter(
            grid_x=grid_x,
            grid_y=grid_y,
            grid_z=grid_z,
            sub_location=sub_location
        ).exists():
            raise ValidationError("A position with these coordinates and sub-location already exists.")
        return cleaned_data


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    form = PositionForm
    list_display = ('id', 'grid_x', 'grid_y', 'grid_z', 'sub_location', 'label_summary')
    list_filter = ('sub_location',)
    search_fields = ('id', 'grid_x', 'grid_y', 'grid_z', 'sub_location__name')
    ordering = ('sub_location', 'grid_x', 'grid_y', 'grid_z')

    def label_summary(self, obj):
        return ", ".join(obj.labels) if obj.labels else "No Labels"
    label_summary.short_description = 'Labels'


class PositionConnectionForm(ModelForm):
    class Meta:
        model = PositionConnection
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        position_from = cleaned_data.get("position_from")
        position_to = cleaned_data.get("position_to")

        if position_from == position_to:
            raise ValidationError("Position from and position to cannot be the same.")

        return cleaned_data


@admin.register(PositionConnection)
class PositionConnectionAdmin(admin.ModelAdmin):
    form = PositionConnectionForm
    list_display = ('id', 'position_from', 'position_to', 'is_active', 'is_public')
    list_filter = ('is_active', 'is_public')
    search_fields = ('position_from__id', 'position_to__id')
    ordering = ('position_from', 'position_to')

    def get_queryset(self, request):
        # Optimize queryset to reduce database hits
        return super().get_queryset(request).select_related('position_from', 'position_to')
