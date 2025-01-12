from rest_framework import serializers

from apps.core.models import StatObject, ViolationObject


class CharacterStatSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class StatObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatObject
        exclude = [
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        ]


class ViolationObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationObject
        exclude = [
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        ]
