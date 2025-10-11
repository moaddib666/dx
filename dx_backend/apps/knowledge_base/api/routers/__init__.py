from rest_framework.routers import DefaultRouter

from apps.knowledge_base.api.views import DocumentViewSet, TimeLineEventViewSet

# Create the Knowledge Base API router
KnowledgeBaseRouter = DefaultRouter()

# Register viewsets
KnowledgeBaseRouter.register('documents', DocumentViewSet, basename='knowledge-base-documents')
KnowledgeBaseRouter.register('timeline-events', TimeLineEventViewSet, basename='knowledge-base-timeline-events')
