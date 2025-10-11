from django.db import models
from pydantic import BaseModel as PydanticBaseModel

from apps.core.utils.models import BaseModel


class DocumentCategoryEnum(models.TextChoices):
    EVENTS = "events", "Events"
    RULES = "rules", "Rules"
    LORE = "lore", "Lore"
    STORIES = "stories", "Stories"
    GUIDES = "guides", "Guides"
    ITEMS = "items", "Items"
    CHARACTERS = "characters", "Characters"
    LOCATIONS = "locations", "Locations"
    PLACES = "places", "Places"
    FACTIONS = "factions", "Factions"
    CREATURES = "creatures", "Creatures"
    SKILLS = "skills", "Skills"
    SPELLS = "spells", "Spells"
    ABILITIES = "abilities", "Abilities"
    OTHER = "other", "Other"


class DimensionDatetimeInfo(PydanticBaseModel):
    active_glow: bool
    sol: int
    solar_year: int
    cycles: int

    @classmethod
    def from_model(cls, instance: 'DateTimeInfo') -> 'DimensionDatetimeInfo':
        return DimensionDatetimeInfo(
            active_glow=instance.active_glow,
            sol=instance.sol,
            solar_year=instance.solar_year,
            cycles=instance.to_cycles(),
        )


class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True, choices=DocumentCategoryEnum.choices,
                            default=DocumentCategoryEnum.OTHER)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='document-categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Document(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    categories = models.ManyToManyField(DocumentCategory, related_name='documents')
    image = models.ImageField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.title


class DateTimeInfo(BaseModel):
    """
    Solary year is 500 sols
    Each sol is 100 cycles

    Epochs:
    BAG - Before Active Glow
    AG - Active Glow
    """
    active_glow = models.BooleanField(default=True)
    sol = models.PositiveBigIntegerField(default=0, help_text="Number of sol's since the start of the calendar")
    solar_year = models.PositiveBigIntegerField(default=0,
                                                help_text="Number of solar years since the start of the calendar")

    def to_cycles(self) -> int:
        return self.solar_year * 500 * 100 + self.sol * 100

    def __str__(self):
        return f"{'HE' if self.active_glow else 'SE'} {self.solar_year} - Sol {self.sol}"


class TimeLineEvent(BaseModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='timeline_events')
    date_time = models.ForeignKey(DateTimeInfo, on_delete=models.CASCADE, related_name='timeline_events')

    def __str__(self):
        return f"Event: {self.document.title} at {self.date_time}"

    class Meta:
        ordering = ['date_time__solar_year', 'date_time__sol']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"
