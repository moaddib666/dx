from drf_spectacular.utils import extend_schema

from apps.core.bus.base import GameEvent
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.adapters.centrifugo.api.serializers import ConnectSerializer, PublishSerializer, SubscribeSerializer
from apps.adapters.name_resolver import PlayerGroupsNameResolver, FightGroupsNameResolver, \
    PlayerActionGroupsNameResolver
from apps.game.services.fight.fight import FightService
from apps.game.services.player.core import PlayerService


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

    p_name_resolver = PlayerGroupsNameResolver
    a_name_resolver = PlayerActionGroupsNameResolver
    f_name_resolver = FightGroupsNameResolver

    @extend_schema(request=ConnectSerializer, responses={200: dict})
    @action(detail=False, methods=['post'], url_path='connect')
    def connect(self, request):
        serializer = ConnectSerializer(data=request.data)

        player = request.user.player
        if not player:
            return Response({"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            player_svc = PlayerService(player)
            player_id = player_svc.get_id()
            channels = []

            player_name_resolver = self.p_name_resolver()
            action_name_resolver = self.a_name_resolver()

            channels.append(player_name_resolver.construct_player_online_group_name())  # player::online
            channels.append(
                player_name_resolver.construct_player_online_id_group_name(player_id))  # player::online::<player_id>
            channels.append(
                action_name_resolver.construct_player_action_group_name(player_id))  # player_action::<player_id>
            if player_svc.in_fight():
                fight_id = player_svc.get_fight_id()
                fight_team = player_svc.get_fight_team()
                fight_name_resolver = self.f_name_resolver()
                channels.append(fight_name_resolver.construct_fight_group_name(fight_id))  # fight::<fight_id>
                channels.append(fight_name_resolver.construct_fight_side_group_name(fight_id,
                                                                                    fight_team))  # fight::<fight_id>::<fight_team>
                channels.append(fight_name_resolver.construct_participant_group_name(fight_id,
                                                                                     player_id))  # fight::<fight_id>::participant::<player_id>

            response_data = {
                "result": {
                    "user": player_id,
                    "info": {
                        "name": player_svc.player.name,  # Example user information
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
            if event.full_event_name == "player.refresh":
                player = PlayerService(request.user.player)
                if player.in_fight():
                    fight_svc = FightService(player.player.fight)
                    fight_svc.refresh_player(player)

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
