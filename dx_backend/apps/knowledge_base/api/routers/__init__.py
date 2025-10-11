from rest_framework.routers import DefaultRouter

from apps.knowledge_base.api.views import DocumentViewSet

# Create the Knowledge Base API router
KnowledgeBaseRouter = DefaultRouter()

# Register viewsets
KnowledgeBaseRouter.register('documents', DocumentViewSet, basename='knowledge-base-documents')
