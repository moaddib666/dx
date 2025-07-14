from django.db import models

from apps.core.models import Trigger
from apps.core.utils.models import BaseModel
from .story import Chapter


class ConditionType(models.TextChoices):
    ALL = "all", "All"
    ANY = "any", "Any"
    NONE = "none", "None"


class Condition(BaseModel):
    """
    Represents a condition for quest starters and objectives based on QuestStoryTaller.MD specification.
    """
    type = models.CharField(max_length=10, choices=ConditionType.choices, default=ConditionType.ALL)
    triggers = models.ManyToManyField(Trigger, related_name='conditions')

    def __str__(self):
        return f"{self.type} condition with {self.triggers.count()} triggers"


class Reward(BaseModel):
    """
    Represents a reward for quest success/failure based on QuestStoryTaller.MD specification.
    """
    description = models.TextField()
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reward: {self.experience} XP"


class TokenReward(BaseModel):
    amount = models.PositiveIntegerField(default=0, help_text="Amount of tokens to reward")
    token = models.ForeignKey('currency.CurrencyToken', on_delete=models.CASCADE, related_name='token_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='tokens', null=True, blank=True)

    def __str__(self):
        return f"TokenReward: {self.amount} {self.token}"


class ItemReward(BaseModel):
    amount = models.PositiveIntegerField(default=0, help_text="Amount of items to reward")
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name='item_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    def __str__(self):
        return f"ItemReward: {self.amount} {self.item}"


class EffectReward(BaseModel):
    effect = models.ForeignKey('effects.Effect', on_delete=models.CASCADE, related_name='effect_rewards')
    duration = models.PositiveIntegerField(default=0, help_text="Duration of the effect in turns")
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='effects', null=True, blank=True)

    def __str__(self):
        return f"EffectReward: {self.effect} for {self.duration} turns"


class Quest(BaseModel):
    """
    Represents a quest within a chapter based on QuestStoryTaller.MD specification.
    """
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='quests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    starters = models.ManyToManyField(Condition, related_name='starter_quests', blank=True)
    objectives = models.ManyToManyField(Condition, related_name='objective_quests', blank=True)
    on_success = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='success_quests', null=True,
                                   blank=True)
    on_failure = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='failure_quests', null=True,
                                   blank=True)
    image = models.ImageField(null=True, blank=True, help_text="Optional URL to an image representing the quest")
    cycle_limit = models.PositiveIntegerField(default=50, help_text="Time limit in cycles (1 cycle = 1 turn)",
                                              null=True, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of the quest within the chapter")

    def __str__(self):
        return f"{self.chapter.story.title} - {self.chapter.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ['chapter', 'order']


class Note(BaseModel):
    """
    Represents a note within a quest based on QuestStoryTaller.MD specification.
    """
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='notes')
    image = models.ImageField(null=True, blank=True, help_text="Optional URL to an image representing the note")
    content = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order of the note within the quest")

    def __str__(self):
        return f"Note for {self.quest.title} - Order: {self.order}"

    class Meta:
        ordering = ['order']
        unique_together = ['quest', 'order']
