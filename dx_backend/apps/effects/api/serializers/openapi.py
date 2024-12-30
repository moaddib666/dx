from rest_framework import serializers

from apps.effects.models import ActiveEffect, Effect


class EffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        exclude = ['created_at', 'updated_at']


class ActiveEffectSerializer(serializers.ModelSerializer):
    effect = EffectSerializer()

    class Meta:
        model = ActiveEffect
        exclude = ['created_at', 'updated_at']
