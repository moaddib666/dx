from django.urls import include, path

from .api.routers import GameMasterRouter

urlpatterns = [
    path("", include(GameMasterRouter.urls)),
]