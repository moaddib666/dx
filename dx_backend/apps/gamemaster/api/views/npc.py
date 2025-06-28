from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.character.models import Character
from apps.game.services.character.character_behavior import CharacterBehaviorService
from apps.gamemaster.api.serializers.character import GameMasterCharacterInfoSerializer
from apps.gamemaster.api.serializers.npc import NPCBehaviorSerializer


class NPCViewSet(viewsets.GenericViewSet):
    """
    ViewSet for game masters to manage NPCs.
    
    This viewset provides operations for managing NPCs, such as changing their behavior.
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = Character.objects.filter(npc=True)
    serializer_class = GameMasterCharacterInfoSerializer

    def get_queryset(self):
        """
        Override to filter NPCs by the current campaign if applicable.
        """
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and hasattr(self.request.user, 'current_campaign'):
            return queryset.filter(campaign=self.request.user.current_campaign)
        return queryset

    @extend_schema(
        responses={200: GameMasterCharacterInfoSerializer}
    )
    @action(detail=True, methods=['patch'], serializer_class=NPCBehaviorSerializer)
    def change_behavior(self, request, pk=None):
        """
        Change the behavior of an NPC.
        
        This action changes the behavior of the specified NPC.
        It requires the behavior parameter.
        """
        # Get the NPC
        npc = self.get_object()

        # Validate the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Change the behavior
        behavior = serializer.validated_data['behavior']
        behavior_service = CharacterBehaviorService(npc)
        behavior_service.change_behavior(behavior)
        return Response(data=GameMasterCharacterInfoSerializer(npc).data, status=status.HTTP_200_OK)
