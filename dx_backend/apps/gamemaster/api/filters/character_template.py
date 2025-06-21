from django_filters import rest_framework as filters

from apps.character.models.npc import CharacterTemplate


class CharacterTemplateFilter(filters.FilterSet):
    """
    Custom filter set for CharacterTemplate model.
    Allows filtering by name, behavior, organization, path, dimension, campaign, and rank.
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = CharacterTemplate
        fields = ['name', 'behavior', 'organization', 'path', 'dimension', 'campaign', 'rank']