from django.urls import include, path

from .api.routers import router, school_router

urlpatterns = [
    path('', include(router.urls)),
    path('', include(school_router.urls)),
]