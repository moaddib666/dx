from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.client.models import Client
from apps.game.models import Campaign
from apps.character.models import Character


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

    class Meta:
        model = Client
        fields = ['current_campaign']


class BasicCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'is_active']


# Dirty Hack for now
from apps.character.api.serializers.openapi import OpenaiCharacterSerializer


class CurrentClientInfoSerializer(serializers.ModelSerializer):
    current_campaign = OpenAICampaignSerializer(read_only=True)
    play_campaigns = OpenAICampaignSerializer(many=True, read_only=True)
    master_campaigns = OpenAICampaignSerializer(many=True, read_only=True)
    owned_characters = serializers.SerializerMethodField()
    main_character = OpenaiCharacterSerializer(read_only=True)

    @extend_schema_field(OpenaiCharacterSerializer(many=True))
    def get_owned_characters(self, obj):
        # Filter out NPC characters (npc=True)
        characters = obj.available_characters.filter(npc=False)
        return OpenaiCharacterSerializer(
            characters, many=True, context=self.context
        ).data

    class Meta:
        model = Client
        fields = [
            'id',
            'is_active',
            'current_campaign',
            'main_character',
            'play_campaigns',
            'master_campaigns',
            'owned_characters'
        ]
