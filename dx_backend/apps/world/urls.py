from django.urls import include, path

from .api.routers import router

urlpatterns = [
    path("", include(router.urls)),
]