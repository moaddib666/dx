import logging
import typing as t

from apps.action.models import CharacterAction
from apps.character.models import Character
from apps.core.models import CharacterActionType
from apps.fight.models import Fight
from apps.game.services.character.core import CharacterService
from apps.world.models import Position
from apps.action.models import Cycle

if t.TYPE_CHECKING:
    from apps.game.services.notifier.base import BaseNotifier


class FightDetector:
    """
    Detects the patterns of Actions that starts the fight.

    1. Accepts current Cycle.
    2. Check all performed actions been done in the previous Cycle, exclude actions that are already in a fight.
    3. Detects if there are any `Aggressive` actions made and if so, creates a Fight object.
    4. The character who made the Aggressive action is assigned as an attacker, and the target of that action is assigned as a defender.
    5. Emits the FightStarted event to all characters in the position of the fight.
    """

    def __init__(self, notifier: "BaseNotifier"):
        self.notifier = notifier
        self.logger = logging.getLogger("game.services.fight.FightDetector")

    AGGRESSIVE_ACTION_TYPES = {
        CharacterActionType.USE_SKILL,
        CharacterActionType.USE_ITEM,
        CharacterActionType.START_FIGHT,
    }

    def detect_fights(self, cycle: "Cycle") -> list[Fight]:
        """
        Detect and create fights based on aggressive actions in the previous cycle.
        
        Returns:
            List of newly created Fight instances
        """
        if cycle.number == 0:
            self.logger.debug("No previous cycle to check for fights")
            return []

        previous_cycle = Cycle.objects.previous(cycle.campaign)
        if not previous_cycle:
            self.logger.debug("No previous cycle found")
            return []

        aggressive_actions = self._get_aggressive_actions(previous_cycle)
        created_fights = []

        for action in aggressive_actions:
            if self._should_create_fight(action):
                fight = self._create_fight_from_action(action, cycle)
                if fight:
                    created_fights.append(fight)
                    self._emit_fight_started_event(fight)

        self.logger.info(f"Detected and created {len(created_fights)} new fights")
        return created_fights

    def _get_aggressive_actions(self, previous_cycle) -> list[CharacterAction]:
        """Get aggressive actions from the previous cycle that aren't already in fights."""
        from django.db.models import Q
        from apps.core.models import ImpactType

        # Get aggressive impact types for efficient querying
        aggressive_impact_types = [
            impact_type for impact_type in ImpactType
            if impact_type.is_aggressive()
        ]

        # Build query conditions
        base_conditions = Q(
            cycle=previous_cycle,
            performed=True,
            action_type__in=self.AGGRESSIVE_ACTION_TYPES,
            fight__isnull=True  # Not already in a fight
        )

        # Actions are aggressive if they either:
        # 1. Have aggressive impacts, OR
        # 2. Are START_FIGHT actions (always aggressive)
        aggressive_conditions = Q(
            impacts__type__in=aggressive_impact_types
        ) | Q(
            action_type=CharacterActionType.START_FIGHT
        )

        # Combine conditions and optimize query
        return list(CharacterAction.objects.filter(
            base_conditions & aggressive_conditions
        ).distinct().select_related(
            'initiator', 'position'
        ).prefetch_related(
            'targets',
            'impacts__target'
        ))

    def _is_action_aggressive(self, action: CharacterAction) -> bool:
        """
        Check CharacterAction -> ActionImpact and if ActionImpact.type is aggressive return True.
        Uses apps.core.models.ImpactType.is_aggressive()
        
        Args:
            action: CharacterAction to check for aggressiveness
            
        Returns:
            bool: True if any of the action's impacts are aggressive
        """
        from apps.core.models import ImpactType

        # Check if action has any aggressive impacts
        for impact in action.impacts.all():
            impact_type = ImpactType(impact.type)
            if impact_type.is_aggressive():
                self.logger.debug(f"Action {action.id} has aggressive impact: {impact.type}")
                return True

        # Special case: START_FIGHT actions are always aggressive
        if action.action_type == CharacterActionType.START_FIGHT:
            self.logger.debug(f"Action {action.id} is START_FIGHT type, considered aggressive")
            return True

        return False

    def _should_create_fight(self, action: CharacterAction) -> bool:
        """
        Determine if an action should create a fight.

        Args:
            action: The CharacterAction to evaluate

        Returns:
            bool: True if a fight should be created
        """
        # Check if initiator and targets are still active
        if not action.initiator.is_active:
            return False

        # Check if any targets are still active
        active_targets = action.targets.filter(is_active=True)
        if not active_targets.exists():
            return False

        # Check if there's already a fight at this position
        existing_fight = Fight.objects.filter(
            position=action.position,
            open=True
        ).first()

        if existing_fight:
            self.logger.debug(f"Fight already exists at position {action.position}")
            return False

        if not self._could_character_start_fight(action.initiator, action.position):
            self.logger.debug(f"Character {action.initiator} cannot start a fight at position {action.position}")
            return False

        first_target = active_targets.first()
        if not first_target:
            self.logger.debug(f"No active targets found for action {action.id}")
            return False
        if not self._could_character_start_fight(first_target, action.position):
            self.logger.debug(f"Target {first_target} cannot start a fight at position {action.position}")
            return False

        return True

    def _could_character_start_fight(self, character: "Character", posittion: "Position") -> bool:
        svc = CharacterService(character)
        # Check if initiator is knocked out
        if svc.is_knocked_out():
            self.logger.debug(f"Character {character} is incapacitated and cannot start a fight")
            return False
        # Check if character is at the position
        if character.position != posittion:
            self.logger.debug(f"Character {character} is not at the fight position {posittion}")
            return False
        return True

    def _create_fight_from_action(self, action: CharacterAction, cycle: "Cycle") -> t.Optional[Fight]:
        """
        Create a Fight instance from an aggressive action.

        Args:
            action: The CharacterAction that triggered the fight

        Returns:
            Fight instance or None if creation failed
        """
        try:
            # Get the first active target as defender
            defender = action.targets.filter(is_active=True).first()
            if not defender:
                self.logger.warning(f"No active defender found for action {action.id}")
                return None

            fight = Fight.objects.create(
                campaign=cycle.campaign,
                position=action.position,
                attacker=action.initiator,
                defender=defender,
                created=cycle,
                open=True
            )

            # Link the action to the fight
            action.fight = fight
            action.save()

            # Set Character.fight field for participants
            action.initiator.fight = fight
            action.initiator.save(update_fields=['fight'])

            defender.fight = fight
            defender.save(update_fields=['fight'])

            self.logger.info(f"Created fight {fight.id} between {action.initiator} and {defender}")

            # Set characters pending join
            joining_fight = [*action.targets.filter(is_active=True), action.initiator]
            for target in joining_fight:
                svc = CharacterService(target)
                svc.spend_all_ap()
                self.logger.debug(f"Spent all AP for character {target.id} in fight {fight.id}")
                fight.pending_joiners.create(
                    character=target,
                    cycle=cycle
                )
            self.logger.debug(f"Set fight field for characters {action.initiator.id} and {defender.id}")
            return fight

        except Exception as e:
            self.logger.error(f"Failed to create fight from action {action.id}: {e}")
            return None

    def _emit_fight_started_event(self, fight: Fight):
        """
        Emit a FightStarted event to all characters at the fight position.

        Args:
            fight: The Fight instance that was started
        """
        try:
            from apps.core.bus.events.fight.produced import FightStartedEvent

            event = FightStartedEvent.create_event(
                fight_id=fight.id,
                position_id=fight.position.id,
                attacker_id=fight.attacker.id,
                defender_id=fight.defender.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted FightStarted event for fight {fight.id}")

        except ImportError:
            self.logger.warning("FightStartedEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit FightStarted event for fight {fight.id}: {e}")
