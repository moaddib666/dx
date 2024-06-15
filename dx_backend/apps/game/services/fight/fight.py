from apps.fight.models import Fight
from apps.game.exceptions import GameLogicException
from apps.game.services.fight.duel import InvitationService
from apps.game.services.player.core import PlayerService


class FightService:

    @classmethod
    def create_from_duel_invitation(cls, invitation: InvitationService):
        return cls.create(
            participants_a=[],
            participants_b=[],
            initiator=invitation.player1,
            target=invitation.player2,
        )

    @classmethod
    def create(cls, participants_a: [PlayerService], participants_b: [PlayerService], initiator: PlayerService, target: PlayerService , is_open=True):
        fight = Fight.objects.create(
            initiator=initiator.player,
            target=target.player,
            is_open=is_open,
        )
        fight.side_a_participants.add(initiator.player, *[p.player for p in participants_a])
        fight.side_b_participants.add(target.player, *[p.player for p in participants_b])
        for p in participants_a + participants_b + [initiator, target]:
            p.player.fight = fight
            p.player.save()
        return cls(fight)

    def __init__(self, fight: Fight):
        self.fight = fight

    def start(self):
        self.fight.current_turn = self.fight.turns.create(
            fight=self.fight,
        )
        self.fight.save()

    def leave(self, player_service):
        self.fight.side_a_participants.remove(player_service.player)
        self.fight.side_b_participants.remove(player_service.player)

        if not self.fight.side_a_participants.exists() or not self.fight.side_b_participants.exists():
            self.end()

    def end(self):
        self.fight.is_ended = True
        self.fight.save()
        return self.fight

    def join(self, player_service, side):

        if self.fight.is_ended:
            raise GameLogicException('Fight is already ended')
        if not self.fight.is_open:
            raise GameLogicException('Fight is not open')

        if side == 'a':  # TODO: make enum with sides Attacker and Defender
            self.fight.side_a_participants.add(player_service.player)
        else:
            self.fight.side_b_participants.add(player_service.player)
        self.fight.save()

