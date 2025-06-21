import logging
import typing as t

from django.db import transaction

from apps.character.models import Character, CharacterTemplate, CharacterStatsTemplate, CharacterStatTemplate, CharacterBiographyTemplate, CharacterSchoolTemplate, CharacterModifierTemplate, CharacterEquipmentTemplate, CharacterSkillTemplate, CharacterBiography
from apps.character.models.player import StatModifier
from apps.core.models import CharacterStats, CharacterBio
from apps.game.services.character.character_clone import CharacterCloner
from apps.game.services.character.core import CharacterService
from apps.game.services.items.world_item import default_world_item_factory
from apps.game.services.npc.rank import NpcRankService
from apps.game.services.npc.stats import StatsApplier
from apps.skills.models import LearnedSchool, LearnedSkill
from apps.items.models import CharacterItem
from .interface import NPCFactoryConfig, NPCFactoryProtocol
from ...character.character_items import default_items_svc_factory


class NPCFactory(NPCFactoryProtocol):
    """Implementation of the NPC factory protocol."""

    logger = logging.getLogger("services.npc.factory")

    def __init__(self):
        self.logger.info("NPCFactory initialized")

    def create_template_from_npc(self, npc: Character, template_name: str = None) -> CharacterTemplate:
        """Create a CharacterTemplate from an existing NPC.

        Args:
            npc: The NPC to create a template from
            template_name: Optional name for the template. If not provided, will use the NPC's name.

        Returns:
            A new CharacterTemplate based on the NPC
        """
        self.logger.info(f"Creating template from NPC: {npc.name}")

        # Create stats template
        stats_template = self._create_stats_template_from_npc(npc)

        # Create biography template
        biography_template = self._create_biography_template_from_npc(npc)

        # Create the main template
        template_name = template_name or f"{npc.name} Template"
        template = CharacterTemplate.objects.create(
            name=template_name,
            description=f"Template created from NPC: {npc.name}",
            rank=npc.rank,
            organization=npc.organization,
            path=npc.path,
            tags=list(npc.tags).copy() if npc.tags else [],
            behavior=npc.behavior,
            dimension=npc.dimension if hasattr(npc, 'dimension') else None,
            stats_template=stats_template,
            biography_template=biography_template,
        )

        # Create school templates
        self._create_school_templates_from_npc(npc, template)

        # Create skill templates
        self._create_skill_templates_from_npc(npc, template)

        # Create modifier templates
        self._create_modifier_templates_from_npc(npc, template)

        # Create equipment templates
        self._create_equipment_templates_from_npc(npc, template)

        self.logger.info(f"Created template: {template.name}")
        return template

    def _create_stats_template_from_npc(self, npc: Character) -> CharacterStatsTemplate:
        """Create a CharacterStatsTemplate from an NPC's stats."""
        # Generate a unique name for the stats template
        import uuid
        unique_suffix = str(uuid.uuid4())[:8]
        stats_template = CharacterStatsTemplate.objects.create(
            name=f"{npc.name} Stats {unique_suffix}",
            description=f"Stats template created from NPC: {npc.name}",
        )

        # Create individual stat templates
        for stat in npc.stats.all():
            CharacterStatTemplate.objects.create(
                template=stats_template,
                stat=stat.name,
                value=stat.value
            )

        return stats_template

    def _create_biography_template_from_npc(self, npc: Character) -> CharacterBiographyTemplate:
        """Create a CharacterBiographyTemplate from an NPC's biography."""
        try:
            bio = npc.biography
            age = bio.age
            gender = bio.gender
            background = bio.background
            appearance = bio.appearance
        except:
            # If the NPC doesn't have a biography, use default values
            age = 30
            gender = 'OTHER'
            background = ''
            appearance = ''

        # Generate a unique name for the biography template
        import uuid
        unique_suffix = str(uuid.uuid4())[:8]
        bio_template = CharacterBiographyTemplate.objects.create(
            name=f"{npc.name} Biography {unique_suffix}",
            description=f"Biography template created from NPC: {npc.name}",
            age_min=age,
            age_max=age,
            gender=gender,
            randomize_gender=False,
            background=background,
            appearance=appearance,
        )

        return bio_template

    def _create_school_templates_from_npc(self, npc: Character, template: CharacterTemplate) -> None:
        """Create CharacterSchoolTemplate objects from an NPC's learned schools."""
        self.logger.info(f"Creating school templates for NPC: {npc.name}")

        # Get all learned schools for the NPC
        learned_schools = npc.learned_schools.all()
        created_count = 0

        for learned_school in learned_schools:
            # Check if this school template already exists
            existing = CharacterSchoolTemplate.objects.filter(
                template=template,
                school=learned_school.school
            ).first()

            if existing:
                # Update the existing template if needed
                if existing.is_base != learned_school.is_base:
                    existing.is_base = learned_school.is_base
                    existing.save(update_fields=['is_base'])
                self.logger.info(f"School template for {learned_school.school.name} already exists, updated")
            else:
                # Create a new template
                CharacterSchoolTemplate.objects.create(
                    template=template,
                    school=learned_school.school,
                    is_base=learned_school.is_base
                )
                created_count += 1

        self.logger.info(f"Created {created_count} new school templates")

    def _create_modifier_templates_from_npc(self, npc: Character, template: CharacterTemplate) -> None:
        """Create CharacterModifierTemplate objects from an NPC's stat modifiers."""
        self.logger.info(f"Creating modifier templates for NPC: {npc.name}")

        # Get all stat modifiers for the NPC
        stat_modifiers = npc.stats_modifiers.all()
        created_count = 0

        for modifier in stat_modifiers:
            # Skip modifiers applied by effects as they are temporary
            if modifier.applied_by_effect:
                continue

            # Check if this modifier template already exists
            existing = CharacterModifierTemplate.objects.filter(
                template=template,
                stat=modifier.name
            ).first()

            if existing:
                # Update the existing template if needed
                if existing.value != modifier.value:
                    existing.value = modifier.value
                    existing.save(update_fields=['value'])
                self.logger.info(f"Modifier template for {modifier.name} already exists, updated")
            else:
                # Create a new template
                CharacterModifierTemplate.objects.create(
                    template=template,
                    stat=modifier.name,
                    value=modifier.value,
                    description=f"Modifier from NPC: {npc.name}"
                )
                created_count += 1

        self.logger.info(f"Created {created_count} new modifier templates")

    def _create_equipment_templates_from_npc(self, npc: Character, template: CharacterTemplate) -> None:
        """Create CharacterEquipmentTemplate objects from an NPC's equipped items."""
        self.logger.info(f"Creating equipment templates for NPC: {npc.name}")

        # Get all equipped items for the NPC
        character_items = npc.equipped_items.all()
        created_count = 0

        for character_item in character_items:
            world_item = character_item.world_item

            # Check if this equipment template already exists
            existing = CharacterEquipmentTemplate.objects.filter(
                template=template,
                item=world_item.item
            ).first()

            if existing:
                # Update the existing template if needed
                if not existing.is_equipped:
                    existing.is_equipped = True
                    existing.save(update_fields=['is_equipped'])
                self.logger.info(f"Equipment template for {world_item.item.name} already exists, updated")
            else:
                # Create a new template
                CharacterEquipmentTemplate.objects.create(
                    template=template,
                    item=world_item.item,
                    quantity=1,  # Assuming quantity of 1 for each equipped item
                    is_equipped=True  # Since these are equipped items
                )
                created_count += 1

        self.logger.info(f"Created {created_count} new equipment templates")

    def _create_skill_templates_from_npc(self, npc: Character, template: CharacterTemplate) -> None:
        """Create CharacterSkillTemplate objects from an NPC's learned skills."""
        self.logger.info(f"Creating skill templates for NPC: {npc.name}")

        # Get all learned skills for the NPC
        learned_skills = npc.learned_skills.all()
        created_count = 0

        for learned_skill in learned_skills:
            # Check if this skill template already exists
            existing = CharacterSkillTemplate.objects.filter(
                template=template,
                skill=learned_skill.skill
            ).first()

            if existing:
                # Update the existing template if needed
                if existing.is_base != learned_skill.is_base:
                    existing.is_base = learned_skill.is_base
                    existing.save(update_fields=['is_base'])
                self.logger.info(f"Skill template for {learned_skill.skill.name} already exists, updated")
            else:
                # Create a new template
                CharacterSkillTemplate.objects.create(
                    template=template,
                    skill=learned_skill.skill,
                    is_base=learned_skill.is_base
                )
                created_count += 1

        self.logger.info(f"Created {created_count} new skill templates")

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

        # Apply template modifiers
        self._apply_template_modifiers(npc, config.template)

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

    def _apply_template_modifiers(self, npc: Character, template: CharacterTemplate) -> None:
        """Apply stat modifiers from a template to an NPC."""
        self.logger.info(f"Applying template modifiers to NPC: {npc.name}")

        # Apply modifiers from the template
        for modifier_template in template.modifier_templates.all():
            StatModifier.objects.create(
                character=npc,
                name=modifier_template.stat,
                value=modifier_template.value
            )
