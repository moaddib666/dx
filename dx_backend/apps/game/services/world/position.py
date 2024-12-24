import json
import logging
import uuid
from abc import abstractmethod
from typing import Any

from django.db import transaction, IntegrityError

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

        with transaction.atomic():
            self._load_positions(rooms)
            self._load_connections(connections)
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
                pc, _ = PositionConnection.objects.create(
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
