"""
Fight services package.

This package provides comprehensive fight management services for the game system.
"""

from .core import (
    FightFactory,
    FightDetector,
    FightAutoJoiner,
    FightAutoLeaver,
    FightPendingJoiner,
    FightCloser,
    FightCoordinator
)

from .integration import FightGameLoopIntegration

__all__ = [
    'FightFactory',
    'FightDetector',
    'FightAutoJoiner',
    'FightAutoLeaver',
    'FightPendingJoiner',
    'FightCloser',
    'FightCoordinator',
    'FightGameLoopIntegration'
]
