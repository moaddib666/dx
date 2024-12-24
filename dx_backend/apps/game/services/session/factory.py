from django.db import transaction
from apps.character.models import Character
from apps.game.models import Session


class GameSessionFactory:

    def __init__(self, client):
        self.client = client

    @transaction.atomic
    def create_session(self, character: Character) -> Session:
        session = Session.objects.create(
            character=character,
            client=self.client,
        )
        return session
