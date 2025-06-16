from rest_framework import serializers

from apps.core.serializers.dto import BaseSkillSerializer, EffectSerializer
from apps.items.models import Item


class GameMasterItemSerializer(serializers.ModelSerializer):
    skill = BaseSkillSerializer(read_only=True)
    effect = EffectSerializer(read_only=True)

    class Meta:
        model = Item
        exclude = ['canonical', 'created_at', 'updated_at']
        read_only_fields = ['id']
        depth = 1

    def to_representation(self, instance):
        """
        Custom representation to handle nested serializers.
        """
        representation = super().to_representation(instance)

        # Handle skill serialization
        if instance.skill:
            skill_data = {
                'name': instance.skill.name,
                'description': instance.skill.description,
                'school': instance.skill.school.id if instance.skill.school else None,
                'multi_target': instance.skill.multi_target,
                'type': instance.skill.type,
                'grade': instance.skill.grade,
                'cost': instance.skill.cost,
                'effect': instance.skill.effect,
                'impact': instance.skill.impact
            }
            representation['skill'] = BaseSkillSerializer(skill_data).data
        else:
            representation['skill'] = None

        # Handle effect serialization
        if instance.effect:
            effect_data = {
                'name': instance.effect.id,  # Effect.id is the name (EffectType)
                'impact': None,  # Default value, will be overridden if present in JSON
                'base_chance': 1.0,  # Default value
                'duration_modifier': {'label': 'default', 'formula': {'base': 0, 'requires': [], 'scaling': []}},  # Default value
                'stat_modifiers': []  # Default value
            }
            # Add any additional data from the effect model if available
            representation['effect'] = EffectSerializer(effect_data).data
        else:
            representation['effect'] = None

        return representation
