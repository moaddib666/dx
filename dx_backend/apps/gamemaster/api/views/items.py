from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.gamemaster.api.serializers.item import GameMasterItemSerializer, SpawnItemSerializer
from apps.items.api.serializers.openapi import (
    WorldItemSerializer, CharacterItemSerializer
)
from apps.items.models import Item, WorldItem, CharacterItem
from apps.character.models import Character
from apps.world.models import Position
from apps.game.services.items.world_item import default_world_item_factory
from apps.game.services.character.character_items import default_items_svc_factory


class GameMasterItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for game masters to manage items.
    This viewset provides full CRUD operations for items.
    """
    queryset = Item.objects.all()
    serializer_class = GameMasterItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]

    @extend_schema(
        description="Spawn an item in the game world. Creates a WorldItem instance from the Item and optionally assigns it to a character.",
        request=SpawnItemSerializer,
        responses={
            201: WorldItemSerializer,
        },
        operation_id="spawn_item",
        tags=["gamemaster", "items"]
    )
    @action(detail=True, methods=['post'])
    def spawn_item(self, request, pk=None):
        """
        Implementation of the spawn_item action.

        Creates a WorldItem from the Item specified by pk, and optionally assigns it to a character.
        The request data is validated using SpawnItemSerializer.

        Logic flow:
        1. Get the Item object using pk
        2. Validate request data using SpawnItemSerializer
        3. Get Character and/or Position objects if IDs are provided
        4. Create WorldItem using WorldItemFactory
        5. If character is provided, assign the item to the character using CharacterItemsService
        6. Return the created WorldItem serialized with WorldItemSerializer

        Error handling:
        - Returns 400 with error message if validation fails
        - Returns 400 with error message if Character or Position not found
        - Returns 400 with error message if item creation or assignment fails
        """
        item = self.get_object()
        serializer = SpawnItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        # Get validated data
        to_character_id = serializer.validated_data.get('to_character_id')
        to_position_id = serializer.validated_data.get('to_position_id')

        # Get character and position objects if IDs are provided
        character = None
        position = None

        try:
            if to_character_id:
                character = Character.objects.get(gameobject_ptr_id=to_character_id)
                # If position is not provided, use character's position
                if not to_position_id:
                    position = character.position

            if to_position_id:
                position = Position.objects.get(id=to_position_id)
        except Character.DoesNotExist:
            return Response(
                {"error": f"Character with ID {to_character_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Position.DoesNotExist:
            return Response(
                {"error": f"Position with ID {to_position_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create world item using the factory
            world_item = default_world_item_factory.create_world_item(
                item=item,
                position=position,
                dimension=character.dimension if character else None
            )

            # If character is provided, assign the item to the character
            if character:
                character_items_service = default_items_svc_factory.from_character(character)
                character_items_service.pick_item(world_item)

            # Return the created world item
            return Response(
                WorldItemSerializer(world_item).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to spawn item: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )



class GameMasterWorldItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage world items.
    This viewset provides full CRUD operations for world items.
    """
    queryset = WorldItem.objects.all()
    serializer_class = WorldItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterCharacterItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage character items.
    This viewset provides full CRUD operations for character items.
    """
    queryset = CharacterItem.objects.all()
    serializer_class = CharacterItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
