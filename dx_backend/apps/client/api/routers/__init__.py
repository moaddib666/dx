from rest_framework.routers import DefaultRouter

from apps.client.api.views.openai import OpenAIClientManagementViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', OpenAIClientManagementViewSet, basename='openai')
