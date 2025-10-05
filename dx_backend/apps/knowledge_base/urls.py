from django.urls import path, include
from apps.knowledge_base.api.routers.knowledge_base import urlpatterns as api_urlpatterns

urlpatterns = [
    path('', include(api_urlpatterns)),
]