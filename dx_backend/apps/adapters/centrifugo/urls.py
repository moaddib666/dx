from django.urls import include, path

from .api.routers import OpenAPIRouter

urlpatterns = [
    path("", include(OpenAPIRouter.urls)),
]