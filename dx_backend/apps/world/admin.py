import logging

from django.contrib import admin
from django.forms import ModelForm, ValidationError

from apps.core.admin import CampaignModelAdmin
from .models import (
    Dimension, Planet, Continent, Country, City, Area, Location, PositionConnection, MapPosition, Map
)

logger = logging.getLogger(__name__)

from django import forms
from django.shortcuts import render, redirect
from django.urls import path, reverse
from .models import Position, SubLocation


class BulkChangeSubLocationForm(forms.Form):
    """
    Form for selecting a new sub-location for bulk action.
    """
    sub_location = forms.ModelChoiceField(
        queryset=SubLocation.objects.all(),
        label="Select Sub-Location",
        required=True
    )


# Dimension Admin
@admin.register(Dimension)
class DimensionAdmin(CampaignModelAdmin):
    list_display = ('id', 'speed', 'energy', 'campaign')
    search_fields = ('id',)
    list_filter = ('speed', 'energy', 'campaign')


# Planet Admin
@admin.register(Planet)
class PlanetAdmin(CampaignModelAdmin):
    list_display = (
        'name', 'distance_from_star', 'diameter', 'mass', 'gravity', 'temperature',
        'number_of_moons', 'is_active', 'campaign'
    )
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'atmosphere', 'campaign')


# Continent Admin
@admin.register(Continent)
class ContinentAdmin(CampaignModelAdmin):
    list_display = ('name', 'planet', 'area', 'population', 'number_of_countries', 'is_active', 'campaign')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'planet', 'campaign')


# Country Admin
@admin.register(Country)
class CountryAdmin(CampaignModelAdmin):
    list_display = ('name', 'continent', 'area', 'is_active', 'campaign')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'continent', 'campaign')


# City Admin
@admin.register(City)
class CityAdmin(CampaignModelAdmin):
    list_display = ('name', 'country', 'is_active', 'campaign')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'country', 'campaign')


# Area Admin
@admin.register(Area)
class AreaAdmin(CampaignModelAdmin):
    list_display = ('name', 'city', 'area', 'is_active', 'campaign')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'city', 'campaign')


# Location Admin
@admin.register(Location)
class LocationAdmin(CampaignModelAdmin):
    list_display = ('name', 'area', 'is_active', 'is_public', 'campaign')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'is_public', 'area', 'campaign')


# SubLocation Admin
@admin.register(SubLocation)
class SubLocationAdmin(CampaignModelAdmin):
    list_display = ('name', 'location', 'is_active', 'campaign')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'location', 'campaign')


# Position Form for Validation
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

        # Exclude the current instance from the duplicate check
        duplicates = Position.objects.filter(
            grid_x=grid_x,
            grid_y=grid_y,
            grid_z=grid_z,
            sub_location=sub_location
        )
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)

        if duplicates.exists():
            raise ValidationError("A position with these coordinates and sub-location already exists.")
        return cleaned_data


# Position Admin with Bulk Action

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    form = PositionForm
    list_display = ('id', 'coordinates', 'sub_location', 'label_summary')
    list_filter = ('sub_location', 'grid_x', 'grid_y', 'grid_z')
    search_fields = ('id', 'grid_x', 'grid_y', 'grid_z', 'sub_location__name', 'labels')
    ordering = ('sub_location', 'grid_x', 'grid_y', 'grid_z')
    actions = ['bulk_change_sub_location']

    def get_search_results(self, request, queryset, search_term):
        """
        Overrides default search results to include custom property search.
        """
        # Default search
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Add custom search for the `coordinates` property
        try:
            x, y, z = map(int, search_term.split("x"))
            coordinates_query = Position.objects.filter(grid_x=x, grid_y=y, grid_z=z)
            queryset |= coordinates_query
        except ValueError:
            # Ignore invalid input that doesn't match the expected "x, y, z" format
            pass

        return queryset, use_distinct

    def label_summary(self, obj):
        return ", ".join(obj.labels) if obj.labels else "No Labels"

    label_summary.short_description = 'Labels'

    @admin.action(description='Change Sub-Location for selected positions')
    def bulk_change_sub_location(self, request, queryset):
        """
        Redirect to the custom view for changing sub-location.
        """
        selected = queryset.values_list('id', flat=True)
        return redirect(f'{reverse("admin:bulk_change_sub_location_view")}?ids={",".join(map(str, selected))}')

    def get_urls(self):
        """
        Add custom URL for the bulk sub-location change view.
        """
        urls = super().get_urls()
        custom_urls = [
            path('bulk_change_sub_location/', self.admin_site.admin_view(self.bulk_change_sub_location_view),
                 name='bulk_change_sub_location_view'),
        ]
        return custom_urls + urls

    def bulk_change_sub_location_view(self, request):
        """
        Custom view for bulk changing the sub-location of selected positions.
        """
        if request.method == 'POST':
            form = BulkChangeSubLocationForm(request.POST)
            if form.is_valid():
                sub_location = form.cleaned_data['sub_location']
                ids = request.GET.get('ids', '').split(',')
                positions = Position.objects.filter(id__in=ids)

                updated = positions.update(sub_location=sub_location)
                self.message_user(request, f"{updated} position(s) updated with the new sub-location.")
                return redirect('..')
        else:
            form = BulkChangeSubLocationForm()

        return render(request, 'admin/bulk_change_sub_location.html', {'form': form})


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
    list_display = ('id', 'position_from', 'position_to', 'is_active', 'is_public', 'is_locked', "is_vertical")
    list_filter = ('is_active', 'is_public', 'is_locked', 'position_from__sub_location')
    search_fields = ('position_from__id', 'position_to__id')
    ordering = ('position_from', 'position_to')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('position_from', 'position_to')


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'is_active')
    list_filter = ('is_active', 'organization')
    search_fields = ('name', 'description', 'organization__name')
    ordering = ('name',)


@admin.register(MapPosition)
class MapPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'map', 'position', 'is_active')
    list_filter = ('is_active', 'map__name')
    search_fields = ('map__name', 'position__sub_location__name', 'position__coordinates')
    ordering = ('map', 'position')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('map', 'position')
