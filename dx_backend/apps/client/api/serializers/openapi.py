from rest_framework import serializers

from apps.client.models import Client


class OpenAIClientManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active', 'provider', 'is_staff', 'date_joined']

