import datetime
import typing as t

from django.db.models import Model

if t.TYPE_CHECKING:
    from apps.game.services.clone.base import Dependency
    from apps.game.services.clone.hook import CloneHook
    from apps.game.services.clone.clone import CloneService
    from apps.game.services.clone.rel_fix import RelationUpdater


class CloneStrategy(t.Protocol):
    cloner: "CloneService"
    fixer: "RelationUpdater"
    hook: t.Optional["CloneHook"] = None

    def clone_root_instance(self, instance: "Model") -> "Model":
        """
        Clone the root instance using the cloner and fixer.
        This method should be implemented by concrete clone strategies.
        """
        return self.cloner.clone_model(instance)

    def apply(self, instance: "Dependency", **kwargs: t.Any) -> None:
        if self.hook:
            self.hook.before_clone(instance)
        new = self.cloner.clone(instance, **kwargs)
        self.fixer.fix(new)
        if self.hook:
            self.hook.after_clone(new)


class DefaultCloneStrategy(CloneStrategy):
    """
    Default implementation of CloneStrategy that uses the provided cloner, fixer, and hook.
    """

    def __init__(self, cloner: "CloneService", fixer: "RelationUpdater", hook: t.Optional["CloneHook"] = None):
        self.cloner = cloner
        self.fixer = fixer
        self.hook = hook


class CampaignCloneStrategy(DefaultCloneStrategy):
    def clone_root_instance(self, instance: "Model") -> "Model":
        instance = super().clone_root_instance(instance)
        instance.name = f"{instance.name} (clone) [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        instance.is_active = False
        instance.is_completed = False
        return instance
