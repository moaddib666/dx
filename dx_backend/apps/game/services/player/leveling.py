import logging

from apps.player.models import Player


class LevelingService:
    logger = logging.getLogger("game.services.player.leveling")

    def __init__(self, player: Player):
        self.player = player

    def add_experience(self, amount):
        logging.info(f"Adding {amount} experience to {self.player.pk}")
        self.player.experience += amount
        self.player.save()
        self.check_level_up()

    def check_level_up(self):
        logging.debug(f"Checking if player {self.player.pk} is leveling up current experience: {self.player.experience} needed: {self.player.rank.next_rank.experience_needed}")
        if self.player.experience >= self.player.rank.next_rank.experience_needed:
            self.level_up()
        else:
            logging.debug(f"Player {self.player.pk} is not leveling up yet")

    def level_up(self):
        logging.info(f"Player {self.player.pk} is leveling up")
        self.player.rank = self.player.rank.next_rank
        self.player.save()
        self.notify_level_up()
        # TODO: Add stats points
        # TODO: Add skill points
        # TODO: Add school points
        # TODO: Add money

    def notify_level_up(self):
        # self.player.notify({
        #     'type': 'level_up',
        #     'data': {
        #         'level': self.player.rank.level,
        #     }
        # })
        pass
