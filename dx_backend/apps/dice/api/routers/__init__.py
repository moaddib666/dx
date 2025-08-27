from rest_framework.routers import DefaultRouter

from apps.dice.api.views.challenge import ChallengeViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('dice', ChallengeViewSet, basename='dice')
