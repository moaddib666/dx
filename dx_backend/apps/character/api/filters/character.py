from django_filters import rest_framework as filters

from apps.character.models import Character


class CharacterFilter(filters.FilterSet):
    npc = filters.BooleanFilter(field_name="npc")

    class Meta:
        model = Character
        fields = ['npc', "position"]
