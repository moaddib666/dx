from drf_spectacular.utils import extend_schema

from apps.core.bus.base import GameEvent
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.adapters.centrifugo.api.serializers import ConnectSerializer, PublishSerializer, SubscribeSerializer
from apps.adapters.name_resolver import CharacterGroupsNameResolver, FightGroupsNameResolver, \
    CharacterActionGroupsNameResolver
from apps.core.bus.channels import Channel
from apps.game.services.character.core import CharacterService


class JWTCookieAuthentication(JWTAuthentication):

    def get_header(self, request: Request) -> bytes:
        return request.COOKIES.get('dx_backend_token').encode()

    def get_raw_token(self, header: bytes) -> str:
        return header.decode()


class CentrifugoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [
        JWTCookieAuthentication
    ]

    p_name_resolver = CharacterGroupsNameResolver
    a_name_resolver = CharacterActionGroupsNameResolver
    f_name_resolver = FightGroupsNameResolver

    @extend_schema(request=ConnectSerializer, responses={200: dict})
    @action(detail=False, methods=['post'], url_path='connect')
    def connect(self, request):
        serializer = ConnectSerializer(data=request.data)

        character = request.user.main_character
        if not character:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            character_svc = CharacterService(character)
            character_id = character_svc.get_id()
            channels = [
                Channel.WORLD,
            ]

            # character_name_resolver = self.p_name_resolver()
            # action_name_resolver = self.a_name_resolver()

            # channels.append(character_name_resolver.construct_character_online_group_name())  # character::online
            # channels.append(
            #     character_name_resolver.construct_character_online_id_group_name(character_id))  # character::online::<character_id>
            # channels.append(
            #     action_name_resolver.construct_character_action_group_name(character_id))  # character_action::<character_id>

            response_data = {
                "result": {
                    "user": character_id,
                    "info": {
                        "name": character_svc.character.name,  # Example user information
                    },
                    "channels": channels
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='publish')
    def publish(self, request):
        serializer = PublishSerializer(data=request.data)
        if serializer.is_valid():
            channel = serializer.validated_data['channel']
            payload = serializer.validated_data['data']

            event = GameEvent.parse_raw(payload)
            if event.full_event_name == "character.refresh":
                character = CharacterService(request.user.main_character)
                if character.in_fight():
                    pass
                    # fight_svc = FightService(character.character.fight)
                    # fight_svc.refresh_character(character)

            # Implement your logic here to handle the publish event

            # Return a response
            response_data = {
                "result": {}
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=SubscribeSerializer, responses={200: dict})
    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            channel = serializer.validated_data['channel']

            # Implement your logic here to handle the subscription event

            # Return a response
            response_data = {
                "result": {}
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
