import abc
import typing as t
from dataclasses import dataclass, field

from apps.character.models import Character, CharacterTemplate
from apps.core.models import BehaviorModel
from apps.world.models import Position


@dataclass
class NPCFactoryConfig:
    """Configuration for creating an NPC."""
    template: t.Optional[CharacterTemplate] = None
    template_character: t.Optional[Character] = None
    position: t.Optional[Position] = None
    name: t.Optional[str] = None
    behavior: str = BehaviorModel.PASSIVE
    rank_grade: t.Optional[int] = None
    rank_grade_rank: t.Optional[int] = None
    character_class: t.Optional[t.List[t.Tuple[str, int]]] = None
    tags: t.List[str] = field(default_factory=list)
    
    def validate(self) -> None:
        """Validate the configuration."""
        if not self.template and not self.template_character:
            raise ValueError("Either template or template_character must be provided")
        
        if self.template and self.template_character:
            raise ValueError("Only one of template or template_character should be provided")
        
        if self.rank_grade is not None and self.rank_grade_rank is None:
            raise ValueError("If rank_grade is provided, rank_grade_rank must also be provided")
        
        if self.rank_grade_rank is not None and self.rank_grade is None:
            raise ValueError("If rank_grade_rank is provided, rank_grade must also be provided")


class NPCFactoryProtocol(abc.ABC):
    """Protocol for NPC factory implementations."""
    
    @abc.abstractmethod
    def create_npc(self, config: NPCFactoryConfig) -> Character:
        """Create a new NPC based on the provided configuration."""
        pass
    
    @abc.abstractmethod
    def create_npcs(self, config: NPCFactoryConfig, count: int) -> t.List[Character]:
        """Create multiple NPCs based on the provided configuration."""
        pass