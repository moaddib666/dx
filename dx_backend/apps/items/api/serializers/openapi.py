from rest_framework import serializers

from apps.items.models import Item, CharacterItem, WorldItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['canonical', 'created_at', 'updated_at']
        read_only_fields = ['id']
        depth = 1


class WorldItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = WorldItem
        exclude = ['created_at', 'updated_at', 'polymorphic_ctype']
        read_only_fields = ['id']


class CharacterItemSerializer(serializers.ModelSerializer):
    world_item = WorldItemSerializer()

    class Meta:
        model = CharacterItem
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['id', 'character']
