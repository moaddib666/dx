from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.action.models import Cycle


class GameCycleSerializer(serializers.ModelSerializer):
    is_current = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField())
    def get_is_current(self, obj):
        current_cycle = Cycle.objects.current(obj.campaign)
        return current_cycle.pk == obj.pk if current_cycle else False

    class Meta:
        model = Cycle
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
