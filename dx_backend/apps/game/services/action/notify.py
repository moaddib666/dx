import logging

from apps.action.models import CharacterAction
from apps.game.services.action.base_service import ActionResultNotifier


class ConsoleResultNotifyService(ActionResultNotifier):
    logger = logging.getLogger(__name__)

    def notify(self, action: CharacterAction, error: Exception = None):
        if error is None:
            self.logger.info(f"Action {action} performed successfully")
        else:
            self.logger.warning(f"Action {action} performed with error {error}")
