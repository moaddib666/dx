import logging

from apps.character.models import Character


class LevelingService:
    logger = logging.getLogger("game.services.character.leveling")

    def __init__(self, character: Character):
        self.character = character

    def add_experience(self, amount):
        logging.info(f"Adding {amount} experience to {self.character.pk}")
        self.character.experience += amount
        self.character.save()
        self.check_level_up()

    def check_level_up(self):
        logging.debug(f"Checking if character {self.character.pk} is leveling up current experience: {self.character.experience} needed: {self.character.rank.next_rank.experience_needed}")
        if self.character.experience >= self.character.rank.next_rank.experience_needed:
            self.level_up()
        else:
            logging.debug(f"Character {self.character.pk} is not leveling up yet")

    def level_up(self):
        logging.info(f"Character {self.character.pk} is leveling up")
        self.character.rank = self.character.rank.next_rank
        self.character.save()
        self.notify_level_up()
        # TODO: Add stats points
        # TODO: Add skill points
        # TODO: Add school points
        # TODO: Add money

    def notify_level_up(self):
        # self.character.notify({
        #     'type': 'level_up',
        #     'data': {
        #         'level': self.character.rank.level,
        #     }
        # })
        pass
