from django.core.management.base import BaseCommand, CommandError

from apps.fight.models import Fight
from apps.game.services.fight.processor import FightPlayerService
from apps.game.services.player.core import PlayerService
from apps.game.services.player.leveling import LevelingService
from apps.player.models import Player


class Command(BaseCommand):
    help = 'Manually handle fight steps'

    def handle(self, *args, **kwargs):
        current_fights = Fight.objects.filter(is_ended=False)
        for fight in current_fights:
            fight_service = FightPlayerService(fight)
            fight_service.process()
