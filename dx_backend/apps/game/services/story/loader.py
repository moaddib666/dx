import json
import logging
import uuid
from typing import Dict, Any, Optional

from django.db import transaction
from pydantic import ValidationError

from apps.core.models import StoryData, TriggerType, TriggerData
from apps.story.models import Story, Chapter, Quest, Condition, Reward, ItemReward, TokenReward, EffectReward
from apps.core.models import Trigger


class StoryLoader:
    """
    Service for loading Story objects from JSON format according to QuestStoryTaller.MD specification.
    Implements smart handling for unknown trigger types by creating CUSTOM triggers.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.created_objects = {
            'stories': 0,
            'chapters': 0,
            'quests': 0,
            'conditions': 0,
            'triggers': 0,
            'rewards': 0,
            'custom_triggers': 0
        }

    def load(self) -> Story:
        """
        Load a Story from JSON file.
        
        Returns:
            Story: The loaded Story instance
            
        Raises:
            ValidationError: If JSON structure is invalid
            FileNotFoundError: If JSON file doesn't exist
        """
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)

        try:
            story_data = StoryData(**data)
        except ValidationError as e:
            self.logger.error(f"Invalid JSON structure: {e}")
            raise

        with transaction.atomic():
            story = self._create_story(story_data)
            self._log_summary()
            return story

    def load_from_dict(self, data: Dict[str, Any]) -> Story:
        """
        Load a Story from dictionary data.
        
        Args:
            data: Dictionary containing story data
            
        Returns:
            Story: The loaded Story instance
        """
        try:
            story_data = StoryData(**data)
        except ValidationError as e:
            self.logger.error(f"Invalid data structure: {e}")
            raise

        with transaction.atomic():
            story = self._create_story(story_data)
            self._log_summary()
            return story

    def _create_story(self, story_data: StoryData) -> Story:
        """Create Story instance from StoryData."""
        story = Story.objects.create(
            title=story_data.title,
            description=story_data.description,
            tags=story_data.tags,
            image=story_data.image,
            canonical=story_data.canonical
        )
        self.created_objects['stories'] += 1

        for order, chapter_data in enumerate(story_data.chapters):
            self._create_chapter(story, chapter_data, order)

        return story

    def _create_chapter(self, story: Story, chapter_data, order: int):
        """Create Chapter instance from ChapterData."""
        chapter = Chapter.objects.create(
            story=story,
            title=chapter_data.title,
            description=chapter_data.description,
            image=chapter_data.image,
            order=order
        )
        self.created_objects['chapters'] += 1

        for quest_order, quest_data in enumerate(chapter_data.quests):
            self._create_quest(chapter, quest_data, quest_order)

    def _create_quest(self, chapter: Chapter, quest_data, order: int):
        """Create Quest instance from QuestData."""
        quest = Quest.objects.create(
            chapter=chapter,
            title=quest_data.title,
            description=quest_data.description,
            image=quest_data.image,
            cycle_limit=quest_data.cycleLimit,
            order=order
        )
        self.created_objects['quests'] += 1

        # Create starters
        for starter_data in quest_data.starters:
            condition = self._create_condition(starter_data)
            quest.starters.add(condition)

        # Create objectives
        for objective_data in quest_data.objectives:
            condition = self._create_condition(objective_data)
            quest.objectives.add(condition)

        # Create rewards
        if quest_data.onSuccess:
            quest.on_success = self._create_reward(quest_data.onSuccess)
            quest.save()

        if quest_data.onFailure:
            quest.on_failure = self._create_reward(quest_data.onFailure)
            quest.save()

    def _create_condition(self, condition_data) -> Condition:
        """Create Condition instance from ConditionData."""
        condition = Condition.objects.create(type=condition_data.type)
        self.created_objects['conditions'] += 1

        for trigger_data in condition_data.triggers:
            trigger = self._create_trigger(trigger_data)
            condition.triggers.add(trigger)

        return condition

    def _create_trigger(self, trigger_data: TriggerData) -> Trigger:
        """
        Create Trigger instance from TriggerData with smart handling for unknown types.
        Unknown trigger types are converted to CUSTOM triggers with extended description.
        """
        trigger_type = trigger_data.type
        description = trigger_data.description

        # Smart handling for unknown trigger types
        if trigger_type not in [choice.value for choice in TriggerType]:
            self.logger.warning(f"Unknown trigger type '{trigger_type}', creating CUSTOM trigger")
            # Extend description with original trigger data
            extended_description = f"{description} [CUSTOM TRIGGER - Original type: {trigger_type}"
            if trigger_data.gameObject:
                extended_description += f", gameObject: {trigger_data.gameObject}"
            if trigger_data.position:
                extended_description += f", position: {trigger_data.position}"
            if trigger_data.location:
                extended_description += f", location: {trigger_data.location}"
            if trigger_data.npc:
                extended_description += f", npc: {trigger_data.npc}"
            if trigger_data.skill:
                extended_description += f", skill: {trigger_data.skill}"
            if trigger_data.item:
                extended_description += f", item: {trigger_data.item}"
            extended_description += "]"

            trigger_type = TriggerType.CUSTOM
            description = extended_description
            self.created_objects['custom_triggers'] += 1

        # Create trigger with resolved references
        trigger = Trigger.objects.create(
            type=trigger_type,
            description=description
        )

        # Set foreign key references if they exist and are valid UUIDs
        self._set_trigger_references(trigger, trigger_data)

        self.created_objects['triggers'] += 1
        return trigger

    def _set_trigger_references(self, trigger: Trigger, trigger_data: TriggerData):
        """Set foreign key references on trigger if valid UUIDs are provided."""
        try:
            if trigger_data.position:
                # Try to resolve position UUID
                from apps.world.models import Position
                try:
                    position = Position.objects.get(pk=uuid.UUID(trigger_data.position))
                    trigger.position = position
                except (Position.DoesNotExist, ValueError):
                    self.logger.warning(f"Position {trigger_data.position} not found")

            if trigger_data.location:
                # Try to resolve location UUID
                from apps.world.models import Location
                try:
                    location = Location.objects.get(pk=uuid.UUID(trigger_data.location))
                    trigger.location = location
                except (Location.DoesNotExist, ValueError):
                    self.logger.warning(f"Location {trigger_data.location} not found")

            if trigger_data.npc:
                # Try to resolve NPC UUID
                from apps.character.models import CharacterTemplate
                try:
                    npc = CharacterTemplate.objects.get(pk=uuid.UUID(trigger_data.npc))
                    trigger.npc = npc
                except (CharacterTemplate.DoesNotExist, ValueError):
                    self.logger.warning(f"CharacterTemplate {trigger_data.npc} not found")

            if trigger_data.skill:
                # Try to resolve skill UUID
                from apps.school.models import Skill
                try:
                    skill = Skill.objects.get(pk=uuid.UUID(trigger_data.skill))
                    trigger.skill = skill
                except (Skill.DoesNotExist, ValueError):
                    self.logger.warning(f"Skill {trigger_data.skill} not found")

            if trigger_data.item:
                # Try to resolve item UUID
                from apps.items.models import Item
                try:
                    item = Item.objects.get(pk=uuid.UUID(trigger_data.item))
                    trigger.item = item
                except (Item.DoesNotExist, ValueError):
                    self.logger.warning(f"Item {trigger_data.item} not found")

            trigger.save()

        except Exception as e:
            self.logger.error(f"Error setting trigger references: {e}")

    def _create_reward(self, reward_data) -> Reward:
        """Create Reward instance from RewardData."""
        reward = Reward.objects.create(
            description=reward_data.description,
            experience=reward_data.experience
        )
        self.created_objects['rewards'] += 1

        # Create item rewards
        for item_data in reward_data.items:
            try:
                from apps.items.models import Item
                item = Item.objects.get(pk=uuid.UUID(item_data.itemId))
                ItemReward.objects.create(
                    reward=reward,
                    item=item,
                    amount=item_data.quantity
                )
            except (Item.DoesNotExist, ValueError) as e:
                self.logger.warning(f"Item {item_data.itemId} not found for reward: {e}")

        # Create token rewards
        for token_data in reward_data.tokens:
            try:
                from apps.currency.models import CurrencyToken
                token = CurrencyToken.objects.get(pk=uuid.UUID(token_data.tokenId))
                TokenReward.objects.create(
                    reward=reward,
                    token=token,
                    amount=token_data.quantity
                )
            except (CurrencyToken.DoesNotExist, ValueError) as e:
                self.logger.warning(f"Token {token_data.tokenId} not found for reward: {e}")

        # Create effect rewards
        for effect_data in reward_data.effects:
            try:
                from apps.effects.models import Effect
                effect = Effect.objects.get(pk=uuid.UUID(effect_data.effectId))
                EffectReward.objects.create(
                    reward=reward,
                    effect=effect,
                    duration=effect_data.duration
                )
            except (Effect.DoesNotExist, ValueError) as e:
                self.logger.warning(f"Effect {effect_data.effectId} not found for reward: {e}")

        return reward

    def _log_summary(self):
        """Log summary of created objects."""
        self.logger.info("Story loading completed:")
        for obj_type, count in self.created_objects.items():
            if count > 0:
                self.logger.info(f"  {obj_type}: {count}")

        if self.created_objects['custom_triggers'] > 0:
            self.logger.warning(f"Created {self.created_objects['custom_triggers']} CUSTOM triggers for unknown types")
