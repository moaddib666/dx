from rest_framework import serializers
from apps.modificators.models import Modificator, StatModificator, CharacterModificator


class StatModificatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatModificator
        fields = ['id', 'stat', 'value']
        read_only_fields = ['id']


class ModificatorSerializer(serializers.ModelSerializer):
    stat_modificators = StatModificatorSerializer(many=True, write_only=True)
    stat_changes = serializers.SerializerMethodField()

    class Meta:
        model = Modificator
        fields = ['id', 'name', 'description', 'icon', 'stat_modificators', 'stat_changes']
        read_only_fields = ['id']

    def get_stat_changes(self, obj):
        # Aggregate stat changes from related StatModificator objects
        stat_modificators = StatModificator.objects.filter(modificator=obj)
        return [
            {'stat': sm.stat, 'value': sm.value} for sm in stat_modificators
        ]

    def create(self, validated_data):
        stat_modificators_data = validated_data.pop('stat_modificators', [])
        modificator = Modificator.objects.create(**validated_data)

        for stat_modificator_data in stat_modificators_data:
            StatModificator.objects.create(modificator=modificator, **stat_modificator_data)

        return modificator

    def update(self, instance, validated_data):
        stat_modificators_data = validated_data.pop('stat_modificators', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()

        # Update StatModificators
        for stat_modificator_data in stat_modificators_data:
            stat_id = stat_modificator_data.get('id')
            if stat_id:
                # Update existing StatModificator
                stat_modificator = StatModificator.objects.get(id=stat_id, modificator=instance)
                stat_modificator.stat = stat_modificator_data.get('stat', stat_modificator.stat)
                stat_modificator.value = stat_modificator_data.get('value', stat_modificator.value)
                stat_modificator.save()
            else:
                # Create new StatModificator
                StatModificator.objects.create(modificator=instance, **stat_modificator_data)

        return instance


class CharacterModificatorSerializer(serializers.ModelSerializer):
    modificator = ModificatorSerializer()

    class Meta:
        model = CharacterModificator
        fields = ['id', 'character', 'modificator']
        read_only_fields = ['id']
