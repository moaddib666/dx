from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.core.admin import CampaignModelAdmin
from ..models import Fight, CharactersPendingJoinFight


class PendingJoinersInline(admin.TabularInline):
    """Inline for displaying pending joiners in a fight."""
    model = CharactersPendingJoinFight
    verbose_name = "Pending Joiner"
    verbose_name_plural = "Pending Joiners"
    extra = 0
    readonly_fields = ('character_link', 'cycle_display')
    fields = ('character_link', 'cycle_display')

    def character_link(self, obj):
        """Display a link to the character admin."""
        if obj.character:
            url = reverse('admin:character_character_change', args=[obj.character.pk])
            return format_html('<a href="{}">{}</a>', url, obj.character.name)
        return '-'

    character_link.short_description = 'Character'

    def cycle_display(self, obj):
        """Display the cycle when the character was added to pending."""
        if obj.cycle:
            return f"Cycle {obj.cycle.number}"
        return '-'

    cycle_display.short_description = 'Added in Cycle'


@admin.register(Fight)
class FightAdmin(CampaignModelAdmin):
    """
    Admin interface for Fight model with comprehensive management capabilities.
    """

    # List view configuration
    list_display = (
        'id',
        'status_indicator',
        'position_link',
        'attacker_link',
        'defender_link',
        'current_round',
        'pending_joiners_count',
        'duration_display',
        'campaign_display'
    )

    list_filter = (
        'open',
        'duel',
        'current_round',
        'campaign',
        'created_at',
        'updated_at'
    )

    search_fields = (
        'attacker__name',
        'defender__name',
        'position_id',
        'position__sub_location__name',
        'position__sub_location__location__name'
    )

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'duration_display',
        'participants_summary',
        'fight_details',
        'related_actions_link'
    )

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'open',
                'duel',
                'current_round'
            )
        }),
        ('Participants', {
            'fields': (
                'attacker',
                'defender',
                'participants_summary'
            )
        }),
        ('Location & Timing', {
            'fields': (
                'position',
                'created',
                'ended_at',
                'duration_display'
            )
        }),
        ('Fight Details', {
            'fields': (
                'fight_details',
                'related_actions_link'
            ),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )

    inlines = [PendingJoinersInline]

    actions = ['close_fights', 'reopen_fights', 'force_next_round']

    # Custom methods for display
    def status_indicator(self, obj):
        """Display a colored status indicator."""
        if obj.open:
            return format_html(
                '<span style="color: green; font-weight: bold;">&#8226;</span> Active'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">&#8226;</span> Closed'
            )

    status_indicator.short_description = 'Status'
    status_indicator.admin_order_field = 'open'

    def position_link(self, obj):
        """Display a link to the position admin."""
        if obj.position:
            url = reverse('admin:world_position_change', args=[obj.position.pk])
            position_name = f"{obj.position.sub_location.name} - {obj.position.coordinates}"
            return format_html('<a href="{}">{}</a>', url, position_name)
        return '-'

    position_link.short_description = 'Position'
    position_link.admin_order_field = 'position__sub_location__name'

    def attacker_link(self, obj):
        """Display a link to the attacker's character admin."""
        if obj.attacker:
            url = reverse('admin:character_character_change', args=[obj.attacker.pk])
            return format_html(
                '<a href="{}" style="color: #d63384; font-weight: bold;">{}</a>',
                url, obj.attacker.name
            )
        return '-'

    attacker_link.short_description = 'Attacker'
    attacker_link.admin_order_field = 'attacker__name'

    def defender_link(self, obj):
        """Display a link to the defender's character admin."""
        if obj.defender:
            url = reverse('admin:character_character_change', args=[obj.defender.pk])
            return format_html(
                '<a href="{}" style="color: #198754; font-weight: bold;">{}</a>',
                url, obj.defender.name
            )
        return '-'

    defender_link.short_description = 'Defender'
    defender_link.admin_order_field = 'defender__name'

    def pending_joiners_count(self, obj):
        """Display the count of pending joiners."""
        count = obj.pending_joiners.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
                count
            )
        return '0'

    pending_joiners_count.short_description = 'Pending'

    def duration_display(self, obj):
        """Display the fight duration."""
        if obj.created and obj.ended_at:
            return f"Rounds {obj.created.number} - {obj.ended_at.number}"
        elif obj.created:
            return f"Started at round {obj.created.number}"
        return '-'

    duration_display.short_description = 'Duration'

    def campaign_display(self, obj):
        """Display the campaign name."""
        if obj.campaign:
            return obj.campaign.name
        return '-'

    campaign_display.short_description = 'Campaign'
    campaign_display.admin_order_field = 'campaign__name'

    def participants_summary(self, obj):
        """Display a comprehensive participants summary."""
        html_parts = []

        # Main participants
        if obj.attacker:
            html_parts.append(
                f'<strong>Attacker:</strong> '
                f'<a href="{reverse("admin:character_character_change", args=[obj.attacker.pk])}">'
                f'{obj.attacker.name}</a>'
            )

        if obj.defender:
            html_parts.append(
                f'<strong>Defender:</strong> '
                f'<a href="{reverse("admin:character_character_change", args=[obj.defender.pk])}">'
                f'{obj.defender.name}</a>'
            )

        # Pending joiners
        pending_records = obj.pending_joiners.all()
        if pending_records:
            joiner_links = []
            for pending_record in pending_records:
                character = pending_record.character
                joiner_links.append(
                    f'<a href="{reverse("admin:character_character_change", args=[character.pk])}">'
                    f'{character.name}</a>'
                )
            html_parts.append(f'<strong>Pending:</strong> {", ".join(joiner_links)}')

        return mark_safe('<br>'.join(html_parts)) if html_parts else '-'

    participants_summary.short_description = 'All Participants'

    def fight_details(self, obj):
        """Display detailed fight information."""
        details = []

        # Fight type
        fight_type = "Duel" if obj.duel else "Group Fight"
        details.append(f'<strong>Type:</strong> {fight_type}')

        # Position details
        if obj.position:
            position_details = []
            if hasattr(obj.position, 'sub_location') and obj.position.sub_location:
                position_details.append(f'Sub-location: {obj.position.sub_location.name}')
                if hasattr(obj.position.sub_location, 'location') and obj.position.sub_location.location:
                    position_details.append(f'Location: {obj.position.sub_location.location.name}')

            if position_details:
                details.append(f'<strong>Location:</strong> {" → ".join(position_details)}')

        # Timing
        if obj.created:
            details.append(f'<strong>Started:</strong> Cycle {obj.created.number}')
        if obj.ended_at:
            details.append(f'<strong>Ended:</strong> Cycle {obj.ended_at.number}')

        return mark_safe('<br>'.join(details)) if details else '-'

    fight_details.short_description = 'Fight Details'

    def related_actions_link(self, obj):
        """Display a link to related actions."""
        # Count related actions
        from apps.action.models import CharacterAction
        actions_count = CharacterAction.objects.filter(fight=obj).count()

        if actions_count > 0:
            # Create a link to filtered actions admin
            url = reverse('admin:action_characteraction_changelist')
            return format_html(
                '<a href="{}?fight__exact={}" target="_blank">{} related actions &rarr;</a>',
                url, obj.pk, actions_count
            )
        return 'No related actions'

    related_actions_link.short_description = 'Related Actions'

    # Custom admin actions
    def close_fights(self, request, queryset):
        """Close selected fights."""
        count = 0
        for fight in queryset.filter(open=True):
            fight.open = False
            fight.save()
            count += 1

        self.message_user(
            request,
            f'Successfully closed {count} fight(s).'
        )

    close_fights.short_description = 'Close selected fights'

    def reopen_fights(self, request, queryset):
        """Reopen selected fights."""
        count = 0
        for fight in queryset.filter(open=False):
            fight.open = True
            fight.ended_at = None
            fight.save()
            count += 1

        self.message_user(
            request,
            f'Successfully reopened {count} fight(s).'
        )

    reopen_fights.short_description = 'Reopen selected fights'

    def force_next_round(self, request, queryset):
        """Advance selected fights to the next round."""
        count = 0
        for fight in queryset.filter(open=True):
            fight.current_round += 1
            fight.save()
            count += 1

        self.message_user(
            request,
            f'Successfully advanced {count} fight(s) to the next round.'
        )

    force_next_round.short_description = 'Advance to next round'

    # Optimize queries
    def get_queryset(self, request):
        """Optimize the queryset with proper prefetching."""
        return super().get_queryset(request).select_related(
            'campaign',
            'position',
            'position__sub_location',
            'position__sub_location__location',
            'attacker',
            'defender',
            'created',
            'ended_at'
        ).prefetch_related(
            'pending_join'
        )

    # Custom filtering
    def get_search_results(self, request, queryset, search_term):
        """Enhanced search functionality."""
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        # Add custom search logic if needed
        try:
            # Search by fight ID
            if search_term.isdigit():
                queryset |= self.model.objects.filter(id=int(search_term))
        except (ValueError, TypeError):
            pass

        return queryset, use_distinct


# Register any additional admin configurations if needed
admin.site.site_header = "DX Game Admin"
admin.site.site_title = "DX Game Admin Portal"
admin.site.index_title = "Welcome to DX Game Administration"
