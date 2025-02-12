import logging

from django.apps import apps


class BargainCleanupService:
    """ Close all not finished bargains """

    bargain_model = apps.get_model('bargain', 'Bargain')
    logger = logging.getLogger("game.services.bargain")

    def __init__(self):
        self.bargains = self.bargain_model.objects.filter(completed=False, cancelled=False)

    def cleanup(self):
        count = self.bargains.count()
        if count == 0:
            return
        self.logger.info(f"Found {self.bargains.count()} not finished bargains")
        self.bargains.delete()
        self.logger.info("Bargains deleted")


bargain_cleaner = BargainCleanupService()
