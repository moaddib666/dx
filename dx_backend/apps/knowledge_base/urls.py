from django.urls import include, path

from .api.routers import KnowledgeBaseRouter

urlpatterns = [
    path("", include(KnowledgeBaseRouter.urls)),
]
