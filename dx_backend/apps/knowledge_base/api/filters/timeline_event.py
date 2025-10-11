from django_filters import rest_framework as filters

from apps.knowledge_base.models import TimeLineEvent


class TimeLineEventFilter(filters.FilterSet):
    """
    Custom filter set for TimeLineEvent model.
    Allows filtering by document, date_time, and date_time fields (active_glow, sol, solar_year).
    """
    document = filters.UUIDFilter(field_name='document__id')
    date_time = filters.UUIDFilter(field_name='date_time__id')
    active_glow = filters.BooleanFilter(field_name='date_time__active_glow')
    sol = filters.NumberFilter(field_name='date_time__sol')
    solar_year = filters.NumberFilter(field_name='date_time__solar_year')
    sol_gte = filters.NumberFilter(field_name='date_time__sol', lookup_expr='gte')
    sol_lte = filters.NumberFilter(field_name='date_time__sol', lookup_expr='lte')
    solar_year_gte = filters.NumberFilter(field_name='date_time__solar_year', lookup_expr='gte')
    solar_year_lte = filters.NumberFilter(field_name='date_time__solar_year', lookup_expr='lte')
    
    class Meta:
        model = TimeLineEvent
        fields = ['document', 'date_time', 'active_glow', 'sol', 'solar_year']
