import typing as t
from dataclasses import dataclass

from apps.character.models import Character
from apps.character.models import Organization
from apps.core.models import BehaviorModel
from apps.game.services.character.core import CharacterService
from apps.game.services.relation.service import get_character_relation_service, get_organization_relation_service
from apps.world.models import Position


@dataclass
class CharacterPositionActionContext:
    character: CharacterService
    friends: t.Set[CharacterService]
    enemies: t.Set[CharacterService]
    neutral: t.Set[CharacterService]

    def add_friend(self, friend: CharacterService):
        if friend in self.enemies:
            return
        if friend in self.neutral:
            self.neutral.remove(friend)
        if friend not in self.friends:
            self.friends.add(friend)

    def add_enemy(self, enemy: CharacterService):
        if enemy not in self.enemies:
            self.enemies.add(enemy)
        if enemy in self.friends:
            self.friends.remove(enemy)
        if enemy in self.neutral:
            self.neutral.remove(enemy)

    def add_neutral(self, neutral: CharacterService):
        if neutral in self.enemies:
            return
        if neutral in self.friends:
            return
        if neutral not in self.neutral:
            self.neutral.add(neutral)


class PositionCharactersBehaviorStateService:

    def __init__(self, position: "Position", orgs: dict["Organization", t.Iterable["Character"]]):
        self.position = position
        self.orgs = orgs
        self._context: dict["Character", CharacterPositionActionContext] = {}

    def get_context(self, character: "Character") -> CharacterPositionActionContext:
        return self._context.setdefault(character, CharacterPositionActionContext(
            character=CharacterService(character),
            friends=set(),
            enemies=set(),
            neutral=set(),
        ))

    def prepare(self):
        """
        Prepare the service by setting up the necessary state or data.
        This can include initializing attributes, loading data, etc.
        """

        for org, characters in self.orgs.items():
            org_relation = get_organization_relation_service(org)
            for target_org in self.orgs:
                if org == target_org:
                    continue
                behavior = org_relation.get_relation_to(target_org)
                if behavior == BehaviorModel.AGGRESSIVE:
                    self._make_org_members_aggressive(org, target_org)
                elif behavior == BehaviorModel.FRIENDLY:
                    self._make_org_members_friendly(org, target_org)

            for character in characters:
                char_service = CharacterService(character)
                char_relation_svc = get_character_relation_service(char_service)
                for target_org, target_characters in self.orgs.items():
                    if org == target_org:
                        continue
                    for target_character in target_characters:
                        target_service = CharacterService(target_character)
                        behavior = char_relation_svc.get_relation_to(target_service)
                        if behavior == BehaviorModel.AGGRESSIVE:
                            self._make_org_members_aggressive(org, target_org)
                            break
                        elif behavior == BehaviorModel.FRIENDLY:
                            self._make_org_members_friendly(org, target_org)
                            break

        for org, characters in self.orgs.items():
            for character in characters:
                context = self.get_context(character)
                for target_org, target_characters in self.orgs.items():
                    for target_character in target_characters:
                        if org == target_org:
                            self._make_friendly(character, target_character)
                            continue
                        target_service = CharacterService(target_character)
                        behavior = get_character_relation_service(context.character).get_relation_to(target_service)
                        if behavior == BehaviorModel.AGGRESSIVE:
                            context.add_enemy(target_service)
                        elif behavior == BehaviorModel.FRIENDLY:
                            context.add_friend(target_service)
                        else:
                            context.add_neutral(target_service)

    def _make_org_members_aggressive(self, org: "Organization", target_org: "Organization"):
        for character in self.orgs[org]:
            for target_character in self.orgs[target_org]:
                self._make_aggressive(character, target_character)

    def _make_org_members_friendly(self, org: "Organization", target_org: "Organization"):
        for character in self.orgs[org]:
            for target_character in self.orgs[target_org]:
                self._make_friendly(character, target_character)

    def _make_aggressive(self, character: "Character", target_character: "Character"):
        source = CharacterService(character)
        target = CharacterService(target_character)
        rel_service = get_character_relation_service(source)
        rel_service.become_aggressive_to(target)
        context = self.get_context(character)
        context.add_enemy(target)

    def _make_friendly(self, character: "Character", target_character: "Character"):
        source = CharacterService(character)
        target = CharacterService(target_character)
        rel_service = get_character_relation_service(source)
        context = self.get_context(character)
        if rel_service.get_relation_to(target) == BehaviorModel.AGGRESSIVE:
            context.add_enemy(target)
            return
        rel_service.become_friendly_to(target)
        context.add_friend(target)
