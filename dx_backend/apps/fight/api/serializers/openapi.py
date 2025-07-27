# serializers.py
from rest_framework import serializers

from apps.fight.models import Fight


class FightGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fight
        exclude = (
            "updated_at",
            "created_at",
        )
