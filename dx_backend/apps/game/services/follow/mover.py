import contextlib
import logging

from django.db import models

from apps.character.models import FollowRule
from apps.game.exceptions import GameException
from apps.game.services.follow.factory import ChaseFollowFactory, get_chase_follow_factory


class WorldFollowService:
    """
    Service for managing follow actions in the game world.
    This service handles the logic for characters following or chasing other characters.
    """
    logger = logging.getLogger("game.services.world.follow")

    def __init__(self, factory: ChaseFollowFactory = None):
        self.factory = factory or get_chase_follow_factory()

    def get_follow_rules(self) -> models.QuerySet:
        """
        Get all follow rules for the current character.
        """
        return FollowRule.objects.all().select_related(
            "follower", "leader"
        ).prefetch_related(
            "follower__position", "leader__position"
        )

    def process_rules(self):
        """
        Move all followers according to their follow rules.
        This method should be called periodically to update the positions of followers.
        """
        rules = self.get_follow_rules()
        for rule in rules:
            try:
                self.process_rule(rule)
            except GameException as e:
                self.safe_delete_rule(rule)
                self.logger.error(f"Error processing follow rule {rule.id}: {e} - rule deleted.")

    def safe_delete_rule(self, rule: FollowRule):
        with contextlib.suppress(Exception):
            rule.delete()

    def process_rule(self, rule: FollowRule):
        """
        Process a single follow rule.
        This method checks if the follower should proceed and moves them accordingly.
        """
        follow_service = self.factory.from_rule(rule)
        if follow_service.should_proceed():
            follow_service.move()
        else:
            self.safe_delete_rule(rule)
