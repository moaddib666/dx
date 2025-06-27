import logging
import typing as t

if t.TYPE_CHECKING:
    from apps.game.services.clone.base import Dependency

logger = logging.getLogger("apps.game.services.clone")


class HookError(Exception):
    """
    Exception raised when a hook fails to execute properly.
    """

    def __init__(self, message, instance: "Dependency"):
        super().__init__(message)
        self.instance = instance


class CloneHook(t.Protocol):
    """
    Protocol for clone hooks that can be executed during the cloning process.
    """

    def before_clone(self, instance: "Dependency") -> None:
        """
        Hook to be executed before cloning an instance.
        """
        pass

    def after_clone(self, instance: "Dependency") -> None:
        """
        Hook to be executed after cloning an instance.
        """
        pass


class SaveCloneHook(CloneHook):
    """
    A hook that saves the cloned instance after cloning.
    """

    def before_clone(self, instance: "Dependency") -> None:
        """
        Before cloning, we can perform any necessary setup.
        """
        logger.debug("Preparing to clone instance: %s", instance)

    def after_clone(self, instance: "Dependency") -> None:
        """
        After cloning, save the cloned instance.
        """
        logger.debug("Saving cloned instance: %s", instance)
        try:
            # due to 1-1 relations, we need to save both source and target
            # FIXME: proper set reversy for 1-1 relations to relay on it
            if isinstance(instance.target, instance.field.model):
                instance.source.save()
                instance.target.save()
            elif isinstance(instance.source, instance.field.model):
                instance.target.save()
                instance.source.save()
        except Exception as err:
            logger.exception("Failed to save cloned instance: %s", instance)
            raise HookError(
                f"Failed to save cloned: {instance}",
                instance
            ) from err
