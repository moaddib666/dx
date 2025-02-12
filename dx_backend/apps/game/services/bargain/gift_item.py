import logging

from django.db.models import Q

from apps.bargain.models import Bargain
from apps.character.models import Character
from apps.game.services.character.character_items import default_items_svc_factory
from apps.items.models import WorldItem


class BargainService:
    logger = logging.getLogger("game.services.bargain")

    def __init__(self, bargain: Bargain, item_svc_factory=default_items_svc_factory):
        self.bargain = bargain
        self.item_svc_factory = item_svc_factory

    @property
    def model(self) -> Bargain:
        return self.bargain

    def is_immutable(self) -> bool:
        return self.bargain.completed or self.bargain.cancelled or self.bargain.side_a_accepted and self.bargain.side_b_accepted

    def cancel(self) -> Bargain:
        self.bargain.cancelled = True
        self.bargain.save(update_fields=['cancelled'])
        return self.bargain

    def accept(self, character: Character) -> Bargain:
        if self.bargain.completed:
            raise ValueError('Bargain is already completed')
        if character == self.bargain.side_a:
            self.bargain.side_a_accepted = True
        elif character == self.bargain.side_b:
            self.bargain.side_b_accepted = True
        else:
            raise ValueError('Character is not in the bargain')

        if self.bargain.side_a_accepted and self.bargain.side_b_accepted:
            self.bargain.completed = True
        self.bargain.save(
            update_fields=['completed', 'side_a_accepted', 'side_b_accepted']
        )
        if self.bargain.completed:
            return self.dial()
        return self.bargain

    def is_duplicate(self, character: Character, item: "WorldItem") -> bool:
        """
        Check if the item is already in the bargain by the character
        """
        if character == self.bargain.side_a:
            return self.bargain.side_a_offered_items.filter(item=item).exists()
        elif character == self.bargain.side_b:
            return self.bargain.side_b_offered_items.filter(item=item).exists()
        else:
            raise ValueError('Character is not in the bargain')

    def add_item(self, character: Character, item: "WorldItem") -> Bargain:
        if self.is_immutable():
            raise ValueError('Bargain is immutable')
        if self.is_duplicate(character, item):
            raise ValueError('Item is already in the bargain')
        if character == self.bargain.side_a:
            self.bargain.side_a_offered_items.create(item=item, bargain=self.bargain)
        elif character == self.bargain.side_b:
            self.bargain.side_b_offered_items.create(item=item, bargain=self.bargain)
        else:
            raise ValueError('Character is not in the bargain')
        return self.bargain

    def remove_item(self, character: Character, item: "WorldItem") -> Bargain:
        if self.is_immutable():
            raise ValueError('Bargain is immutable')
        if character == self.bargain.side_a:
            self.bargain.side_a_offered_items.filter(item=item).delete()
        elif character == self.bargain.side_b:
            self.bargain.side_b_offered_items.filter(item=item).delete()
        else:
            raise ValueError('Character is not in the bargain')
        return self.bargain

    def _exchange_item(self, character: Character, target_character: Character, world_item: WorldItem):
        try:
            world_item = self.item_svc_factory.from_character(character).drop_world_item(world_item)
            self.item_svc_factory.from_character(target_character).pick_item(world_item)
        except Exception as e:
            self.logger.error(f"Error dialing bargain {self.bargain.id}: {e}")
        else:
            self.logger.debug(f"Item {world_item.id} exchanged between {character.id} and {target_character.id}")

    def dial(self) -> Bargain:
        if self.bargain.side_a_accepted and self.bargain.side_b_accepted:
            for offered_item in self.bargain.side_a_offered_items.all():
                self._exchange_item(self.bargain.side_a, self.bargain.side_b, offered_item.item)
            for offered_item in self.bargain.side_b_offered_items.all():
                self._exchange_item(self.bargain.side_b, self.bargain.side_a, offered_item.item)
        return self.bargain


class GiftItemService(BargainService):

    def dial(self) -> Bargain:
        for offered_item in self.bargain.side_a_offered_items.all():
            self._exchange_item(self.bargain.side_a, self.bargain.side_b, offered_item.item)
        return self.bargain


class BargainServiceFactory:

    def from_bargain(self, bargain: Bargain):
        return BargainService(bargain)

    def gift_item(self, bargain: Bargain):
        return GiftItemService(bargain)

    def from_character(self, character: Character, target_character: Character):
        return self.from_bargain(Bargain.objects.create(side_a=character, side_b=target_character))

    def gift_item_from_character(self, character: Character, target_character: Character):
        # close old bargains
        bargains = Bargain.objects.filter(
            Q(side_a=character) | Q(side_b=character),
            completed=False,
            cancelled=False
        )
        for bargain in bargains:
            self.from_bargain(bargain).cancel()
        return self.gift_item(Bargain.objects.create(side_a=character, side_b=target_character, side_b_accepted=True))


default_bargain_svc_factory = BargainServiceFactory()
