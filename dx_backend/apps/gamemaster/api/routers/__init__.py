from rest_framework.routers import DefaultRouter

from apps.gamemaster.api.views.character import GameMasterCharacterViewSet
from apps.gamemaster.api.views.currency import GameMasterCurrencyTokenViewSet, GameMasterCharacterCurrencyViewSet
from apps.gamemaster.api.views.effects import GameMasterEffectViewSet, GameMasterActiveEffectViewSet
from apps.gamemaster.api.views.game_objects import GameObjectViewSet
from apps.gamemaster.api.views.items import GameMasterItemViewSet, GameMasterWorldItemViewSet, GameMasterCharacterItemViewSet
from apps.gamemaster.api.views.school import GameMasterSchoolViewSet, GameMasterSkillViewSet, GameMasterPathViewSet
from apps.gamemaster.api.views.skills import GameMasterLearnedSkillViewSet, GameMasterLearnedSchoolViewSet
from apps.gamemaster.api.views.world import (
    GameMasterDimensionViewSet, GameMasterPlanetViewSet, GameMasterContinentViewSet,
    GameMasterCountryViewSet, GameMasterCityViewSet, GameMasterAreaViewSet,
    GameMasterLocationViewSet, GameMasterPositionViewSet, GameMasterMapViewSet
)

GameMasterRouter = DefaultRouter()

# Character viewsets
GameMasterRouter.register('characters', GameMasterCharacterViewSet, basename='gamemaster-characters')

# World viewsets
GameMasterRouter.register('dimensions', GameMasterDimensionViewSet, basename='gamemaster-dimensions')
GameMasterRouter.register('planets', GameMasterPlanetViewSet, basename='gamemaster-planets')
GameMasterRouter.register('continents', GameMasterContinentViewSet, basename='gamemaster-continents')
GameMasterRouter.register('countries', GameMasterCountryViewSet, basename='gamemaster-countries')
GameMasterRouter.register('cities', GameMasterCityViewSet, basename='gamemaster-cities')
GameMasterRouter.register('areas', GameMasterAreaViewSet, basename='gamemaster-areas')
GameMasterRouter.register('locations', GameMasterLocationViewSet, basename='gamemaster-locations')
GameMasterRouter.register('positions', GameMasterPositionViewSet, basename='gamemaster-positions')
GameMasterRouter.register('maps', GameMasterMapViewSet, basename='gamemaster-maps')

# Items viewsets
GameMasterRouter.register('items', GameMasterItemViewSet, basename='gamemaster-items')
GameMasterRouter.register('world-items', GameMasterWorldItemViewSet, basename='gamemaster-world-items')
GameMasterRouter.register('character-items', GameMasterCharacterItemViewSet, basename='gamemaster-character-items')

# Skills viewsets
GameMasterRouter.register('learned-skills', GameMasterLearnedSkillViewSet, basename='gamemaster-learned-skills')
GameMasterRouter.register('learned-schools', GameMasterLearnedSchoolViewSet, basename='gamemaster-learned-schools')

# Effects viewsets
GameMasterRouter.register('effects', GameMasterEffectViewSet, basename='gamemaster-effects')
GameMasterRouter.register('active-effects', GameMasterActiveEffectViewSet, basename='gamemaster-active-effects')

# School viewsets
GameMasterRouter.register('schools', GameMasterSchoolViewSet, basename='gamemaster-schools')
GameMasterRouter.register('skills', GameMasterSkillViewSet, basename='gamemaster-skills')
GameMasterRouter.register('paths', GameMasterPathViewSet, basename='gamemaster-paths')

# Currency viewsets
GameMasterRouter.register('currency-tokens', GameMasterCurrencyTokenViewSet, basename='gamemaster-currency-tokens')
GameMasterRouter.register('character-currencies', GameMasterCharacterCurrencyViewSet, basename='gamemaster-character-currencies')

# Game Objects viewset
GameMasterRouter.register('game-objects', GameObjectViewSet, basename='gamemaster-game-objects')
