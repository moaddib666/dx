from rest_framework import serializers

from apps.bargain.models import OfferedItem, Bargain


class OfferedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferedItem
        exclude = ("created_at", "updated_at")
        read_only_fields = ("id", "bargain")


class DetailedOfferedItemSerializer(OfferedItemSerializer):
    class Meta(OfferedItemSerializer.Meta):
        depth = 2


class DetailedBargainSerializer(serializers.ModelSerializer):
    side_a_offered_items = DetailedOfferedItemSerializer(many=True)
    side_b_offered_items = DetailedOfferedItemSerializer(many=True)

    class Meta:
        model = Bargain
        exclude = ("created_at", "updated_at")


class BargainCreateSerializer(serializers.Serializer):
    target_character_id = serializers.UUIDField()


class BargainSerializer(serializers.ModelSerializer):
    side_a_offered_items = OfferedItemSerializer(many=True)
    side_b_offered_items = OfferedItemSerializer(many=True)

    class Meta:
        model = Bargain
        exclude = ("created_at", "updated_at")
