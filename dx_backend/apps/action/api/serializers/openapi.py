# serializers.py
from rest_framework import serializers

from ...models import CharacterAction


class CharacterActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterAction
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', "initiator"]

