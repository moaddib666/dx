import logging

from django.db import transaction
from django.db.models import QuerySet

from apps.adapters.protocol.sender import Sender
from apps.core.bus.events.fight.produced import CharacterNewTurnGameEvent
from apps.core.models import CurrentTurn, FIGHT_TURN_DURATION_SECONDS
from apps.fight.models import Fight, FightTurn
from apps.game.exceptions import GameLogicException
from apps.game.services.fight.duel import InvitationService
from apps.game.services.fight.processor import TurnProcessorService
from apps.game.services.notifier.fight import FightNotifier
from apps.game.services.character.core import CharacterService


class FightService:
    notifier: FightNotifier
    logger = logging.getLogger("game.services.fight")

    @classmethod
    def create_from_duel_invitation(cls, invitation: InvitationService):
        cls.logger.info(f'Creating fight from duel invitation {invitation}')
        return cls.create(
            participants_a=[],
            participants_b=[],
            initiator=invitation.character1,
            target=invitation.character2,
        )

    @classmethod
    def create(cls, participants_a: [CharacterService], participants_b: [CharacterService], initiator: CharacterService,
               target: CharacterService, is_open=True):
        fight = Fight.objects.create(
            initiator=initiator.character,
            target=target.character,
            is_open=is_open,
        )
        fight.side_a_participants.add(initiator.character, *[p.main_character for p in participants_a])
        fight.side_b_participants.add(target.character, *[p.main_character for p in participants_b])
        for p in participants_a + participants_b + [initiator, target]:
            p.main_character.fight = fight
            p.main_character.save()
        cls.logger.info(f'Fight created {fight}')
        return cls(fight)

    def __init__(self, fight: Fight, notifier: Sender = None):
        self.fight = fight
        self.notifier = notifier or FightNotifier(fight.id)

    def start(self):
        self.logger.info(f'Starting fight {self.fight}')
        self.fight.current_turn = self.fight.turns.create(
            fight=self.fight,
        )
        self.fight.save()

    def leave(self, character_service):
        self.logger.info(f'Character {character_service.main_character} is leaving fight {self.fight}')
        self.fight.side_a_participants.remove(character_service.main_character)
        self.fight.side_b_participants.remove(character_service.main_character)

        if not self.fight.side_a_participants.exists() or not self.fight.side_b_participants.exists():
            self.end()

    def end(self):
        self.logger.info(f'Ending fight {self.fight}')
        self.fight.is_ended = True
        self.fight.save()
        return self.fight

    def join(self, character_service, side):

        if self.fight.is_ended:
            raise GameLogicException('Fight is already ended')
        if not self.fight.is_open:
            raise GameLogicException('Fight is not open')

        if side == 'a':  # TODO: make enum with sides Attacker and Defender
            self.fight.side_a_participants.add(character_service.main_character)
        else:
            self.fight.side_b_participants.add(character_service.main_character)
        self.logger.info(f'Character {character_service.main_character} joined fight {self.fight} on side {side}')
        self.fight.save()

    def refresh_character(self, character: CharacterService):
        self.logger.info(f'Refreshing character {character} in fight {self.fight}')
        self.notifier.send_participant(
            character.get_id(),
            CharacterNewTurnGameEvent.create_event(
                self.serialize_current_turn(),
                character.get_character_info(),
            )
        )

    def serialize_current_turn(self) -> CurrentTurn:
        return CurrentTurn(
            id=self.fight.current_turn.id,
            started_at=self.fight.current_turn.created_at,
            duration=FIGHT_TURN_DURATION_SECONDS,
        )

    def get_participants(self) -> QuerySet:
        return self.fight.side_a_participants.all() | self.fight.side_b_participants.all()

    def process_current_turn(self):
        self.logger.info(f"Processing current turn for fight {self.fight.id}")

    def prepare_characters(self):
        self.logger.info(f"Filling up characters AP for fight {self.fight.id}")
        for participant in (
                self.get_participants()
        ):

            character = CharacterService(participant)
            if not character.is_knocked_out():
                character.refill_ap()
                self.logger.debug(f"Refilled AP for character {participant.id}")
            self.refresh_character(character)

    def spawn_turn(self):
        self.logger.info(f"Spawning new turn for fight {self.fight.id}")
        previous_turn = self.fight.current_turn
        previous_turn.refresh_from_db()
        if previous_turn and not previous_turn.is_finished:
            self.logger.error(f"Previous turn {previous_turn.id} is not finished")
            raise GameLogicException("Previous turn is not finished")
        turn = FightTurn.objects.create(fight=self.fight)
        self.fight.current_turn = turn
        self.fight.save()
        self.logger.info(f"Spawned new turn {turn.id} for fight {self.fight.id}")
        self.prepare_characters()

    @transaction.atomic
    def process(self):
        self.logger.info(f"Processing fight {self.fight.id}")
        if self.fight.current_turn:
            turn_svc = TurnProcessorService(self.fight.current_turn, self.notifier)
            if not turn_svc.ready_to_processing():
                return
            self.logger.debug(f"Turn {self.fight.current_turn.id} is ready to processing")
            turn_svc.play()
        self.spawn_turn()
