from rest_framework.routers import DefaultRouter

from apps.fight.api.views.openai import DuelInvitationViewSet, FightViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('invitation', DuelInvitationViewSet, basename='openai-duel')
OpenAIRouter.register('', FightViewSet, basename='openai-fight ')
