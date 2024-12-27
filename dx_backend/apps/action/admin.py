from django.contrib import admin
from django.db import models

from .models import Cycle, DiceRollResult


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')  # Display the cycle details
    actions = ['start_new_cycle']

    def start_new_cycle(self, request, queryset):
        """
        Custom action to start a new cycle.
        """
        Cycle.objects.next_cycle()
        self.message_user(request, "New cycle has been started.")

    start_new_cycle.short_description = "Start a new cycle"


from django.contrib import admin
from django.utils.html import format_html
from .models import CharacterAction, ActionImpact, Cycle


class ActionImpactInline(admin.TabularInline):
    model = ActionImpact
    extra = 0
    readonly_fields = ('action', 'target', 'type', 'violation', 'size', 'dice_roll_result')


@admin.register(CharacterAction)
class CharacterActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cycle_group', 'action_type', 'initiator', 'position_id', 'accepted', 'performed', 'created_at')
    list_filter = ('accepted', 'action_type', 'cycle')  # Filter by cycle
    search_fields = ('initiator__name', 'data')
    actions = ['approve_selected_actions']
    inlines = [ActionImpactInline]

    def cycle_group(self, obj):
        """
        Display the cycle ID and visually distinguish the current cycle.
        """
        current_cycle = Cycle.objects.current()
        if obj.cycle == current_cycle:
            return format_html(
                '<span style="font-weight: bold; color: green;">Current Cycle {}</span>',
                obj.cycle.id
            )
        return format_html(
            '<span style="color: gray;">Cycle {}</span>',
            obj.cycle.id
        )

    cycle_group.short_description = 'Cycle'

    def position_id(self, obj):
        """
        Display the position ID.
        """
        return obj.position.id if obj.position else "None"

    position_id.short_description = 'Position ID'

    def approve_selected_actions(self, request, queryset):
        """
        Bulk approve selected character actions.
        """
        queryset.update(accepted=True)
        self.message_user(request, f"{queryset.count()} action(s) accepted.")

    approve_selected_actions.short_description = "Approve selected actions"

    def get_queryset(self, request):
        """
        Override queryset to annotate whether actions are in the current cycle.
        """
        qs = super().get_queryset(request)
        current_cycle = Cycle.objects.current()
        return qs.annotate(is_current_cycle=models.Case(
            models.When(cycle=current_cycle, then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField(),
        ))

    def get_row_css(self, obj):
        """
        Add a CSS class to gray out rows for non-current cycles.
        """
        return "non-current-cycle" if not obj.is_current_cycle else ""

    def get_changelist_instance(self, request):
        """
        Attach custom CSS class logic to rows.
        """
        cl = super().get_changelist_instance(request)
        cl.row_attrs = {'class': lambda obj: self.get_row_css(obj)}
        return cl

    class Media:
        """
        Include custom styles to gray out rows for non-current cycles.
        """
        css = {
            'all': ('admin/custom_admin.css',),  # Link to the custom CSS file
        }


@admin.register(ActionImpact)
class ActionImpactAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'target', 'type', 'violation', 'size', 'dice_roll_result')
    list_filter = ('type', 'violation')
    search_fields = ('action__data', 'target__name')


@admin.register(DiceRollResult)
class DiceRollResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'dice_side', 'multiplier', 'outcome')
    list_filter = ('outcome',)
    search_fields = ('outcome',)
