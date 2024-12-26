# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin and Jet
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),

    # Authentication
    path('api-auth/', include('rest_framework.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/google/', include('allauth.socialaccount.urls')),
    # JWT Authentication
    path('auth/jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Schema and Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Core APIs
    path('api/core/', include('apps.core.urls')),
    path('api/client/', include('apps.client.urls')),

    # Feature Modules
    path('api/character/', include('apps.character.urls')),
    path('api/school/', include('apps.school.urls')),
    path('api/world/', include('apps.world.urls')),
    path('api/fight/', include('apps.fight.urls')),
    path('api/skills/', include('apps.skills.urls')),
    path('api/action/', include('apps.action.urls')),
    path('api/items/', include('apps.items.urls')),
    path('api/currency/', include('apps.currency.urls')),
    path('api/gallery/', include('apps.gallery.urls')),
    path('api/modificators/', include('apps.modificators.urls')),

    # Adapters
    path('api/adapters/centrifugo/', include('apps.adapters.centrifugo.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
