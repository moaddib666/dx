import logging
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models.dice import ChallengeCreationRequest
from apps.dice.models import Challenge
from apps.game.services.challenge import ChallengeService
from apps.gamemaster.api.serializers.challenge import (
    GameMasterCreateChallengeSerializer,
    GameMasterChallengeResponseSerializer
)


class GameMasterChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for GameMasters to create and manage challenges for characters.
    
    This viewset provides functionality for GameMasters to:
    - Create new challenges for characters
    - View existing challenges
    - Configure challenge parameters including difficulty, dice, modifiers, and advantage/disadvantage
    
    The challenge creation process includes business logic that automatically adds
    modifiers based on character state, stats, effects, skills, and items.
    """
    queryset = Challenge.objects.all()
    permission_classes = [permissions.IsAdminUser]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.challenge_service = ChallengeService()
        self.logger = logging.getLogger(__name__)
    
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        if self.action == 'create_challenge':
            return GameMasterCreateChallengeSerializer
        return GameMasterChallengeResponseSerializer
    
    def get_queryset(self):
        """
        Override to filter challenges by the current campaign if applicable.
        Includes prefetching for performance optimization.
        """
        queryset = super().get_queryset().select_related(
            'target',  # Character who faces the challenge
            'outcome'  # DiceRollResult if challenge is completed
        ).prefetch_related(
            'modifiers'  # All challenge modifiers
        )
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'current_campaign'):
            # Filter challenges for characters in the current campaign
            return queryset.filter(target__campaign=self.request.user.current_campaign)
        return queryset
    
    @extend_schema(
        description="Create a new challenge for a character",
        request=GameMasterCreateChallengeSerializer,
        responses={
            201: OpenApiResponse(
                response=GameMasterChallengeResponseSerializer,
                description="Challenge created successfully"
            ),
            400: OpenApiResponse(description="Invalid request data"),
            403: OpenApiResponse(description="Permission denied - Admin access required"),
            404: OpenApiResponse(description="Target character not found")
        },
        summary="Create Challenge",
    )
    @action(detail=False, methods=['post'], url_path='create')
    @transaction.atomic
    def create_challenge(self, request):
        """
        Create a new challenge for a character.
        
        This endpoint allows GameMasters to create challenges for players by:
        1. Selecting the target character
        2. Setting difficulty class and dice configuration
        3. Choosing the relevant character stat
        4. Adding custom modifiers
        5. Setting advantage/disadvantage
        
        The system will automatically:
        - Add modifiers based on character's current state (health, energy, etc.)
        - Apply business logic for additional modifiers from effects, skills, and items
        - Set the challenge as the character's current challenge
        - Send event notifications via the event bus
        
        **Request Body:**
        ```json
        {
            "target_character": "character_uuid",
            "difficulty": 15,
            "dice_sides": 20,
            "stat": "physical_strength",
            "advantage": false,
            "disadvantage": false,
            "description": "Climb the steep cliff face",
            "modifiers": [
                {
                    "name": "Climbing Gear",
                    "value": 2
                },
                {
                    "name": "Bad Weather",
                    "value": -1
                }
            ]
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Extract validated data
            validated_data = serializer.validated_data
            target_character = validated_data['target_character']
            
            self.logger.info(
                f"GameMaster {request.user.email} creating challenge for character {target_character.name}"
            )
            
            # Create ChallengeCreationRequest DTO
            challenge_request = ChallengeCreationRequest(
                target_character_id=target_character.id,
                difficulty=validated_data['difficulty'],
                dice_sides=validated_data.get('dice_sides', 20),
                stat=validated_data.get('stat', 'luck'),
                advantage=validated_data.get('advantage', False),
                disadvantage=validated_data.get('disadvantage', False),
                description=validated_data.get('description', ''),
                modifiers=validated_data.get('modifiers', [])
            )
            
            # Create the challenge using the service with DTO
            challenge = self.challenge_service.create_challenge_for_character(
                target_character=target_character,
                request=challenge_request
            )
            
            # Return the created challenge
            response_serializer = GameMasterChallengeResponseSerializer(challenge)
            
            self.logger.info(
                f"Challenge {challenge.id} created successfully for character {target_character.name}"
            )
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            self.logger.error(f"Error creating challenge: {str(e)}")
            return Response(
                {"error": "Failed to create challenge", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    