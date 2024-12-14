# """
# ASGI config for dx_backend project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """
#
# import os
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dx_backend.settings")
#
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
#
# from apps.adapters.channels_adapter import routing
#
#
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })