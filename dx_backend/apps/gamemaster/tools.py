from apps.core.bus import event_bus
from apps.game.services.action.accept import AccpetorFactory
from apps.game.services.action.factory import CharacterActionFactory, ManualCharacterActionPlayerServiceFactory
from apps.game.services.action.pipeline import ActionPipeline
from apps.game.services.notifier.base import BaseNotifier

ACTION_PIPELINE_TOOL = ActionPipeline(
    action_acceptor=AccpetorFactory(),
    action_factory=CharacterActionFactory(),
    cycle_player_factory=ManualCharacterActionPlayerServiceFactory,
    notifier=BaseNotifier(event_bus)
)
