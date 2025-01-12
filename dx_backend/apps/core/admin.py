from django.apps import apps
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from apps.core.models import GameObject, StatObject, ViolationObject


@admin.register(GameObject)
class BaseModelAdmin(PolymorphicParentModelAdmin):
    base_model = GameObject
    list_filter = (PolymorphicChildModelFilter,)  # Optional

    def get_child_models(self):
        Character = apps.get_model('character.Character')
        return (Character,)


@admin.register(StatObject)
class StatObjectAdmin(admin.ModelAdmin):
    base_model = StatObject
    list_filter = (PolymorphicChildModelFilter,)  # Optional

    def get_child_models(self,):
        return []

    def get_child_type_choices(self,*args, **kwargs):
        return []

@admin.register(ViolationObject)
class ViolationObjectAdmin(admin.ModelAdmin):
    base_model = ViolationObject
    list_filter = (PolymorphicChildModelFilter,)

    def get_child_models(self,):
        return []

    def get_child_type_choices(self,*args, **kwargs):
        return []