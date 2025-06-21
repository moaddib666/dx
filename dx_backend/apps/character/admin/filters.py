from django.contrib import admin

from ..models import Character


class SubLocationFilter(admin.SimpleListFilter):
    """
    Custom filter for filtering by sublocation.
    """
    title = 'SubLocation'
    parameter_name = 'position__sublocation'

    def lookups(self, request, model_admin):
        sublocations = set(
            obj.position.sub_location for obj in Character.objects.select_related('position__sub_location') if
            obj.position
        )
        return [(s.id, s.name) for s in sublocations]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__sub_location_id=self.value())
        return queryset


class GridZFilter(admin.SimpleListFilter):
    """
    Custom filter for filtering by grid_z.
    """
    title = 'Grid Z'
    parameter_name = 'position__grid_z'

    def lookups(self, request, model_admin):
        grid_z_values = set(
            obj.position.grid_z for obj in Character.objects.select_related('position') if obj.position
        )
        return [(z, f'Grid Z: {z}') for z in grid_z_values]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__grid_z=self.value())
        return queryset