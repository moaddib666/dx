from rest_framework import serializers

from apps.items.models import Item, PlayerItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'icon', 'type', 'weight', 'ap_cost', 'hp_cost', 'ep_cost',
                  'once_per_fight', 'once_per_turn', 'once']
        read_only_fields = ['id']


class PlayerItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = PlayerItem
        fields = ['id', 'player', 'item', 'amount']
        read_only_fields = ['id', 'player']
