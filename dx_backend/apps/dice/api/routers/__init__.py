from rest_framework.routers import DefaultRouter

from apps.dice.api.views.challenge import ChallengeViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('challenge', ChallengeViewSet, basename='dice-challenge')
