import abc
import logging
import typing as t

from apps.game.services.npc.factory import NPCFactoryConfig, NPCFactory
from apps.spawner.models import NPCSpawner

if t.TYPE_CHECKING:
    from apps.action.models import Cycle
    from apps.core.models import GameObject


class SpecificSpawnerService(t.Protocol):
    @abc.abstractmethod
    def spawn(self) -> "GameObject":
        ...

    @abc.abstractmethod
    def should_spawn(self, cycle: "Cycle") -> bool:
        ...


class CoreSpawnersService:
    logger = logging.getLogger(__name__)

    def process_spawners(self, cycle: "Cycle"):
        self.process_npc_spawners(cycle)

    def process_npc_spawners(self, cycle: "Cycle"):
        npc_spawners = NPCSpawner.objects.filter(is_active=True, campaign=cycle.campaign)
        for spawner in npc_spawners:
            service = NPCSpawnerService(spawner)
            if service.should_spawn(cycle):
                npc = service.spawn()
                self.logger.info(f"Spawned NPC {npc} from spawner {spawner.id} at position {spawner.position}")
                spawner.spawned_entities.add(npc)


class NPCSpawnerService(SpecificSpawnerService):
    logger = logging.getLogger(__name__)

    def __init__(self, spawner: "NPCSpawner"):
        self.spawner = spawner
        self.factory = NPCFactory()

    def spawn(self) -> "GameObject":
        config = NPCFactoryConfig(
            template=self.spawner.character_template,
            position=self.spawner.position,
            behavior=self.spawner.character_template.behavior,
            campaign=self.spawner.campaign,
        )

        npc = self.factory.create_npc(config)
        return npc

    def should_spawn(self, cycle: "Cycle") -> bool:
        if self.spawner.spawn_limit <= self.spawner.spawned_entities.count():
            self.logger.debug(f"Spawner {self.spawner.id} reached spawn limit.")
            return False
        if self.spawner.respawn_cycles <= 0:
            self.spawner.is_active = False
            self.spawner.save(update_fields=['is_active'])
            self.logger.debug(f"Spawner {self.spawner.id} deactivated due to non-positive respawn cycles.")
            return False
        if self.spawner.next_spawn_cycle_number < cycle.number:
            self.spawner.next_spawn_cycle_number = cycle.number + self.spawner.respawn_cycles
            self.spawner.save(update_fields=['next_spawn_cycle_number'])
            return False
        if self.spawner.next_spawn_cycle_number and self.spawner.next_spawn_cycle_number >= cycle.number:
            self.logger.debug(
                f"Spawner {self.spawner.id} not ready to spawn. Next spawn cycle: {self.spawner.next_spawn_cycle_number}, current cycle: {cycle.number}.")
            return False
        self.logger.debug(f"Spawner {self.spawner.id} is ready to spawn.")
        return True
