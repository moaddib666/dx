from rest_framework import serializers

from apps.client.models import Client


class OpenAIClientManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active', 'provider', 'is_staff', 'date_joined']


class RegistrationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'write_only': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['provider'] = Client.ClientProvider.local
        client = Client.objects.create_user(**validated_data)
        return client
