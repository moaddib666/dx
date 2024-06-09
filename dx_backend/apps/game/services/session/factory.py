from django.db import transaction
from apps.player.models import Character
from apps.game.models import Session


class GameSessionFactory:

    def __init__(self, client):
        self.client = client

    @transaction.atomic
    def create_session(self, player: Character) -> Session:
        session = Session.objects.create(
            player=player,
            client=self.client,
        )
        return session
