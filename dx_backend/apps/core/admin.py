from django.apps import apps
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from apps.core.models import GameObject


@admin.register(GameObject)
class BaseModelAdmin(PolymorphicParentModelAdmin):
    base_model = GameObject
    list_filter = (PolymorphicChildModelFilter,)  # Optional

    def get_child_models(self):
        Character = apps.get_model('character.Character')
        return (Character, )
