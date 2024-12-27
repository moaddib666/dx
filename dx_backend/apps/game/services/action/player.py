import typing

from django.db.models import QuerySet

from apps.action.models import Cycle
from apps.character.models import Character
from .base_service import CharacterActionPlayerServicePrototype, ActionResultNotifier
from ..character.core import CharacterService

if typing.TYPE_CHECKING:
    from .factory import CharacterActionFactory


class ManualCharacterActionPlayerService(CharacterActionPlayerServicePrototype):
    char_svc_cls = CharacterService

    def __init__(self, cycle: Cycle, factory: "CharacterActionFactory", notify_svc: "ActionResultNotifier"):
        self.cycle = cycle
        self.factory = factory
        self.notify_svc = notify_svc

    def prepare(self):
        pass

    def post(self):
        self.update_characters()

    def play(self):
        self.prepare()
        self._play()
        self.post()

    def _play(self):
        for action in self.get_actions():
            try:
                self.factory.from_action(action).perform(action)
                self.notify_svc.notify(action)
            except Exception as e:
                self.notify_svc.notify(action, e)

    def update_characters(self):
        characters = self._get_suitable_characters()
        for char in characters:
            char.refill_ap()

    def _get_suitable_characters(self) -> ["CharacterService"]:
        """
        take characters that have hp > 0 and not stunned
        :return:
        """
        qs = Character.objects.all()
        res = []
        for char in qs:
            svc = self.char_svc_cls(char)
            if svc.get_current_hp() > 0 and not svc.is_knocked_out():
                res.append(svc)
        return res

    def get_actions(self) -> QuerySet:
        return self.cycle.actions.filter(performed=False)
