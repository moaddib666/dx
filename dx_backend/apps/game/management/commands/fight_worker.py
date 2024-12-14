import time

from django.core.management.base import BaseCommand, CommandError

from apps.fight.models import Fight
from apps.game.services.fight.fight import FightService


class Command(BaseCommand):
    help = 'Manually handle fight steps'

    def handle(self, *args, **kwargs):
        self.loop()

    def check_and_process(self):
        current_fights = Fight.objects.filter(is_ended=False).select_related('current_turn')
        for fight in current_fights:
            fight_service = FightService(fight)
            fight_service.process()

    def loop(self):
        while True:
            time.sleep(1)
            self.check_and_process()
