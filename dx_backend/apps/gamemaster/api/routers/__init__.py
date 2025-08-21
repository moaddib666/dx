from rest_framework.routers import DefaultRouter

from apps.gamemaster.api.views.character import GameMasterCharacterViewSet
from apps.gamemaster.api.views.character_template import CharacterTemplateViewSet
from apps.gamemaster.api.views.impersonation import GameMasterImpersonationViewSet
from apps.gamemaster.api.views.npc import NPCViewSet
from apps.gamemaster.api.views.currency import GameMasterCurrencyTokenViewSet, GameMasterCharacterCurrencyViewSet
from apps.gamemaster.api.views.effects import GameMasterEffectViewSet, GameMasterActiveEffectViewSet
from apps.gamemaster.api.views.game_objects import GameObjectViewSet
from apps.gamemaster.api.views.items import GameMasterItemViewSet, GameMasterWorldItemViewSet, \
    GameMasterCharacterItemViewSet
from apps.gamemaster.api.views.school import GameMasterSchoolViewSet, GameMasterSkillViewSet, GameMasterPathViewSet
from apps.gamemaster.api.views.skills import GameMasterLearnedSkillViewSet, GameMasterLearnedSchoolViewSet, \
    SkillFactoryViewSet
from apps.gamemaster.api.views.world import WorldMapViewSet, PositionManagementViewSet, \
    PositionConnectionManagementViewSet

GameMasterRouter = DefaultRouter()

# Character viewsets
GameMasterRouter.register('characters', GameMasterCharacterViewSet, basename='gamemaster-characters')
GameMasterRouter.register('character-templates', CharacterTemplateViewSet, basename='gamemaster-character-templates')
GameMasterRouter.register('npcs', NPCViewSet, basename='gamemaster-npcs')

# # Items viewsets
GameMasterRouter.register('items', GameMasterItemViewSet, basename='gamemaster-items')
# GameMasterRouter.register('world-items', GameMasterWorldItemViewSet, basename='gamemaster-world-items')
# GameMasterRouter.register('character-items', GameMasterCharacterItemViewSet, basename='gamemaster-character-items')

# # Skills viewsets
# GameMasterRouter.register('learned-skills', GameMasterLearnedSkillViewSet, basename='gamemaster-learned-skills')
# GameMasterRouter.register('learned-schools', GameMasterLearnedSchoolViewSet, basename='gamemaster-learned-schools')
GameMasterRouter.register('skill', SkillFactoryViewSet, basename='gamemaster-skill')
# # Effects viewsets
# GameMasterRouter.register('effects', GameMasterEffectViewSet, basename='gamemaster-effects')
# GameMasterRouter.register('active-effects', GameMasterActiveEffectViewSet, basename='gamemaster-active-effects')

# # School viewsets
# GameMasterRouter.register('schools', GameMasterSchoolViewSet, basename='gamemaster-schools')
# GameMasterRouter.register('skills', GameMasterSkillViewSet, basename='gamemaster-skills')
# GameMasterRouter.register('paths', GameMasterPathViewSet, basename='gamemaster-paths')

# # Currency viewsets
# GameMasterRouter.register('currency-tokens', GameMasterCurrencyTokenViewSet, basename='gamemaster-currency-tokens')
# GameMasterRouter.register('character-currencies', GameMasterCharacterCurrencyViewSet,
#                           basename='gamemaster-character-currencies')

# Game Objects viewset
GameMasterRouter.register('game-objects', GameObjectViewSet, basename='gamemaster-game-objects')

# World Map viewset
GameMasterRouter.register('world-map', WorldMapViewSet, basename='gamemaster-world-map')
GameMasterRouter.register('world-positions', PositionManagementViewSet, basename='gamemaster-world-positions')
GameMasterRouter.register('world-position-connections', PositionConnectionManagementViewSet,
                          basename='gamemaster-world-position-connections')

# Impersonation viewset
GameMasterRouter.register('impersonation', GameMasterImpersonationViewSet, basename='gamemaster-impersonation')
