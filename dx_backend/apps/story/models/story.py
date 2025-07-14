from django.db import models
from apps.core.utils.models import BaseModel


class Story(BaseModel):
    """
    Represents a story based on QuestStoryTaller.MD specification.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.JSONField(default=list, help_text="List of tags for the story")
    image = models.URLField(null=True, blank=True, help_text="Optional URL to an image representing the story")
    canonical = models.BooleanField(default=False, help_text="Default to false, need review by the Owner")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Stories"


class Chapter(BaseModel):
    """
    Represents a chapter within a story based on QuestStoryTaller.MD specification.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True, help_text="Optional URL to an image representing the chapter")
    order = models.PositiveIntegerField(default=0, help_text="Order of the chapter within the story")

    def __str__(self):
        return f"{self.story.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ['story', 'order']
