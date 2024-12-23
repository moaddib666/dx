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

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/google/', include('allauth.socialaccount.urls')),
    # JWT
    path('auth/jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ##
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('core/', include('apps.core.urls')),
    path('client/', include('apps.client.urls')),
    path('player/', include('apps.player.urls')),
    path('school/', include('apps.school.urls')),
    path('world/', include('apps.world.urls')),
    path('fight/', include('apps.fight.urls')),
    path('skills/', include('apps.skills.urls')),
    path('action/', include('apps.action.urls')),
    path('items/', include('apps.items.urls')),
    path('currency/', include('apps.currency.urls')),
    path('modificators/', include('apps.modificators.urls')),
    path('adapters/centrifugo/', include('apps.adapters.centrifugo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
