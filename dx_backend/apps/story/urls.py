from django.urls import path, include
from apps.story.api.routers import urlpatterns as api_urlpatterns

urlpatterns = [
    path('', include(api_urlpatterns)),
]
