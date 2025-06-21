import typing as t

if t.TYPE_CHECKING:
    from apps.game.services.action.accept import AccpetorFactory
    from apps.game.services.action.factory import CharacterActionFactory, ManualCharacterActionPlayerServiceFactory
    from apps.game.services.notifier.base import BaseNotifier
    from apps.action.models import CharacterAction


class ActionPipeline:
    """
    ActionPipeline is a class that manages the execution of actions in a game.
    It allows for the addition of actions to a queue and processes them sequentially.
    """
    notifier: "BaseNotifier"
    action_factory: "CharacterActionFactory"
    action_acceptor: "AccpetorFactory"
    cycle_player_factory: "ManualCharacterActionPlayerServiceFactory"

    def __init__(self,
                 action_acceptor: "AccpetorFactory",
                 action_factory: "CharacterActionFactory",
                 cycle_player_factory: "ManualCharacterActionPlayerServiceFactory",
                 notifier: "BaseNotifier"):
        self.actions = []
        self.action_acceptor = action_acceptor
        self.action_factory = action_factory
        self.cycle_player_factory = cycle_player_factory
        self.notifier = notifier

    def chain(self, action: "CharacterAction") -> "ActionPipeline":
        """
        Add an action to the pipeline.

        Args:
            action: The action to be added to the pipeline.
        """
        self.actions.append(action)
        return self

    def execute(self):
        """
        Execute all actions in the pipeline sequentially.
        """
        for action in self.actions:
            acceptor = self.action_acceptor.create(action, self.action_factory, self.notifier)
            acceptor.accept()
            if action.immediate:
                svc = self.cycle_player_factory(cycle=action.cycle, factory=self.action_factory)
                svc.apply_single_action(action=action)
        self.actions.clear()
