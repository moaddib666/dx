from django_filters import rest_framework as filters

from apps.shields.models import ActiveShield


class CharacterActiveShieldFilter(filters.FilterSet):

    class Meta:
        model = ActiveShield
        fields = ['target', ]
