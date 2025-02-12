import logging

from apps.items.models import CharacterItem, WorldItem


class CharacterItemsService:
    logger = logging.getLogger("game.services.character.items")

    def __init__(self, character):
        self.character = character
        self.logger.info(f"Initialized CharacterItemsService for character: {character.id} - {character.name}")

    def get_visible_items(self) -> [CharacterItem]:
        visible_items = self.character.equipped_items.all()
        self.logger.debug(
            f"Fetched visible items for character {self.character.id}: {[item.pk for item in visible_items]}"
        )
        return visible_items

    def remove_item(self, item: CharacterItem) -> WorldItem:
        self.logger.info(
            f"Removing item {item.pk} ({item.world_item}) from character {self.character.id}"
        )
        self.character.equipped_items.filter(pk=item.pk).delete()
        self.logger.debug(
            f"Item {item.pk} removed. Returning its WorldItem {item.world_item.id}."
        )
        return item.world_item

    def add_item(self, item: WorldItem):
        self.logger.info(
            f"Adding WorldItem {item.id} ({item}) to character {self.character.id}"
        )
        self.character.equipped_items.create(world_item=item)
        self.logger.debug(f"WorldItem {item.id} added to character {self.character.id}.")

    def drop_world_item(self, world_item: WorldItem) -> WorldItem:
        self.logger.info(
            f"Dropping WorldItem {world_item.id} ({world_item}) from character {self.character.id}"
        )
        character_item = self.character.equipped_items.get(world_item=world_item)
        character_item.delete()
        self.logger.debug(
            f"WorldItem {world_item.id} dropped from character {self.character.id}."
        )
        return world_item

    def drop_item(self, item: CharacterItem) -> WorldItem:
        self.logger.info(
            f"Dropping item {item.pk} ({item.world_item}) from character {self.character.id}"
        )
        world_item = self.remove_item(item)
        world_item.position = self.character.position
        world_item.save(update_fields=["position"])
        self.logger.debug(
            f"Item {item.pk} dropped at position {self.character.position}. Updated WorldItem {world_item.id}."
        )
        return world_item

    def pick_item(self, item: WorldItem):
        self.logger.info(
            f"Picking up WorldItem {item.id} ({item}) for character {self.character.id}"
        )
        self.add_item(item)
        item.position = None
        item.save(update_fields=["position"])
        self.logger.debug(
            f"WorldItem {item.id} picked up by character {self.character.id}. Position set to None."
        )


class CharacterItemsServiceFactory:

    def from_character(self, character):
        return CharacterItemsService(character)


default_items_svc_factory = CharacterItemsServiceFactory()
