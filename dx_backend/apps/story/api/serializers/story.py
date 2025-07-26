from rest_framework import serializers
from apps.story.models import Story, Chapter, Quest, Condition, Reward, TokenReward, ItemReward, EffectReward, Note
from apps.core.models import Trigger


class TriggerSerializer(serializers.ModelSerializer):
    """
    Serializer for Trigger model.
    """

    class Meta:
        model = Trigger
        exclude = ("created_at", "updated_at")


class ConditionSerializer(serializers.ModelSerializer):
    """
    Serializer for Condition model.
    """
    triggers = TriggerSerializer(many=True, read_only=True)
    trigger_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Condition
        fields = ['id', 'type', 'triggers', 'trigger_ids']

    def create(self, validated_data):
        trigger_ids = validated_data.pop('trigger_ids', [])
        condition = Condition.objects.create(**validated_data)
        if trigger_ids:
            condition.triggers.set(trigger_ids)
        return condition

    def update(self, instance, validated_data):
        trigger_ids = validated_data.pop('trigger_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if trigger_ids is not None:
            instance.triggers.set(trigger_ids)
        return instance


class TokenRewardSerializer(serializers.ModelSerializer):
    """
    Serializer for TokenReward model.
    """

    class Meta:
        model = TokenReward
        fields = ['id', 'amount', 'token', 'reward']


class ItemRewardSerializer(serializers.ModelSerializer):
    """
    Serializer for ItemReward model.
    """

    class Meta:
        model = ItemReward
        fields = ['id', 'amount', 'item', 'reward']


class EffectRewardSerializer(serializers.ModelSerializer):
    """
    Serializer for EffectReward model.
    """

    class Meta:
        model = EffectReward
        fields = ['id', 'effect', 'duration', 'reward']


class RewardSerializer(serializers.ModelSerializer):
    """
    Serializer for Reward model.
    """
    tokens = TokenRewardSerializer(many=True, read_only=True)
    items = ItemRewardSerializer(many=True, read_only=True)
    effects = EffectRewardSerializer(many=True, read_only=True)

    class Meta:
        model = Reward
        fields = ['id', 'description', 'experience', 'tokens', 'items', 'effects']


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model.
    """

    class Meta:
        model = Note
        fields = ['id', 'quest', 'image', 'content', 'order']


class QuestSerializer(serializers.ModelSerializer):
    """
    Serializer for Quest model.
    """
    starters = ConditionSerializer(many=True, read_only=True)
    objectives = ConditionSerializer(many=True, read_only=True)
    on_success = RewardSerializer(read_only=True)
    on_failure = RewardSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    starter_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    objective_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    success_reward_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    failure_reward_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Quest
        fields = [
            'id', 'title', 'description', 'starters', 'objectives', 'on_success', 'on_failure',
            'image', 'cycle_limit', 'order', 'chapter', 'notes',
            'starter_ids', 'objective_ids', 'success_reward_id', 'failure_reward_id'
        ]

    def create(self, validated_data):
        starter_ids = validated_data.pop('starter_ids', [])
        objective_ids = validated_data.pop('objective_ids', [])
        success_reward_id = validated_data.pop('success_reward_id', None)
        failure_reward_id = validated_data.pop('failure_reward_id', None)

        quest = Quest.objects.create(**validated_data)

        if starter_ids:
            quest.starters.set(starter_ids)
        if objective_ids:
            quest.objectives.set(objective_ids)
        if success_reward_id:
            quest.on_success_id = success_reward_id
        if failure_reward_id:
            quest.on_failure_id = failure_reward_id
        quest.save()

        return quest

    def update(self, instance, validated_data):
        starter_ids = validated_data.pop('starter_ids', None)
        objective_ids = validated_data.pop('objective_ids', None)
        success_reward_id = validated_data.pop('success_reward_id', None)
        failure_reward_id = validated_data.pop('failure_reward_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if starter_ids is not None:
            instance.starters.set(starter_ids)
        if objective_ids is not None:
            instance.objectives.set(objective_ids)
        if success_reward_id is not None:
            instance.on_success_id = success_reward_id
        if failure_reward_id is not None:
            instance.on_failure_id = failure_reward_id
        instance.save()

        return instance


class ChapterSerializer(serializers.ModelSerializer):
    """
    Serializer for Chapter model.
    """
    quests = QuestSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'image', 'order', 'story', 'quests']


class StorySerializer(serializers.ModelSerializer):
    """
    Serializer for Story model.
    """
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'title', 'description', 'tags', 'image', 'canonical', 'chapters']


class StoryDetailSerializer(StorySerializer):
    """
    Detailed serializer for Story model with nested chapters and quests.
    """
    pass
