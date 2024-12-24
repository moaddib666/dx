from django.urls import include, path

from .api.routers import OpenAIRouter

urlpatterns = [
    path("", include(OpenAIRouter.urls)),
]