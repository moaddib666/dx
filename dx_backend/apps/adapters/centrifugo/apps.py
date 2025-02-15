from django.apps import AppConfig


class CentrifugoAdapterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.adapters.centrifugo"

    def ready(self):
        from apps.core.bus import setup_publisher
        from apps.adapters.centrifugo.publisher import CENTRIFUGO_PUBLISHER
        setup_publisher(CENTRIFUGO_PUBLISHER)
