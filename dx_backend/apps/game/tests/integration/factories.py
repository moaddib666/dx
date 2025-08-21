"""
Factory Boy factories for integration tests.
"""

import factory
from factory.django import DjangoModelFactory

from apps.action.models import Cycle, CharacterAction
from apps.game.models import Campaign


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


class CycleFactory(DjangoModelFactory):
    """Factory for Cycle model."""

    class Meta:
        model = Cycle

    number = factory.Sequence(lambda n: n)
    campaign = factory.SubFactory(CampaignFactory)


class CharacterActionFactory(DjangoModelFactory):
    """Factory for CharacterAction model."""

    class Meta:
        model = CharacterAction

    cycle = factory.SubFactory(CycleFactory)
    accepted = False
    performed = False
    data = factory.Dict({})
    immediate = False
    action_type = CharacterAction.ActionType.USE_SKILL
    order = factory.Sequence(lambda n: float(n))
