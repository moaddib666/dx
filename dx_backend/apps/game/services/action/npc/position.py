import logging
import typing as t

from apps.character.models import Character
from apps.character.models import Organization
from apps.core.models import BehaviorModel
from apps.game.services.action.npc.context import CharacterPositionActionContext
from apps.game.services.character.core import CharacterService
from apps.game.services.relation.service import get_character_relation_service, get_organization_relation_service
from apps.world.models import Position

logger = logging.getLogger(__name__)


class PositionCharactersBehaviorStateService:

    def __init__(self, position: "Position", orgs: dict["Organization", t.Iterable["Character"]]):
        logger.debug(f"Initializing PositionCharactersBehaviorStateService for position {position}")
        logger.debug(f"Organizations count: {len(orgs)}")
        self.position = position
        self.orgs = orgs
        self._context: dict["Character", CharacterPositionActionContext] = {}

    def get_context(self, character: "Character") -> CharacterPositionActionContext:
        logger.debug(f"Getting context for character {character}")
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
        logger.debug("Starting prepare() method")

        # Phase 1: Process organization-level relations
        logger.debug("Phase 1: Processing organization-level relations")
        for org, characters in self.orgs.items():
            logger.debug(f"Processing organization {org}")
            org_relation = get_organization_relation_service(org)
            for target_org in self.orgs:
                if org == target_org:
                    continue
                logger.debug(f"Checking relation from {org} to {target_org}")
                behavior = org_relation.get_relation_to(target_org)
                logger.debug(f"Organization relation behavior: {behavior}")
                if behavior == BehaviorModel.AGGRESSIVE:
                    logger.debug(f"Making {org} members aggressive to {target_org} members")
                    self._make_org_members_aggressive(org, target_org)
                elif behavior == BehaviorModel.FRIENDLY:
                    logger.debug(f"Making {org} members friendly to {target_org} members")
                    self._make_org_members_friendly(org, target_org)

            # Phase 2: Process character-level overrides
            logger.debug(f"Phase 2: Processing character-level overrides for {org}")
            for character in characters:
                logger.debug(f"Processing character {character}")
                char_service = CharacterService(character)
                char_relation_svc = get_character_relation_service(char_service)
                for target_org, target_characters in self.orgs.items():
                    if org == target_org:
                        continue
                    logger.debug(f"Checking {character} relations to {target_org} members")
                    for target_character in target_characters:
                        target_service = CharacterService(target_character)
                        behavior = char_relation_svc.get_relation_to(target_service)
                        logger.debug(f"Character relation behavior from {character} to {target_character}: {behavior}")
                        if behavior == BehaviorModel.AGGRESSIVE:
                            logger.debug(
                                f"Character {character} has aggressive relation, making all {org} members aggressive to {target_org}")
                            self._make_org_members_aggressive(org, target_org)
                            break
                        elif behavior == BehaviorModel.FRIENDLY:
                            logger.debug(
                                f"Character {character} has friendly relation, making all {org} members friendly to {target_org}")
                            self._make_org_members_friendly(org, target_org)
                            break

        # Phase 3: Set up individual character contexts
        logger.debug("Phase 3: Setting up individual character contexts")
        for org, characters in self.orgs.items():
            logger.debug(f"Setting up contexts for {org} characters")
            for character in characters:
                logger.debug(f"Setting up context for character {character}")
                context = self.get_context(character)
                for target_org, target_characters in self.orgs.items():
                    for target_character in target_characters:
                        if org == target_org:
                            logger.debug(f"Same organization, making {character} friendly to {target_character}")
                            self._make_friendly(character, target_character)
                            continue
                        target_service = CharacterService(target_character)
                        behavior = get_character_relation_service(context.character).get_relation_to(target_service)
                        logger.debug(f"Final relation from {character} to {target_character}: {behavior}")
                        if behavior == BehaviorModel.AGGRESSIVE:
                            logger.debug(f"Adding {target_character} as enemy to {character}")
                            context.add_enemy(target_service)
                        elif behavior == BehaviorModel.FRIENDLY:
                            logger.debug(f"Adding {target_character} as friend to {character}")
                            context.add_friend(target_service)
                        else:
                            logger.debug(f"Adding {target_character} as neutral to {character}")
                            context.add_neutral(target_service)

        logger.debug("Completed prepare() method")

    def _make_org_members_aggressive(self, org: "Organization", target_org: "Organization"):
        logger.debug(f"Making all members of {org} aggressive to all members of {target_org}")
        for character in self.orgs[org]:
            for target_character in self.orgs[target_org]:
                logger.debug(f"Making {character} aggressive to {target_character}")
                self._make_aggressive(character, target_character)

    def _make_org_members_friendly(self, org: "Organization", target_org: "Organization"):
        logger.debug(f"Making all members of {org} friendly to all members of {target_org}")
        for character in self.orgs[org]:
            for target_character in self.orgs[target_org]:
                logger.debug(f"Making {character} friendly to {target_character}")
                self._make_friendly(character, target_character)

    def _make_aggressive(self, character: "Character", target_character: "Character"):
        logger.debug(f"Making {character} aggressive to {target_character}")
        source = CharacterService(character)
        target = CharacterService(target_character)
        rel_service = get_character_relation_service(source)
        rel_service.become_aggressive_to(target)
        context = self.get_context(character)
        context.add_enemy(target)
        logger.debug(f"Successfully made {character} aggressive to {target_character}")

    def _make_friendly(self, character: "Character", target_character: "Character"):
        logger.debug(f"Making {character} friendly to {target_character}")
        source = CharacterService(character)
        target = CharacterService(target_character)
        rel_service = get_character_relation_service(source)
        context = self.get_context(character)
        if rel_service.get_relation_to(target) == BehaviorModel.AGGRESSIVE:
            logger.debug(f"Character {character} is already aggressive to {target_character}, adding as enemy instead")
            context.add_enemy(target)
            return
        rel_service.become_friendly_to(target)
        context.add_friend(target)
        logger.debug(f"Successfully made {character} friendly to {target_character}")
