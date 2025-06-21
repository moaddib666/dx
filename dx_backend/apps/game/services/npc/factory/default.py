import logging
import typing as t

from django.db import transaction

from apps.character.models import Character, CharacterTemplate
from apps.core.models import CharacterStats
from apps.game.services.character.character_clone import CharacterCloner
from apps.game.services.character.core import CharacterService
from apps.game.services.items.world_item import default_world_item_factory
from apps.game.services.npc.rank import NpcRankService
from apps.game.services.npc.stats import StatsApplier
from apps.skills.models import LearnedSchool
from .interface import NPCFactoryConfig, NPCFactoryProtocol
from ...character.character_items import default_items_svc_factory


class NPCFactory(NPCFactoryProtocol):
    """Implementation of the NPC factory protocol."""

    logger = logging.getLogger("services.npc.factory")

    def __init__(self):
        self.logger.info("NPCFactory initialized")

    def create_npc(self, config: NPCFactoryConfig) -> Character:
        """Create a new NPC based on the provided configuration."""
        config.validate()
        self.logger.info(f"Creating NPC with config: {config}")

        with transaction.atomic():
            # Create the base NPC
            if config.template:
                npc = self._create_from_template(config)
            else:
                npc = self._create_from_character(config)

            # Apply customizations
            self._apply_customizations(npc, config)

            # Refill stats
            CharacterService(npc).refill_all()

            self.logger.info(f"Created NPC: {npc.name} (ID: {npc.id})")
            return npc

    def create_npcs(self, config: NPCFactoryConfig, count: int) -> t.List[Character]:
        """Create multiple NPCs based on the provided configuration."""
        if count <= 0:
            raise ValueError("Count must be greater than 0")

        self.logger.info(f"Creating {count} NPCs with config: {config}")
        npcs = []

        for i in range(count):
            # Create a copy of the config to avoid modifying the original
            npc_config = NPCFactoryConfig(
                template=config.template,
                template_character=config.template_character,
                position=config.position,
                name=config.name,
                behavior=config.behavior,
                rank_grade=config.rank_grade,
                rank_grade_rank=config.rank_grade_rank,
                character_class=config.character_class,
                tags=config.tags.copy() if config.tags else []
            )

            # Generate a unique name if needed
            if npc_config.name:
                npc_config.name = f"{npc_config.name} {i + 1}"

            npc = self.create_npc(npc_config)
            npcs.append(npc)

        return npcs

    def _create_from_template(self, config: NPCFactoryConfig) -> Character:
        """Create an NPC from a CharacterTemplate."""
        self.logger.info(f"Creating NPC from template: {config.template.name}")

        # Create a new character
        npc = Character.objects.create(
            owner=None,  # NPCs don't have owners
            name=config.name or config.template.name,
            organization=config.template.organization,
            tags=list(config.template.tags).copy() if config.template.tags else [],
            path=config.template.path,
            rank=config.template.rank,
            npc=True,
            behavior=config.behavior or config.template.behavior,
            dimension=config.template.dimension,
            position=config.position,
            is_active=True
        )

        # Apply template stats
        if config.template.stats_template:
            self._apply_template_stats(npc, config.template)

        # Apply template biography
        if config.template.biography_template:
            self._apply_template_biography(npc, config.template)

        # Apply template skills
        self._apply_template_skills(npc, config.template)

        # Apply template schools
        self._apply_template_schools(npc, config.template)

        # Apply template equipment
        self._apply_template_equipment(npc, config.template)

        return npc

    def _create_from_character(self, config: NPCFactoryConfig) -> Character:
        """Create an NPC by cloning an existing character."""
        self.logger.info(f"Creating NPC from character: {config.template_character.name}")

        # Clone the character
        cloner = CharacterCloner(config.template_character)
        clones = cloner.clone(1, template="{base_name}")

        for npc in clones:
            # Update NPC-specific fields
            npc.npc = True
            npc.behavior = config.behavior
            if config.name:
                npc.name = config.name
            if config.position:
                npc.position = config.position
            if config.tags:
                npc.tags.extend(config.tags)

            npc.save()
            return npc
        raise ValueError("Failed to clone character")

    def _apply_customizations(self, npc: Character, config: NPCFactoryConfig) -> None:
        """Apply customizations to the NPC."""
        # Apply rank if specified
        if config.rank_grade is not None and config.rank_grade_rank is not None:
            self._apply_rank(npc, config.rank_grade, config.rank_grade_rank, config.character_class)

        # Apply tags if specified
        if config.tags:
            for tag in config.tags:
                if tag not in npc.tags:
                    npc.tags.append(tag)
            npc.save(update_fields=['tags'])

    def _apply_rank(self, npc: Character, grade: int, grade_rank: int,
                    character_class: t.Optional[t.List[t.Tuple[str, int]]]) -> None:
        """Apply a rank to the NPC."""
        self.logger.info(f"Applying rank {grade}-{grade_rank} to NPC: {npc.name}")

        # Use the specified character class or a default balanced class
        if character_class:
            # Convert string stat names to CharacterStats enum values
            class_priorities = [(getattr(CharacterStats, stat_name), priority)
                                for stat_name, priority in character_class]
        else:
            # Default to a balanced character class
            class_priorities = [
                (CharacterStats.PHYSICAL_STRENGTH, 3),
                (CharacterStats.SPEED, 3),
                (CharacterStats.KNOWLEDGE, 3),
                (CharacterStats.FLOW_MANIPULATION, 3),
            ]

        # Create a stats applier with the character class
        stats_applier = StatsApplier(class_priorities)

        # Create a rank service with the stats applier
        rank_service = NpcRankService(applier=stats_applier)

        # Apply the rank
        rank_service.rank_npc(npc, grade=grade, grade_rank=grade_rank)

    def _apply_template_stats(self, npc: Character, template: CharacterTemplate) -> None:
        """Apply stats from a template to an NPC."""
        self.logger.info(f"Applying template stats to NPC: {npc.name}")

        # Get all stats from the template
        stats = template.stats_template.get_all_stats()

        # Apply the stats to the NPC
        for stat_name, value in stats.items():
            stat, _ = npc.stats.get_or_create(name=stat_name)
            stat.base_value = value
            stat.save(update_fields=['base_value'])

    def _apply_template_biography(self, npc: Character, template: CharacterTemplate) -> None:
        """Apply biography from a template to an NPC."""
        self.logger.info(f"Applying template biography to NPC: {npc.name}")

        bio_template = template.biography_template

        # Create the biography
        from apps.character.models import CharacterBiography

        CharacterBiography.objects.create(
            character=npc,
            age=bio_template.generate_age(),
            gender=bio_template.generate_gender(),
            background=bio_template.generate_background(),
            appearance=bio_template.generate_appearance(),
            avatar=bio_template.avatar
        )

    def _apply_template_skills(self, npc: Character, template: CharacterTemplate) -> None:
        """Apply skills from a template to an NPC."""
        self.logger.info(f"Applying template skills to NPC: {npc.name}")

        from apps.skills.models import LearnedSkill

        # Apply skills from the template
        for skill_template in template.skill_templates.all():
            LearnedSkill.objects.create(
                character=npc,
                skill=skill_template.skill,
                is_base=skill_template.is_base
            )

    def _apply_template_schools(self, npc: Character, template: CharacterTemplate) -> None:
        """Apply schools from a template to an NPC."""
        self.logger.info(f"Applying template schools to NPC: {npc.name}")

        # Apply schools from the template
        for school_template in template.school_templates.all():
            LearnedSchool.objects.create(
                character=npc,
                school=school_template.school,
                is_base=school_template.is_base
            )

    def _apply_template_equipment(self, npc: Character, template: CharacterTemplate) -> None:
        """Apply equipment from a template to an NPC."""
        self.logger.info(f"Applying template equipment to NPC: {npc.name}")
        for equipment_template in template.equipment_templates.all():
            world_item = default_world_item_factory.create_world_item(
                item=equipment_template.item,
                position=npc.position,
                dimension=npc.dimension
            )
            char_items_factory = default_items_svc_factory.from_character(npc)
            char_items_factory.add_item(world_item)
