from rest_framework.routers import DefaultRouter

from apps.player.api.views.openai import OpenAISchoolsManagementViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', OpenAISchoolsManagementViewSet, basename='openai')
