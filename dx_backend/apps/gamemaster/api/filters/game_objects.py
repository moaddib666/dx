from django_filters import rest_framework as filters

from apps.core.models import GameObject


class GameObjectFilter(filters.FilterSet):
    """
    Custom filter set for GameObject model.
    Allows filtering by object_type and position.grid_z.
    """
    object_type = filters.CharFilter(field_name='polymorphic_ctype__model')
    position_grid_z = filters.NumberFilter(field_name='position__grid_z')
    
    class Meta:
        model = GameObject
        fields = ['is_active', 'dimension', 'campaign', 'object_type', 'position_grid_z']