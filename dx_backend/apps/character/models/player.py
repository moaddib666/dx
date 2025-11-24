from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.character.models.common import Organization, Rank
from apps.core.models import CharacterStats, GenderEnum, GameObject, BehaviorModel
from apps.core.utils.models import BaseModel, TagsDescriptor


class CharacterBiography(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(900)])
    gender = models.CharField(max_length=50, choices=GenderEnum.choices,
                              default=GenderEnum.OTHER)
    background = models.TextField(blank=True)
    appearance = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True,
                               default='avatars/placeholder/other.png')
    character = models.OneToOneField('character.Character', to_field='gameobject_ptr',
                                     on_delete=models.CASCADE,
                                     related_name='biography')


class PublishedCharacter(BaseModel):
    biography = models.ForeignKey(
        CharacterBiography, on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    big_avatar = models.ImageField(upload_to='avatarsPublic/', blank=True,
                                   default='avatars/placeholder/other.png')
    small_avatar = models.ImageField(upload_to='avatarsPublic/', blank=True,
                                     default='avatars/placeholder/other.png')
    tiktalk_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)


class Character(GameObject):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    owner = models.ForeignKey('client.Client', on_delete=models.CASCADE,
                              related_name='available_characters', null=True,
                              blank=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True,
                                     blank=True)
    tags = models.JSONField(default=list)
    path = models.ForeignKey("school.ThePath", on_delete=models.SET_NULL, null=True,
                             blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.IntegerField(default=0)

    current_health_points = models.IntegerField(default=1)
    current_energy_points = models.IntegerField(default=1)
    current_active_points = models.IntegerField(default=1)

    place_of_birth = models.ForeignKey("world.Location", on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='where_born')
    # FIXME: implement migration moved to GameObject
    # dimension = models.ForeignKey("world.Dimension", on_delete=models.SET_NULL, null=True, blank=True, default=1)
    # is_active = models.BooleanField(default=True)

    # fight = models.ForeignKey('fight.Fight', on_delete=models.SET_NULL, null=True, blank=True)

    school_slots = models.PositiveIntegerField(default=2)

    #
    npc = models.BooleanField(default=False)
    template = models.ForeignKey('character.CharacterTemplate',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    behavior = models.CharField(max_length=20, choices=BehaviorModel.choices(),
                                default=BehaviorModel.PASSIVE,
                                db_index=True)

    last_safe_position = models.ForeignKey('world.Position', on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name='characters_in_safe')

    resetting_base_stats = models.BooleanField(default=False)

    fight = models.ForeignKey('fight.Fight', on_delete=models.SET_NULL, null=True,
                              blank=True, related_name='joined')
    challenge = models.OneToOneField('dice.Challenge', on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='for_character')

    @property
    def alive(self) -> bool:
        return self.current_health_points > 0

    def __str__(self):
        return self.name


class Stat(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    name = models.CharField(max_length=255, choices=CharacterStats.choices(),
                            default=CharacterStats.PHYSICAL_STRENGTH)
    additional_value = models.IntegerField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE,
                                  related_name='stats')

    base_value = models.IntegerField(default=0)
    dice_rolls = models.ManyToManyField('action.DiceRollResult',
                                        related_name='base_stat_results')

    @property
    def value(self) -> int:
        return self.base_value + self.additional_value

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'character'],
                                    name='unique_stat_per_character')
        ]
        ordering = ['character', 'name']


class StatModifier(BaseModel):
    """
    name: string
    value: int
    """
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    name = models.CharField(max_length=255, choices=CharacterStats.choices(),
                            default=CharacterStats.PHYSICAL_STRENGTH)
    value = models.IntegerField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE,
                                  related_name='stats_modifiers')

    applied_by_effect = models.ForeignKey('effects.ActiveEffect',
                                          on_delete=models.CASCADE, null=True,
                                          blank=True,
                                          related_name='applied_stat_modifiers')

    def __str__(self):
        return f"{self.name} - {self.value}"
