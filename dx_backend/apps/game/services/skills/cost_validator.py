import abc

from apps.game.exceptions import GameLogicException
from apps.character.models import Character
from apps.school.dto import Cost
from apps.school.models import Skill


class SpecificCostService(abc.ABC):

    point_type: str
    def __init__(self, value: int):
        self.value = value

    @abc.abstractmethod
    def validate(self, character: Character) -> bool:
        pass

    @abc.abstractmethod
    def perform_apply(self, character: Character):
        pass

    def apply(self, character: Character):
        if not self.validate(character):
            raise GameLogicException(f"Not enough {self.point_type} points")
        self.perform_apply(character)


class EnergyCostService(SpecificCostService):
    point_type = "energy"
    def validate(self, character: Character) -> bool:
        return character.current_energy_points >= self.value

    def perform_apply(self, character: Character):
        if not self.validate(character):
            raise GameLogicException("Not enough energy points")
        character.current_energy_points -= self.value
        character.save()


class HealthCostService(SpecificCostService):
    point_type = "health"
    def validate(self, character: Character) -> bool:
        return character.current_health_points >= self.value

    def perform_apply(self, character: Character):
        if not self.validate(character):
            raise GameLogicException("Not enough health points")
        character.current_health_points -= self.value
        character.save()


class ActionPointsCostService(SpecificCostService):
    point_type = "action points"
    def validate(self, character: Character) -> bool:
        return character.current_active_points >= self.value

    def perform_apply(self, character: Character):
        if not self.validate(character):
            raise GameLogicException("Not enough action points")
        character.current_active_points -= self.value
        character.save()


class SkillCostService:
    mapping = {
        Skill.CostType.ENERGY: EnergyCostService,
        Skill.CostType.HEALTH: HealthCostService,
        Skill.CostType.AP: ActionPointsCostService,
    }

    def __init__(self, skill: Skill):
        self.skill = skill

    def resolve(self, cost: Cost) -> SpecificCostService:
        return self.mapping[cost["kind"]](cost["value"])

    def validate(self, character: Character) -> bool:
        for cost in self.skill.cost:
            if not self.resolve(cost).validate(character):
                raise GameLogicException(f"Not enough {self.mapping[cost['kind']]} points")

    def apply(self, character):
        for cost in self.skill.cost:
            self.resolve(cost).apply(character)

    def get_energy_cost(self):
        for cost in self.skill.cost:
            if cost["kind"] == Skill.CostType.ENERGY:
                return cost["value"]

    def get_health_cost(self):
        for cost in self.skill.cost:
            if cost["kind"] == Skill.CostType.HEALTH:
                return cost["value"]

    def get_ap_cost(self):
        for cost in self.skill.cost:
            if cost["kind"] == Skill.CostType.AP:
                return cost["value"]