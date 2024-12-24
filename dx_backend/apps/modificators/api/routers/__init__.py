from rest_framework.routers import DefaultRouter

from apps.modificators.api.views.openai import OpenAICharacterModificatorsViewSet, OpenAIWorldModificatorsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('character', OpenAICharacterModificatorsViewSet, basename='openai-character-modificators')
OpenAIRouter.register('world', OpenAIWorldModificatorsViewSet, basename='openai-world-modificators')
