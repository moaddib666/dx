# Import all admin classes to register them with Django admin
from .story import StoryAdmin, ChapterAdmin
from .quest import QuestAdmin, NoteAdmin
from .rewards import (
    ConditionAdmin,
    RewardAdmin,
    TokenRewardAdmin,
    ItemRewardAdmin,
    EffectRewardAdmin
)

# All admin classes are automatically registered via @admin.register decorators
# in their respective files:
# - story.py: Story, Chapter
# - quest.py: Quest, Note  
# - rewards.py: Condition, Reward, TokenReward, ItemReward, EffectReward
