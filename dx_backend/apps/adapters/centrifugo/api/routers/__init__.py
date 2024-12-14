from rest_framework.routers import DefaultRouter

from ...api.views.openai import CentrifugoViewSet


OpenAPIRouter = DefaultRouter()
OpenAPIRouter.register('', CentrifugoViewSet, basename='centrifugo')
