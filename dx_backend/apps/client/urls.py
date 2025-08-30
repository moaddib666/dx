from django.urls import include, path

from .api.routers import OpenAIRouter
from .api.views.oauth import google_oauth_login, google_oauth_url

urlpatterns = [
    path("", include(OpenAIRouter.urls)),
    # Google OAuth endpoints
    path("auth/google/login/", google_oauth_login, name="google_oauth_login"),
    path("auth/google/url/", google_oauth_url, name="google_oauth_url"),
]