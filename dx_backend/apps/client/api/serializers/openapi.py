from rest_framework import serializers

from apps.client.models import Client
from apps.game.models import Campaign


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


class OpenAICampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'description', 'is_active', 'is_completed', 'background_image']
        read_only_fields = ['id', 'is_active', 'is_completed']


class CurrentCampaignSerializer(serializers.ModelSerializer):
    current_campaign_details = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['current_campaign', 'current_campaign_details']

    def get_current_campaign_details(self, obj):
        if obj.current_campaign:
            return OpenAICampaignSerializer(obj.current_campaign).data
        return None
