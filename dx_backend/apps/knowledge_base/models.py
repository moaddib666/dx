from django.db import models
from apps.core.utils.models import BaseModel


class KnowledgeBaseItemTag(models.Model):
    """
    Tag model for knowledge base items.
    """
    label = models.CharField(max_length=255, primary_key=True)
    
    def __str__(self):
        return self.label
    
    class Meta:
        verbose_name = "Knowledge Base Item Tag"
        verbose_name_plural = "Knowledge Base Item Tags"


class DXDate(models.Model):
    """
    DX Date model with cycle-based dating system.
    Cycle system: dxDay = 100 cycle; dxYear = 10,000; dxMonth = 12
    Era-Decade-Sol conversion: Sol = 100 cycles, Decade = 10 Sol, Era = 1000 Decade
    """
    dxCycle = models.BigIntegerField(primary_key=True, help_text="Cycle number (dxDay = 100 cycle; dxYear = 10,000; dxMonth = 12)")
    BAG = models.BooleanField(default=False, help_text="Before Active Glow")
    
    def __str__(self):
        return f"Cycle {self.dxCycle} {'(BAG)' if self.BAG else ''}"
    
    class Meta:
        verbose_name = "DX Date"
        verbose_name_plural = "DX Dates"


class KnowledgeBaseItem(BaseModel):
    """
    Knowledge base item model for storing events, locations, and characters.
    """
    
    class CategoryChoices(models.TextChoices):
        EVENTS = "events", "Events"
        LOCATION = "location", "Location"
        CHARACTER = "character", "Character"
    
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        help_text="Category of the knowledge base item"
    )
    dxCycle = models.BigIntegerField(help_text="Cycle number (dxDay = 100 cycle; dxYear = 10,000; dxMonth = 12)")
    description = models.TextField(help_text="Description of the knowledge base item")
    breadcrumbs = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='child_items',
        help_text="Related knowledge base items forming breadcrumb navigation"
    )
    tags = models.ManyToManyField(
        KnowledgeBaseItemTag,
        blank=True,
        related_name='knowledge_base_items',
        help_text="Tags associated with this knowledge base item"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata as JSON (e.g., {'customField': 'value'})"
    )
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.description[:50]}..."
    
    class Meta:
        verbose_name = "Knowledge Base Item"
        verbose_name_plural = "Knowledge Base Items"
        ordering = ['dxCycle', 'category']
