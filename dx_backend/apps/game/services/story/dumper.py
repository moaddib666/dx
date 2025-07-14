import json
import logging
from typing import Dict, Any, Optional

from apps.core.models import StoryData, ChapterData, QuestData, ConditionData, TriggerData, RewardData
from apps.core.models import ItemRewardData, TokenRewardData, EffectRewardData
from apps.story.models import Story, Chapter, Quest, Condition, Reward
from apps.core.models import Trigger


class StoryDumper:
    """
    Service for dumping Story objects to JSON format according to QuestStoryTaller.MD specification.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, output_file_path: Optional[str] = None):
        self.output_file_path = output_file_path
        self.processed_objects = {
            'stories': 0,
            'chapters': 0,
            'quests': 0,
            'conditions': 0,
            'triggers': 0,
            'rewards': 0
        }

    def dump(self, story: Story) -> None:
        """
        Dump a Story to JSON file.
        
        Args:
            story: The Story instance to dump
            
        Raises:
            ValueError: If output_file_path is not set
        """
        if not self.output_file_path:
            raise ValueError("output_file_path must be set to dump to file")

        data = self.to_dict(story)

        with open(self.output_file_path, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        self._log_summary()
        self.logger.info(f"Story successfully dumped to {self.output_file_path}")

    def to_dict(self, story: Story) -> Dict[str, Any]:
        """
        Convert a Story to dictionary format.
        
        Args:
            story: The Story instance to convert
            
        Returns:
            Dict containing the story data in JSON format
        """
        self._reset_counters()
        story_data = self._serialize_story(story)
        return story_data.dict()

    def to_json_string(self, story: Story) -> str:
        """
        Convert a Story to JSON string.
        
        Args:
            story: The Story instance to convert
            
        Returns:
            JSON string representation of the story
        """
        data = self.to_dict(story)
        return json.dumps(data, indent=4, ensure_ascii=False)

    def _reset_counters(self):
        """Reset processed object counters."""
        for key in self.processed_objects:
            self.processed_objects[key] = 0

    def _serialize_story(self, story: Story) -> StoryData:
        """Serialize Story instance to StoryData."""
        chapters = []
        for chapter in story.chapters.all().order_by('order'):
            chapters.append(self._serialize_chapter(chapter))

        self.processed_objects['stories'] += 1

        return StoryData(
            title=story.title,
            description=story.description,
            tags=story.tags or [],
            chapters=chapters,
            image=story.image.url if story.image else None,
            canonical=story.canonical
        )

    def _serialize_chapter(self, chapter: Chapter) -> ChapterData:
        """Serialize Chapter instance to ChapterData."""
        quests = []
        for quest in chapter.quests.all().order_by('order'):
            quests.append(self._serialize_quest(quest))

        self.processed_objects['chapters'] += 1

        return ChapterData(
            title=chapter.title,
            description=chapter.description,
            quests=quests,
            image=chapter.image.url if chapter.image else None
        )

    def _serialize_quest(self, quest: Quest) -> QuestData:
        """Serialize Quest instance to QuestData."""
        starters = []
        for condition in quest.starters.all():
            starters.append(self._serialize_condition(condition))

        objectives = []
        for condition in quest.objectives.all():
            objectives.append(self._serialize_condition(condition))

        on_success = None
        if quest.on_success:
            on_success = self._serialize_reward(quest.on_success)

        on_failure = None
        if quest.on_failure:
            on_failure = self._serialize_reward(quest.on_failure)

        self.processed_objects['quests'] += 1

        return QuestData(
            title=quest.title,
            description=quest.description,
            starters=starters,
            objectives=objectives,
            onSuccess=on_success,
            onFailure=on_failure,
            image=quest.image.url if quest.image else None,
            cycleLimit=quest.cycle_limit
        )

    def _serialize_condition(self, condition: Condition) -> ConditionData:
        """Serialize Condition instance to ConditionData."""
        triggers = []
        for trigger in condition.triggers.all():
            triggers.append(self._serialize_trigger(trigger))

        self.processed_objects['conditions'] += 1

        return ConditionData(
            type=condition.type,
            triggers=triggers
        )

    def _serialize_trigger(self, trigger: Trigger) -> TriggerData:
        """Serialize Trigger instance to TriggerData."""
        self.processed_objects['triggers'] += 1

        return TriggerData(
            type=trigger.type,
            gameObject=str(trigger.game_object.id) if trigger.game_object else None,
            position=str(trigger.position.id) if trigger.position else None,
            description=trigger.description,
            location=str(trigger.location.id) if trigger.location else None,
            npc=str(trigger.npc.id) if trigger.npc else None,
            skill=str(trigger.skill.id) if trigger.skill else None,
            item=str(trigger.item.id) if trigger.item else None
        )

    def _serialize_reward(self, reward: Reward) -> RewardData:
        """Serialize Reward instance to RewardData."""
        items = []
        for item_reward in reward.items.all():
            items.append(ItemRewardData(
                itemId=str(item_reward.item.id),
                quantity=item_reward.amount
            ))

        tokens = []
        for token_reward in reward.tokens.all():
            tokens.append(TokenRewardData(
                tokenId=str(token_reward.token.id),
                quantity=token_reward.amount
            ))

        effects = []
        for effect_reward in reward.effects.all():
            effects.append(EffectRewardData(
                effectId=str(effect_reward.effect.id),
                duration=effect_reward.duration
            ))

        self.processed_objects['rewards'] += 1

        return RewardData(
            description=reward.description,
            experience=reward.experience,
            items=items,
            tokens=tokens,
            effects=effects
        )

    def _log_summary(self):
        """Log summary of processed objects."""
        self.logger.info("Story dumping completed:")
        for obj_type, count in self.processed_objects.items():
            if count > 0:
                self.logger.info(f"  {obj_type}: {count}")
