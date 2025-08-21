"""
Factory Boy factories for game models.
"""

import factory
from factory.django import DjangoModelFactory

from apps.game.models import Campaign
from apps.character.models.npc import (
    CharacterTemplate, CharacterStatsTemplate, CharacterBiographyTemplate,
    CharacterStatTemplate
)
from apps.character.models.common import Organization, Rank
from apps.core.models import CharacterStats, BehaviorModel, GenderEnum
from apps.world.tests.factories.world import DimensionFactory


class CampaignFactory(DjangoModelFactory):
    """Factory for Campaign model."""

    class Meta:
        model = Campaign

    name = factory.Sequence(lambda n: f"Test Campaign {n}")
    description = factory.Faker('text', max_nb_chars=200)
    is_active = True
    is_completed = False
    default = False
    auto_play = False


class OrganizationFactory(DjangoModelFactory):
    """Factory for Organization model."""

    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Test Organization {n}")
    description = factory.Faker('text', max_nb_chars=200)


class RankFactory(DjangoModelFactory):
    """Factory for Rank model."""

    class Meta:
        model = Rank

    name = factory.Sequence(lambda n: f"Test Rank {n}")
    description = factory.Faker('text', max_nb_chars=200)
    grade = factory.Sequence(lambda n: min(n // 101, 10))  # Ensure unique combinations
    grade_rank = factory.Sequence(lambda n: n % 101)  # 0-100 as per model validation
    additional_stat_points = 0
    experience_needed = factory.Faker('pyint', min_value=0, max_value=10000)


class CharacterStatsTemplateFactory(DjangoModelFactory):
    """Factory for CharacterStatsTemplate model."""

    class Meta:
        model = CharacterStatsTemplate

    name = factory.Sequence(lambda n: f"Test Stats Template {n}")
    description = factory.Faker('text', max_nb_chars=200)


class CharacterStatTemplateFactory(DjangoModelFactory):
    """Factory for CharacterStatTemplate model."""

    class Meta:
        model = CharacterStatTemplate

    template = factory.SubFactory(CharacterStatsTemplateFactory)
    stat = factory.Iterator([stat for stat in CharacterStats])
    value = factory.Faker('pyint', min_value=1, max_value=20)


class CharacterBiographyTemplateFactory(DjangoModelFactory):
    """Factory for CharacterBiographyTemplate model."""

    class Meta:
        model = CharacterBiographyTemplate

    name = factory.Sequence(lambda n: f"Test Biography Template {n}")
    description = factory.Faker('text', max_nb_chars=200)
    age_min = 18
    age_max = 60
    gender = GenderEnum.OTHER
    randomize_gender = False
    background = factory.Faker('text', max_nb_chars=500)
    appearance = factory.Faker('text', max_nb_chars=500)
    background_variations = factory.List([])
    appearance_variations = factory.List([])
    avatar = ''


class CharacterTemplateFactory(DjangoModelFactory):
    """Factory for CharacterTemplate model."""

    class Meta:
        model = CharacterTemplate

    name = factory.Sequence(lambda n: f"Test Character Template {n}")
    description = factory.Faker('text', max_nb_chars=200)
    rank = None  # Avoid unique constraint issues
    organization = factory.SubFactory(OrganizationFactory)
    path = None  # ThePath factory would need to be created if needed
    tags = factory.List(['test', 'factory'])
    behavior = BehaviorModel.PASSIVE
    dimension = None  # Avoid unique constraint issues
    stats_template = factory.SubFactory(CharacterStatsTemplateFactory)
    biography_template = factory.SubFactory(CharacterBiographyTemplateFactory)
    health_multiplier = 1.0
    energy_multiplier = 1.0
    action_points_multiplier = 1.0
    randomize_name = False
    name_pattern = ''
