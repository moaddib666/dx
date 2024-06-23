from rest_framework.routers import DefaultRouter

from apps.fight.api.views.openai import DuelInvitationViewSet, FightViewSet, FightActionsViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('invitation', DuelInvitationViewSet, basename='openai-duel')
OpenAIRouter.register('action', FightActionsViewSet, basename='openai-action ')
OpenAIRouter.register('fight', FightViewSet, basename='openai-fight ')
