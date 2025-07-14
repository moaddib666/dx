from django.db import models
from apps.core.utils.models import BaseModel
from apps.core.models import Trigger
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
    items = models.JSONField(default=list, help_text="List of items with itemId and quantity")
    tokens = models.JSONField(default=list, help_text="List of tokens with tokenId and quantity")
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reward: {self.experience} XP"


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
    image = models.URLField(null=True, blank=True, help_text="Optional URL to an image representing the quest")
    cycle_limit = models.PositiveIntegerField(default=50, help_text="Time limit in cycles (1 cycle = 1 turn)")
    order = models.PositiveIntegerField(default=0, help_text="Order of the quest within the chapter")

    def __str__(self):
        return f"{self.chapter.story.title} - {self.chapter.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ['chapter', 'order']
