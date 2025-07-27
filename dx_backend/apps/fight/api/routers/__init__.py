from rest_framework.routers import DefaultRouter

from apps.fight.api.views.openai import FightViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('fight', FightViewSet, basename='openai-fight ')
