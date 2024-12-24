import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.adapters.channels_adapter.name_resolver import FightGroupsNameResolver
from apps.fight.models import Fight
from apps.game.services.fight.fight import FightService
from apps.character.models import Character


class AuthenticatedWebsocketConsumer(AsyncWebsocketConsumer):
    class AuthError(Exception):
        pass

    def get_user(self):
        return self.scope["user"]

    def get_character(self):
        return self.get_user().main_character

    async def authenticate(self):
        if not self.get_user().is_authenticated:
            await self.close()
            raise self.AuthError("User is not authenticated")


class FightConsumer(AuthenticatedWebsocketConsumer):
    fight: Fight
    fight_side: str
    participant: Character

    __service__: FightService

    logger = logging.getLogger("adapter.websocket.fight")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_resolver = FightGroupsNameResolver()

    def available_groups(self) -> tuple[str, str, str]:
        return (
            self.name_resolver.construct_fight_group_name(self.fight.id),
            self.name_resolver.construct_fight_side_group_name(
                self.fight.id, self.fight_side
            ),
            self.name_resolver.construct_participant_group_name(
                self.fight.id, self.participant.id
            ),
        )

    @sync_to_async
    def fill_character_info(self):
        character = self.get_character()
        fight = character.fight
        side = "a" if character in fight.side_a_participants.all() else "b"
        return character, fight, side

    async def connect(self):
        try:
            await self.authenticate()
        except self.AuthError as e:
            self.logger.warning(f"Websocket connection failed: {e}")
            return

        character, fight, side = await self.fill_character_info()
        self.participant = character
        self.fight = fight
        self.fight_side = side

        for group_name in self.available_groups():
            await self.channel_layer.group_add(group_name, self.channel_name)

        await self.accept()
        await self.say_hello()

    @sync_to_async
    def say_hello(self):
        self.__service__ = FightService(self.fight)
        self.__service__.refresh_character(self.participant)

    async def disconnect(self, close_code):
        for group_name in self.available_groups():
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive(self, *args, **kwargs):
        self.logger.debug(f"Received message: {args}, {kwargs}")

    async def send_message(self, message: dict, group_name: str):
        await self.channel_layer.group_send(
            group_name, {"type": "send_message", "message": json.dumps(message)}
        )
