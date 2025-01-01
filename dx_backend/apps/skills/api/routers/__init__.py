from rest_framework.routers import DefaultRouter

from apps.skills.api.views.openai import OpenAILearnedSkillsViewSet, OpenAILearnedSchoolsViewSet, \
    GameMasterOpenAILearnedSkillsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('shools', OpenAILearnedSchoolsViewSet, basename='openai-shools')
OpenAIRouter.register('skills', OpenAILearnedSkillsViewSet, basename='openai-skills')
OpenAIRouter.register('gm/skills', GameMasterOpenAILearnedSkillsViewSet, basename='openai-gm-skills')

