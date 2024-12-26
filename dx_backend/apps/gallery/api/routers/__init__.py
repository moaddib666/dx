from rest_framework.routers import DefaultRouter

from apps.gallery.api.views.openai import WorldGalleryViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('world', WorldGalleryViewSet, basename='openai-world-gallery')
