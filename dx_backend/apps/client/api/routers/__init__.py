from rest_framework.routers import DefaultRouter

from apps.client.api.views.openai import (
    OpenAIClientManagementViewSet,
    OpenAICampaignManagementViewSet,
    CurrentClientViewSet
)

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', OpenAIClientManagementViewSet, basename='openai')
OpenAIRouter.register('campaigns', OpenAICampaignManagementViewSet, basename='openai-campaigns')
OpenAIRouter.register('current', CurrentClientViewSet, basename='client-current')
