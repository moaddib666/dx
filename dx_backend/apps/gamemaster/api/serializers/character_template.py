from rest_framework import serializers

from apps.character.models.npc import CharacterTemplate
from apps.character.api.serializers.openapi import ThePathSerializer
from apps.character.models import Rank


class CharacterTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for CharacterTemplate model.

    This serializer provides the necessary data for listing character templates,
    including template name, id, behavior, organization, avatar, grade, and path.
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    avatar = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    path = ThePathSerializer(read_only=True)

    def get_avatar(self, obj):
        """
        Get the avatar URL from the biography_template if it exists.
        Uses request from context to build absolute URL.
        """
        if obj.biography_template and obj.biography_template.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.biography_template.avatar.url)
            return obj.biography_template.avatar.url
        return None

    def get_grade(self, obj):
        """
        Get the grade from the rank if it exists.
        """
        if obj.rank:
            return {
                'grade': obj.rank.grade,
                'grade_rank': obj.rank.grade_rank,
                'name': obj.rank.name
            }
        return None

    class Meta:
        model = CharacterTemplate
        fields = [
            'id', 'name', 'behavior', 'organization', 'organization_name', 
            'avatar', 'grade', 'path'
        ]
        read_only_fields = fields


class CreateNPCFromTemplateSerializer(serializers.Serializer):
    """
    Serializer for creating an NPC from a template.

    This serializer validates the data needed to create an NPC from a template,
    including the template ID and position ID.
    """
    template_id = serializers.IntegerField(required=True)
    position_id = serializers.IntegerField(required=True)
