from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, permissions, status, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.character.api.serializers.openapi import CharacterTemplateFullSerializer
from apps.character.models.npc import CharacterTemplate
from apps.core.utils.api import CampaignFilterMixin
from apps.game.services.character.template_exporter import CharacterTemplateExporter
from apps.game.services.npc.factory import NPCFactory
from apps.game.services.npc.factory.interface import NPCFactoryConfig
from apps.gamemaster.api.filters import CharacterTemplateFilter
from apps.gamemaster.api.serializers.character import GameMasterCharacterInfoSerializer
from apps.gamemaster.api.serializers.character_template import CharacterTemplateSerializer, \
    CreateNPCFromTemplateSerializer
from apps.world.models import Position


class CharacterTemplateViewSet(CampaignFilterMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for game masters to view character templates and create NPCs from them.

    This viewset provides read-only operations for character templates and an action
    to create NPCs from templates.
    """

    class StandardResultsSetPagination(pagination.PageNumberPagination):
        page_size = 100
        page_size_query_param = 'page_size'
        max_page_size = 200

    queryset = CharacterTemplate.objects.all()
    serializer_class = CharacterTemplateSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterTemplateFilter
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['post'], serializer_class=CreateNPCFromTemplateSerializer)
    @transaction.atomic
    def create_npc(self, request):
        """
        Create an NPC from a template.

        This action creates a new NPC based on the specified template and position.
        It requires template_id and position_id parameters.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        template_id = serializer.validated_data['template_id']
        position_id = serializer.validated_data['position_id']

        # Get the template and position
        template = get_object_or_404(CharacterTemplate, id=template_id)
        position = get_object_or_404(Position, id=position_id)

        # Get the campaign from the user's main character or fall back to the template's campaign
        campaign = None
        if (self.request.user.is_authenticated and
                hasattr(self.request.user, 'main_character') and
                self.request.user.main_character and
                self.request.user.main_character.campaign):
            campaign = self.request.user.main_character.campaign
        else:
            campaign = template.campaign

        # Create the NPC
        config = NPCFactoryConfig(
            template=template,
            position=position,
            behavior=template.behavior,
            campaign=campaign
        )

        factory = NPCFactory()
        npc = factory.create_npc(config)

        # Serialize the created NPC with all details including avatar
        serializer = GameMasterCharacterInfoSerializer(npc, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Export Character Template",
        description="Export a character template as JSON. Game Master access only.",
        responses={
            200: CharacterTemplateFullSerializer,
            403: "Game Master access required",
            404: "Template not found",
        }
    )
    @action(detail=True, methods=['get'])
    def export_template(self, request, pk=None):
        """
        Export character template as JSON.
        Game Master only endpoint.

        Uses the template ID from the URL to export a specific template.
        """
        # Create the template using the exporter with the template ID
        template_exporter = CharacterTemplateExporter(template_id=pk)
        template = template_exporter.export_template()

        # Return the template data
        return Response(template.model_dump())
