import logging
import typing as t

if t.TYPE_CHECKING:
    from apps.game.services.clone.base import Dependency

logger = logging.getLogger("apps.game.services.clone")


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
        instance.source.save()
        instance.target.save()
