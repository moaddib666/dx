from apps.character.models import Character
from apps.core.models import CharacterGenericData
from .character_base_stats import CharacterBaseStatsService
from .character_creator import CharacterCreator
from .character_items import default_items_svc_factory
from .character_modificators import CharacterModificatorService
from .character_schools import CharacterSchoolService
from .character_skills import CharacterSkillsService
from .character_spawner import CharacterSpawner
from .character_stats import CharacterStatsService
from .core import CharacterService
from .location_service import LocationService
from ..items.world_item import default_world_item_factory
from ..rand_dice import DiceService


class CharacterFactory:

    def __init__(self, client):
        self.client = client
        self.character_creator = CharacterCreator(self.client)
        self.character_base_stats = CharacterBaseStatsService
        self.location_service = LocationService()
        self.character_spawner = CharacterSpawner()
        self.character_stats = CharacterStatsService()
        self.modificator_service = CharacterModificatorService()
        self.school_service = CharacterSchoolService()
        self.skill_service = CharacterSkillsService()
        self.dice_service_cls = DiceService
        self.world_item_factory = default_world_item_factory
        self.character_items_svc_factory = default_items_svc_factory

    def create_character(self, name: str, age: int, gender: str):
        character = self.character_creator.create_character(name, age, gender)
        location = self.location_service.get_or_create_home(character)
        self.character_spawner.spawn_character(character, location)
        self.character_stats.initialize_stats(character)
        return character

    def import_character(self, dto: CharacterGenericData) -> CharacterService:
        character = self.character_creator.import_character(dto)
        position = self.location_service.default(character)
        self.character_spawner.spawn_character(character, position)
        self.character_base_stats(character, self.dice_service_cls).reset_base_stats()
        self.modificator_service.initialize(character, dto.modificators)
        self.school_service.initialize(character, dto.schools)
        self.skill_service.initialize(character, dto.spells)
        self.give_campaign_start_items(character)
        char = CharacterService(character)
        char.refill_all()

        return char

    def give_campaign_start_items(self, character: Character):
        if not character.campaign:
            return
        items_svc = self.character_items_svc_factory.from_character(character)
        for start_item in character.campaign.start_items.all():
            if self.dice_service_cls.roll_chance(start_item.chance):
                for _ in range(start_item.quantity):
                    world_item = self.world_item_factory.create_world_item(start_item.item, character.campaign)
                    items_svc.pick_item(world_item)
