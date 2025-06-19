import logging
from typing import Optional

from apps.items.models import Item, WorldItem
from apps.world.models import Position


class WorldItemFactory:
    """
    Factory for creating WorldItem instances from Item instances.
    """
    logger = logging.getLogger("game.services.items.world_item")

    @classmethod
    def create_world_item(cls, item: Item, position: Optional[Position] = None, dimension=None) -> WorldItem:
        """
        Create a WorldItem instance from an Item instance.
        
        Args:
            item: The Item instance to create a WorldItem from
            position: Optional Position instance to set for the WorldItem
            dimension: Optional Dimension instance to set for the WorldItem
            
        Returns:
            WorldItem: The created WorldItem instance
        """
        cls.logger.info(f"Creating WorldItem from Item: {item.id} - {item.name}")
        
        world_item = WorldItem.objects.create(
            item=item,
            charges_left=item.charges,
            visibility=item.visibility,
            position=position,
            dimension=dimension
        )
        
        cls.logger.debug(f"Created WorldItem: {world_item.id}")
        return world_item


# Create a default instance for easy import
default_world_item_factory = WorldItemFactory()