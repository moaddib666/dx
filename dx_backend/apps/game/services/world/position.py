import json
import logging
import uuid
from abc import abstractmethod
from typing import Any, List, Dict

from django.db import transaction, IntegrityError

from apps.character.models import Character
from apps.world.models import Position, PositionConnection


class IdTranslator:
    @abstractmethod
    def to_external_id(self, internal_id: Any) -> Any:
        pass

    @abstractmethod
    def to_internal_id(self, external_id: Any) -> Any:
        pass


class UUIDTranslator(IdTranslator):
    def to_external_id(self, internal_id: uuid.UUID) -> int:
        return internal_id.int

    def to_internal_id(self, external_id: int) -> uuid.UUID:
        return uuid.UUID(int=external_id)


class Reporter:
    @abstractmethod
    def on_position_processed(self, room):
        pass

    @abstractmethod
    def on_connection_processed(self, connection):
        pass

    @abstractmethod
    def report(self):
        pass


class ConsoleReporter(Reporter):
    def __init__(self):
        self.rooms = 0
        self.connections = 0

    def on_position_processed(self, room):
        self.rooms += 1

    def on_connection_processed(self, connection):
        self.connections += 1

    def report(self):
        print(f"Rooms: {self.rooms}")
        print(f"Connections: {self.connections}")


class PositionLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, json_file_path, default_sub_location, id_translator: IdTranslator = UUIDTranslator()):
        self.json_file_path = json_file_path
        self.default_sub_location = default_sub_location
        self.id_translator = id_translator
        self.reporter = ConsoleReporter()

    def load(self):
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)

        rooms = data.get("rooms", [])
        connections = data.get("connections", [])
        virtualConnections = data.get("virtualConnections", [])

        with transaction.atomic():
            self._load_positions(rooms)
            self._load_connections(connections)
            self._load_connections(virtualConnections)
            self.reporter.report()

    def _load_positions(self, rooms):
        for room in rooms:
            labels = room.get('labels', [])
            labels.extend([
                room['type'],
                room.get('label', 'regular'),
                room['name'],
            ])
            p, _ = Position.objects.update_or_create(
                pk=self.id_translator.to_internal_id(room['id']),
                defaults={
                    'grid_x': room['grid_x'],
                    'grid_y': room['grid_y'],
                    'grid_z': room['grid_z'],
                    'sub_location': self.default_sub_location,
                    'labels': labels
                }
            )
            self.reporter.on_position_processed(p)

    def _load_connections(self, connections):
        for connection in connections:
            from_room_id = self.id_translator.to_internal_id(connection['room_a'])
            to_room_id = self.id_translator.to_internal_id(connection['room_b'])

            try:
                from_room = Position.objects.get(pk=from_room_id)
                to_room = Position.objects.get(pk=to_room_id)
            except Position.DoesNotExist:
                self.logger.warning(
                    f"Connection between {from_room_id} and {to_room_id} skipped. Room not found.",
                )
                continue

            position_from, position_to = (
                (from_room, to_room)
                if from_room_id < to_room_id
                else (to_room, from_room)
            )

            if PositionConnection.objects.filter(
                    position_from=position_from,
                    position_to=position_to
            ).exists():
                self.logger.debug(f"Connection between {position_from} and {position_to} already exists. Skipping.")
                continue

            try:
                pc = PositionConnection.objects.create(
                    position_from=position_from,
                    position_to=position_to,
                    is_active=True,
                    is_public=True
                )
                self.reporter.on_connection_processed(pc)
            except IntegrityError as e:
                self.logger.error(
                    f"Connection between {position_from} and {position_to} failed. {str(e)}",
                    exc_info=True
                )


class JsonDumper:
    logger = logging.getLogger(__name__)

    def __init__(self, output_file_path, context=None):
        self.output_file_path = output_file_path
        self.context = context

    def dump(self):
        data = self.as_dict()

        with open(self.output_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.logger.info(f"Data successfully dumped to {self.output_file_path}")

    def as_dict(self) -> dict:
        return {
            "rooms": self._dump_positions(),
            "connections": self._dump_connections(vertical=False),
            "virtualConnections": self._dump_connections(vertical=True),
            "characters": self._dump_characters(),
        }

    def _build_url(self, url: str) -> str:
        if not self.context or 'request' not in self.context:
            return url
        request = self.context['request']
        return request.build_absolute_uri(url)

    def _dump_characters(self) -> Dict[str, List[Any]]:
        self.logger.info("Dumping characters")
        characters = Character.objects.filter(is_active=True)
        mapping = {}
        self.logger.info(f"Found {characters.count()} characters")
        for character in characters:
            avatar = None
            if character.biography and character.biography.avatar:
                avatar = self._build_url(character.biography.avatar.url)

            char_serialized = {
                "id": str(character.pk),
                "name": character.name,
                "npc": character.npc,
                "avatar": avatar,
            }
            mapping.setdefault(str(character.position_id), []).append(char_serialized)
            self.logger.debug(f"Character {character.pk} dumped to {character.position_id}")
        self.logger.info("Characters dumped")
        return mapping

    def _dump_positions(self) -> List[Dict[str, Any]]:
        positions = Position.objects.all()
        rooms = []

        for position in positions:
            room_data = {
                "id": str(position.pk),  # Serialize UUID as string
                "grid_x": position.grid_x,
                "grid_y": position.grid_y,
                "grid_z": position.grid_z,
                "type": position.labels[0] if position.labels else "unknown",
                "label": position.labels[1] if len(position.labels) > 1 else "regular",
                "name": position.labels[2] if len(position.labels) > 2 else "unknown",
            }
            rooms.append(room_data)

        return rooms

    def _dump_connections(self, vertical=False) -> List[Dict[str, Any]]:
        connections = PositionConnection.objects.filter(is_active=True)
        connection_list = []

        for connection in connections:
            if vertical and not connection.is_vertical():
                continue
            if not vertical and connection.is_vertical():
                continue
            connection_data = {
                "room_a": str(connection.position_from.pk),
                "room_b": str(connection.position_to.pk),
            }
            connection_list.append(connection_data)

        return connection_list


class MiniMapDumper:
    """
    Dumps the data across the character like a minimap. The data is used to visualize the character's surroundings.
    The size of the minimap is 5x5 - 25 rooms.
    The minimap show only 9x9 rooms around the character. with NPC and other characters.
    Other is fog of war unless the character has been there or somebody use the cartography and map the area.
    """
    pass