from rest_framework import serializers


class CharacterStatSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
