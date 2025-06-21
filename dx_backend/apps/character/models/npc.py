import random

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import CharacterStats, GenderEnum, BehaviorModel
from apps.core.utils.models import BaseModel


class CharacterTemplate(BaseModel):
    """
    Main template for creating NPCs. This is the central template that ties
    all other template components together.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    # Basic character properties
    rank = models.ForeignKey('character.Rank', on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey('character.Organization', on_delete=models.SET_NULL, null=True, blank=True)
    path = models.ForeignKey("school.ThePath", on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    behavior = models.CharField(max_length=20, choices=BehaviorModel.choices(), default=BehaviorModel.PASSIVE)
    dimension = models.ForeignKey("world.Dimension", on_delete=models.SET_NULL, null=True, blank=True, default=1)

    # Template components (relationships to other templates)
    stats_template = models.ForeignKey("CharacterStatsTemplate", on_delete=models.SET_NULL, null=True, blank=True)
    biography_template = models.ForeignKey("CharacterBiographyTemplate", on_delete=models.SET_NULL, null=True,
                                           blank=True)

    # Health/Energy calculations
    health_multiplier = models.FloatField(default=1.0,
                                          help_text="Multiplier for calculated health based on Physical Strength")
    energy_multiplier = models.FloatField(default=1.0,
                                          help_text="Multiplier for calculated energy based on Mental Strength")
    action_points_multiplier = models.FloatField(default=1.0,
                                                 help_text="Multiplier for calculated action points based on Speed")

    # Randomization settings
    randomize_name = models.BooleanField(default=False,
                                         help_text="Generate random names for NPCs created from this template")
    name_pattern = models.CharField(max_length=255, blank=True,
                                    help_text="Pattern for name generation, e.g., '{base_name} {number}'")

    # Campaign association
    campaign = models.ForeignKey('campaign.Campaign', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Character Template"
        verbose_name_plural = "Character Templates"


class CharacterStatsTemplate(BaseModel):
    """
    Template for character stats. Can be reused across multiple character templates.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_stat_value(self, stat_name: str) -> int:
        """Get the value for a specific stat, return 10 if not defined"""
        try:
            return self.stats.get(stat=stat_name).value
        except CharacterStatTemplate.DoesNotExist:
            return 10  # Default value

    def get_all_stats(self) -> dict:
        """Return all stats as a dictionary"""
        stats = {}
        for stat_choice in CharacterStats.choices:
            stat_name = stat_choice[0]
            stats[stat_name] = self.get_stat_value(stat_name)
        return stats


class CharacterStatTemplate(BaseModel):
    """
    Individual stat values for a stats template.
    """
    template = models.ForeignKey(CharacterStatsTemplate, on_delete=models.CASCADE, related_name='stats')
    stat = models.CharField(max_length=255, choices=CharacterStats.choices())
    value = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        unique_together = ('template', 'stat')

    def __str__(self):
        return f"{self.template.name} - {self.stat}: {self.value}"


class CharacterBiographyTemplate(BaseModel):
    """
    Template for character biography with randomization options.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    # Age range
    age_min = models.PositiveIntegerField(default=18, validators=[MinValueValidator(18), MaxValueValidator(900)])
    age_max = models.PositiveIntegerField(default=60, validators=[MinValueValidator(18), MaxValueValidator(900)])

    # Gender (can be specific or random)
    gender = models.CharField(max_length=50, choices=GenderEnum.choices, default=GenderEnum.OTHER)
    randomize_gender = models.BooleanField(default=False)

    # Appearance and background
    background = models.TextField(blank=True)
    appearance = models.TextField(blank=True)

    # Random variations
    background_variations = models.JSONField(default=list, blank=True,
                                             help_text="List of background variations to choose from randomly")
    appearance_variations = models.JSONField(default=list, blank=True,
                                             help_text="List of appearance variations to choose from randomly")

    avatar = models.ImageField(upload_to='avatars/', blank=True, help_text="Avatar image for the character")

    def __str__(self):
        return self.name

    def generate_age(self) -> int:
        """Generate a random age within the specified range"""
        return random.randint(self.age_min, self.age_max)

    def generate_gender(self) -> str:
        """Generate gender based on template settings"""
        if self.randomize_gender:
            return random.choice([choice[0] for choice in GenderEnum.choices])
        return self.gender

    def generate_background(self) -> str:
        """Generate background, using variations if available"""
        if self.background_variations:
            return random.choice(self.background_variations)
        return self.background

    def generate_appearance(self) -> str:
        """Generate appearance, using variations if available"""
        if self.appearance_variations:
            return random.choice(self.appearance_variations)
        return self.appearance


class CharacterSkillTemplate(BaseModel):
    """
    Skills that should be learned by characters created from a template.
    """
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='skill_templates')
    skill = models.ForeignKey("skills.Skill", on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)

    class Meta:
        unique_together = ('template', 'skill')

    def __str__(self):
        return f"{self.template.name} - {self.skill.name}"


class CharacterSchoolTemplate(BaseModel):
    """
    Schools that should be learned by characters created from a template.
    """
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='school_templates')
    school = models.ForeignKey("school.School", on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)

    class Meta:
        unique_together = ('template', 'school')

    def __str__(self):
        return f"{self.template.name} - {self.school.name}"


class CharacterModifierTemplate(BaseModel):
    """
    Stat modifiers that should be applied to characters created from a template.
    """
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='modifier_templates')
    stat = models.CharField(max_length=255, choices=CharacterStats.choices())
    value = models.IntegerField(help_text="Modifier value (can be positive or negative)")
    description = models.CharField(max_length=255, blank=True, help_text="Description of what causes this modifier")

    def __str__(self):
        return f"{self.template.name} - {self.stat}: {self.value:+d}"


class CharacterEquipmentTemplate(BaseModel):
    """
    Items/equipment that should be given to characters created from a template.
    """
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='equipment_templates')
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_equipped = models.BooleanField(default=False, help_text="Whether the item should be equipped automatically")

    class Meta:
        unique_together = ('template', 'item')

    def __str__(self):
        return f"{self.template.name} - {self.item.name} x{self.quantity}"


class CharacterNameTemplate(BaseModel):
    """
    Name templates for generating random names.
    """
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='name_templates')
    name_type = models.CharField(max_length=50, choices=[
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('full_name', 'Full Name'),
        ('nickname', 'Nickname'),
        ('title', 'Title'),
    ])
    names = models.JSONField(default=list, help_text="List of names to choose from randomly")
    gender_specific = models.CharField(max_length=50, choices=GenderEnum.choices, blank=True,
                                       help_text="If set, only use for this gender")

    def __str__(self):
        return f"{self.template.name} - {self.name_type}"

    def get_random_name(self, gender: str = None) -> str:
        """Get a random name, optionally filtered by gender"""
        if self.gender_specific and gender and self.gender_specific != gender:
            return ""

        if not self.names:
            return ""

        return random.choice(self.names)
