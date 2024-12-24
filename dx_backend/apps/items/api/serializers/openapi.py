from rest_framework import serializers

from apps.items.models import Item, CharacterItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'icon', 'type', 'weight', 'ap_cost', 'hp_cost', 'ep_cost',
                  'once_per_fight', 'once_per_turn', 'once']
        read_only_fields = ['id']


class CharacterItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = CharacterItem
        fields = ['id', 'character', 'item', 'amount']
        read_only_fields = ['id', 'character']
