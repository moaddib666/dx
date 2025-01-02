from apps.action.models import CharacterAction
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype


class UseItemActionService(CharacterActionServicePrototype):

    def __init__(self, use_skill_service: "CharacterActionServicePrototype"):
        self.use_skill_service = use_skill_service

    def perform(self, action: CharacterAction):
        self.use_skill_service.perform(action)
        action.item.charges_left -= 1
        action.item.save(
            update_fields=["charges_left", "updated_at"]
        )

    def check(self, action: CharacterAction):
        if action.item.charges_left < 1:
            raise GameException("Item has no charges left")
        self.use_skill_service.check(action)

    def check_acceptance(self, action: CharacterAction):
        """
        Check if the action is possible to accept
        1. Action initiator has the item
        2. Item is usable
        3. Item is not on cooldown
        4. Item has enough charges
        """
        initiator = action.initiator
        item = action.item
        if not initiator.equipped_items.filter(world_item=item).exists():
            raise GameException("Item not equipped or not owned by the character")
        if item.charges_left < 1:
            raise GameException("Item has no charges left")
        if item.item.skill is None:
            raise GameException("Item is not usable")

    def accept(self, action: CharacterAction):
        item_skill = action.item.item.skill
        action.skill = item_skill
        action.save()
        self.use_skill_service.accept(action)
