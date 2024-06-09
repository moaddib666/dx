from django.db import transaction
from apps.player.models import Player
from apps.game.models import Session


class GameSessionFactory:

    def __init__(self, client):
        self.client = client

    @transaction.atomic
    def create_session(self, player: Player) -> Session:
        session = Session.objects.create(
            player=player,
            client=self.client,
        )
        return session
