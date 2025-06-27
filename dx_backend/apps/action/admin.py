from django.contrib import admin
from django.db import models

from apps.core.admin import CampaignModelAdmin
from .models import Cycle, DiceRollResult, SpecialAction


@admin.register(Cycle)
class CycleAdmin(CampaignModelAdmin):
    list_display = ('id', 'campaign', 'created_at', 'updated_at')  # Display the cycle details
    list_filter = ('campaign',)
    actions = ['start_new_cycle']

    def start_new_cycle(self, request, queryset):
        """
        Custom action to start a new cycle.
        """
        # Get the campaign from the session
        campaign_id = request.session.get('campaign_id')
        if campaign_id:
            from apps.game.models import Campaign
            campaign = Campaign.objects.get(id=campaign_id)
            Cycle.objects.next_cycle(campaign=campaign)
            self.message_user(request, "New cycle has been started.")
        else:
            # No campaign in session, show an error message
            self.message_user(request, "Cannot start a new cycle without a campaign. Please select a campaign first.",
                              level='error')

    start_new_cycle.short_description = "Start a new cycle"


from django.contrib import admin
from django.utils.html import format_html
from .models import CharacterAction, ActionImpact, Cycle


class ActionImpactInline(admin.TabularInline):
    model = ActionImpact
    extra = 0
    readonly_fields = ('action', 'target', 'type', 'violation', 'size', 'dice_roll_result')


@admin.register(CharacterAction)
class CharacterActionAdmin(CampaignModelAdmin):
    list_display = (
        'id', 'cycle_group', 'action_type', 'initiator', 'position_id', 'accepted', 'performed', 
        'created_at')
    list_filter = ('accepted', 'action_type', 'cycle', 'cycle__campaign')  # Filter by cycle and cycle's campaign
    search_fields = ('initiator__name', 'data')
    actions = ['approve_selected_actions']
    inlines = [ActionImpactInline]

    def cycle_group(self, obj):
        """
        Display the cycle ID and visually distinguish the current cycle.
        """
        # Get the campaign from the object's cycle
        campaign = obj.cycle.campaign if obj.cycle else None
        current_cycle = Cycle.objects.current(campaign=campaign)
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
        Override queryset to annotate whether actions are in the current cycle
        and filter by campaign.
        """
        qs = super().get_queryset(request)

        # Get the campaign from the session
        campaign_id = request.session.get('campaign_id')
        campaign = None
        if campaign_id:
            from apps.game.models import Campaign
            campaign = Campaign.objects.get(id=campaign_id)
            # Filter by campaign through cycle relationship
            qs = qs.filter(cycle__campaign_id=campaign_id)

        current_cycle = Cycle.objects.current(campaign=campaign)
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
class ActionImpactAdmin(CampaignModelAdmin):
    list_display = ('id', 'action', 'target', 'type', 'violation', 'size', 'dice_roll_result')
    list_filter = ('type', 'violation', 'action__cycle__campaign')
    search_fields = ('action__data', 'target__name')

    def get_queryset(self, request):
        """
        Override to filter by campaign through action -> cycle -> campaign relationship.
        """
        qs = super().get_queryset(request)
        campaign_id = request.session.get('campaign_id')

        if campaign_id:
            return qs.filter(action__cycle__campaign_id=campaign_id)

        return qs


@admin.register(DiceRollResult)
class DiceRollResultAdmin(CampaignModelAdmin):
    list_display = ('id', 'dice_side', 'multiplier', 'outcome')
    list_filter = ('outcome', 'actionimpact__action__cycle__campaign')
    search_fields = ('outcome',)

    def get_queryset(self, request):
        """
        Override to filter by campaign through actionimpact -> action -> cycle -> campaign relationship.
        """
        qs = super().get_queryset(request)
        campaign_id = request.session.get('campaign_id')

        if campaign_id:
            return qs.filter(actionimpact__action__cycle__campaign_id=campaign_id).distinct()

        return qs


@admin.register(SpecialAction)
class SpecialActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'final', 'immediate', 'icon_preview',)
    list_filter = ('immediate', 'final')
    search_fields = ('action_type', 'description')
    readonly_fields = ('icon_preview', 'formatted_cost')  # Preview and formatted cost in detail view

    def icon_preview(self, obj):
        """
        Display a thumbnail preview of the icon.
        """
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.icon.url
            )
        return "No Icon"

    icon_preview.short_description = "Icon Preview"

    def formatted_cost(self, obj):
        """
        Display the cost in a readable format.
        """
        if not obj.cost:
            return "No Cost"
        return format_html(
            '<ul>{}</ul>',
            ''.join(f'<li>{cost["kind"]}: {cost["value"]}</li>' for cost in obj.cost)
        )

    formatted_cost.short_description = "Cost"

    def get_fieldsets(self, request, obj=None):
        """
        Organize the fields for better UX.
        """
        fieldsets = [
            (None, {
                'fields': (
                'action_type', 'name', 'description', 'immediate', 'final', 'cost', 'formatted_cost', 'icon',
                'icon_preview'),
            }),
        ]
        return fieldsets

    class Media:
        """
        Add any custom CSS or JS for enhanced UI/UX.
        """
        css = {
            'all': ('admin/custom_admin.css',),
        }
