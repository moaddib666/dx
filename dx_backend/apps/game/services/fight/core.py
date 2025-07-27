import typing as t

from apps.fight.models import Fight

if t.TYPE_CHECKING:
    from apps.action.models import Cycle
    from apps.game.services.notifier.base import BaseNotifier
    from apps.character.models import Character


# TODO:
#   1. Refactor this move each class to its own file.
#   2. Implement FightDetector, FightAutoJoiner, FightAuthLeaver, FightPendingJoiner, FindCloser classes.
#   3. Add the Events and their data to the notifier.
#   4. Ensure all made by services are logged via logging.getLogger("game.services.fight.{className}") loggers.
#   5. Make sure all implemented changes compatible with the current Models and Services architecture.
#   6. Make sure we could integrate this services with the out main game loop
#       - apps.game.services.action.player.ManualCharacterActionPlayerService.prepare
#       - apps.game.services.action.player.ManualCharacterActionPlayerService.post

class FightFactory:
    model: t.Type[Fight]

    def create_fight(self, cycle: "Cycle", attacker: "Character", defender: "Character") -> Fight:
        """
        Creates a new fight instance with the given parameters.

        :param cycle: The current cycle in which the fight is happening.
        :param attacker: The character who initiated the fight.
        :param defender: The character who is being attacked.
        :return: A new Fight instance.
        """
        return self.model.objects.create(cycle=cycle, attacker=attacker, defender=defender)


class FightDetector:
    notifier: "BaseNotifier"
    cycle: "Cycle"
    """
    Detects the patters of Actions that starts the fight.

    1. Accepts current Cycle.
    2. Check all performed actions been done in the previous Cycle, exclude actions that are already in a fight.
    3. Detects if there are any `Aggressive` actions made and if so, creates a Fight object.
    4. The character who made the Aggressive action is assigned as an attacker, and the target of that action is assigned as a defender.
    5. Emits the FightStarted event to all characters in the position of the fight.
    """


class FightAutoJoiner:
    notifier: "BaseNotifier"
    """
    Detects the active fights and it's positions, find if there are any characters in the same position and not in the fight and adds them to the fight.
    
    1. Finds all active fights in the current Cycle.
    2. For each fight, finds all characters in the same position that are not in the fight.
    3. For each character found, adds them to the fight as pending joiners.
    4. Emmit the CharacterPendingJoinFight event to the all characters in that position.
    5. Emits the PendingJoinFight event to the character who joined the fight.
    """


class FightAuthLeaver:
    """
    Detach characters from fights that are not active anymore, or if characters change their position from the fight position.
    
    1. Find all characters in the fight.
    2. For each character, check if the fight is still active or if the character has changed their position.
    3. If the fight is not active or the character has changed their position, remove the character from the fight.
    4. Emit the CharacterLeaveFight event to the character who left the fight.
    5. Emit the LeftFight event to the character who left the fight.
    """


class FightPendingJoiner:
    notifier: "BaseNotifier"
    """
    Handles the pending joiners in the fight.
    
    1. Find all characters in the fight that are pending to join.
    2. Check that a fight is still open and could be joined.
    3. Remove characters from the pending joiners list
    4. Emit the CharacterJoinFight event to the character in the location of the fight.
    5. Emit the JoinedFight event to the character who joined the fight.
    """


class FindCloser:
    notifier: "BaseNotifier"
    """
    Detects the find is ended by inspecting last cycle actions, close the fight emit events and remove all characters from the fight.

    1. Find all fight active participants in the current Cycle.
    2. Exclude characters that do not have health. 
    3. If nobody left in the fight, close the fight.
    4. Check previous Cycle actions if no actions were made in the previous Cycle, close the fight.
    5. Emit the FightEnded event to all characters in the position.
    6. Remove all characters from the fight.
    """
