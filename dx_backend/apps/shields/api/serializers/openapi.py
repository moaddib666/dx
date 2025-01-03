from rest_framework import serializers

from apps.shields.models import ActiveShield, Shield


class ShieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shield
        exclude = ['created_at', 'updated_at']


class ActiveShieldSerializer(serializers.ModelSerializer):
    shield = ShieldSerializer()

    class Meta:
        model = ActiveShield
        exclude = ['created_at', 'updated_at']
