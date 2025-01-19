import typing as t

from apps.core.models import AttributeType
from apps.game.exceptions import GameException

T_COST = t.TypedDict("T_COST", {
    "kind": AttributeType,
    "value": int,
})

if t.TYPE_CHECKING:
    from apps.game.services.character.core import CharacterService

class CostService:

    def __init__(self, cost: list[T_COST]):
        self._cost_map = {cost_item["kind"]: cost_item["value"] for cost_item in cost}

    def get_cost(self, kind: AttributeType) -> int:
        return self._cost_map.get(kind, 0)

    def get_ap_cost(self) -> int:
        return self.get_cost(AttributeType.ACTION_POINTS)

    def get_hp_cost(self) -> int:
        return self.get_cost(AttributeType.HEALTH)

    def get_ep_cost(self) -> int:
        return self.get_cost(AttributeType.ENERGY)


class AnyCostService:

    def __init__(self, cost_service_cls: type[CostService]):
        self._cost_service = cost_service_cls

    def validate(self, cost: list[T_COST], character_svc: "CharacterService"):
        for cost_item in cost:
            if character_svc.get_attribute_value(cost_item["kind"]) < cost_item["value"]:
                raise GameException(f"Not enough {cost_item['kind']} to perform the action")

    def spend(self, cost: list[T_COST], character_svc: "CharacterService"):
        for cost_item in cost:
            character_svc.spend_attribute(cost_item["kind"], cost_item["value"])


DefaultCostService = AnyCostService(cost_service_cls=CostService)
