import typing as t

from apps.character.models import Character

if t.TYPE_CHECKING:
    from apps.core.models import PositionConnectionRequirement, PositionConnectionConfig
    from apps.world.models import PositionConnection
    from apps.game.services.character.core import CharacterService


class PositionConnectionService:
    """
    Service to check if a position is accessible.
    """

    def __init__(self, connection: "PositionConnection"):
        self.connection = connection
        self.connection_config = self.parse_connection_config(connection.config)

    def parse_connection_config(self, config: dict) -> "PositionConnectionConfig | None":
        """
        Parse the connection configuration and set it to the service.
        """
        return PositionConnectionConfig(**config) if config else None

    def is_accessible(self, character: "CharacterService") -> bool:
        """
        Check if the position connection is accessible for the given character.
        """
        default = all(
            (
                self.connection.is_active,
                not self.connection.locked,
                self.connection.is_public,
            )
        )
        if not self.connection_config:
            return default
        if default:
            return True
        return all(
            (
                self.condition_evaluator(character, req)
                for req in self.connection_config.requirements
            )
        )

    def condition_evaluator(self, character: "CharacterService", req: "PositionConnectionRequirement") -> bool:
        """
        Evaluate the condition for the position connection requirement.
        """
        return all(
            (
                character.has_skill(req.skill_id) if req.skill_id else True,
                character.has_item(req.item_id) if req.item_id else True,
                character.model.position.gameobject_set.instance_of(Character).filter(
                    campaign=character.model.campaign,
                    pk=req.character_id,
                ).exist() if req.character_id else True,
            )
        )
