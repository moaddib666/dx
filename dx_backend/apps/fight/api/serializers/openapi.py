# serializers.py
from rest_framework import serializers

from apps.character.models import Character
from apps.fight.models import Fight


class Fighter(serializers.ModelSerializer):
    path_name = serializers.CharField(source="path.name", read_only=True)
    rank_name = serializers.CharField(source="rank.name", read_only=True)
    avatar = serializers.ImageField(source="biography.avatar", read_only=True)
    alive = serializers.BooleanField(read_only=True)

    class Meta:
        model = Character
        fields = (
            "id",
            "name",
            "path_name",
            "rank_name",
            "avatar",
            "alive",
        )
        read_only_fields = fields


class FightGenericSerializer(serializers.ModelSerializer):
    joined = Fighter(
        many=True,
        read_only=True
    )
    pending_join = serializers.SerializerMethodField()
    attacker = Fighter(read_only=True)
    defender = Fighter(read_only=True)

    def get_pending_join(self, obj):
        """Get pending joiners from the CharactersPendingJoinFight relationship."""
        pending_characters = [pending_record.character for pending_record in obj.pending_joiners.all()]
        return Fighter(pending_characters, many=True).data

    class Meta:
        model = Fight
        exclude = (
            "updated_at",
            "created_at",
        )
