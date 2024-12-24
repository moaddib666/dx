from django.contrib import admin
from .models import CharacterAction, ActionImpact, DiceRollResult

@admin.register(CharacterAction)
class CharacterActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'initiator', 'skill', 'target_dimension', 'target_location')
    list_filter = ('action_type', 'initiator')
    search_fields = ('initiator__name', 'targets__name')
    filter_horizontal = ('targets',)

@admin.register(ActionImpact)
class ActionImpactAdmin(admin.ModelAdmin):
    list_display = ('action', 'target', 'type', 'violation', 'size', 'dice_roll_result')
    list_filter = ('type', 'violation', 'target')
    search_fields = ('action__initiator__name', 'target__name')

@admin.register(DiceRollResult)
class DiceRollResultAdmin(admin.ModelAdmin):
    list_display = ('dice_side', 'multiplier', 'outcome')
    list_filter = ('outcome',)
    search_fields = ('outcome',)
