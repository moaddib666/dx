from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.game"

    def ready(self):
        import apps.game.signals  # noqa
