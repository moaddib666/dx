from django.urls import include, path

from .api.routers import OpenAIRouter
from .views import health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("", include(OpenAIRouter.urls)),
]