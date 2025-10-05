from rest_framework.routers import DefaultRouter
from apps.knowledge_base.api.views import (
    KnowledgeBaseItemViewSet,
    KnowledgeBaseItemTagViewSet,
    DXDateViewSet
)

# Create router for knowledge base API endpoints
knowledge_base_router = DefaultRouter()

# Register all knowledge base-related ViewSets
knowledge_base_router.register(r'items', KnowledgeBaseItemViewSet, basename='knowledgebaseitem')
knowledge_base_router.register(r'tags', KnowledgeBaseItemTagViewSet, basename='knowledgebaseitemtag')
knowledge_base_router.register(r'dates', DXDateViewSet, basename='dxdate')

# Export URL patterns
urlpatterns = knowledge_base_router.urls