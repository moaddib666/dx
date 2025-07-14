from rest_framework.routers import DefaultRouter
from apps.story.api.views import (
    StoryViewSet,
    ChapterViewSet,
    QuestViewSet,
    ConditionViewSet,
    RewardViewSet,
    TriggerViewSet
)

# Create router for story API endpoints
story_router = DefaultRouter()

# Register all story-related ViewSets
story_router.register(r'stories', StoryViewSet, basename='story')
story_router.register(r'chapters', ChapterViewSet, basename='chapter')
story_router.register(r'quests', QuestViewSet, basename='quest')
story_router.register(r'conditions', ConditionViewSet, basename='condition')
story_router.register(r'rewards', RewardViewSet, basename='reward')
story_router.register(r'triggers', TriggerViewSet, basename='trigger')

# Export URL patterns
urlpatterns = story_router.urls
