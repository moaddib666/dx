from django.apps import AppConfig


class WebsocketAdapterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.adapters.channels_adapter"
