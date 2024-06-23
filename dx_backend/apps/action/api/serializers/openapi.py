# serializers.py
from rest_framework import serializers

from ...models import PlayerAction


class PlayerActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerAction
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', "initiator"]

