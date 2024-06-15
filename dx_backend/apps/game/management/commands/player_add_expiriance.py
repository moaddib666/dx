from django.core.management.base import BaseCommand, CommandError
from apps.game.services.player.core import PlayerService
from apps.game.services.player.leveling import LevelingService
from apps.player.models import Player


class Command(BaseCommand):
    help = 'Add experience to a player'

    def add_arguments(self, parser):
        parser.add_argument('player_id', type=str, help='The ID of the player to add experience to')
        parser.add_argument('experience', type=int, help='The amount of experience to add')

    def handle(self, *args, **kwargs):
        player_id = kwargs['player_id']
        experience = kwargs['experience']

        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist as e:
            raise CommandError('Player with ID "%s" does not exist' % player_id) from e

        player_service = PlayerService(player)
        leveling_service = LevelingService(player)
        try:
            leveling_service.add_experience(experience)
        except Exception as e:
            raise CommandError('Failed to add experience to player "%s": %s' % (player_id, e)) from e
        self.stdout.write(
            self.style.SUCCESS('Successfully added %s experience to player "%s"' % (experience, player_id)))
