from django.apps import apps
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter
from apps.core.admin.mixins import CampaignAdminMixin

from apps.core.models import GameObject, StatObject, ViolationObject, DimensionAnomaly, DimensionAnomalyEffect


class AnomalyEffectFilter(SimpleListFilter):
    """Custom filter for DimensionAnomaly effect field with better UI."""
    title = 'Effect Type'
    parameter_name = 'effect_type'

    def lookups(self, request, model_admin):
        return [
            ('positive', 'Positive Effects'),
            ('negative', 'Negative Effects'),
            ('neutral', 'Neutral Effects'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'positive':
            return queryset.filter(effect=DimensionAnomalyEffect.Positive)
        if self.value() == 'negative':
            return queryset.filter(effect=DimensionAnomalyEffect.Negative)
        if self.value() == 'neutral':
            return queryset.filter(effect=DimensionAnomalyEffect.Neutral)
        return queryset


class AnomalyLevelFilter(SimpleListFilter):
    """Custom filter for DimensionAnomaly level field with range options."""
    title = 'Danger Level'
    parameter_name = 'danger_level'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Low Danger (Level 1-3)'),
            ('medium', 'Medium Danger (Level 4-6)'),
            ('high', 'High Danger (Level 7+)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(level__lte=3)
        if self.value() == 'medium':
            return queryset.filter(level__gt=3, level__lte=6)
        if self.value() == 'high':
            return queryset.filter(level__gt=6)
        return queryset


class PositionGridZFilter(SimpleListFilter):
    """Custom filter for DimensionAnomaly position's grid_z field."""
    title = 'Position Z-Level'
    parameter_name = 'grid_z'

    def lookups(self, request, model_admin):
        # Get all unique grid_z values from positions related to anomalies
        grid_z_values = DimensionAnomaly.objects.exclude(
            position__isnull=True
        ).values_list(
            'position__grid_z', flat=True
        ).distinct().order_by('position__grid_z')

        return [(str(z), f'Z-Level {z}') for z in grid_z_values]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__grid_z=self.value())
        return queryset


class DimensionAnomalyForm(ModelForm):
    """Custom form for DimensionAnomaly."""
    class Meta:
        model = DimensionAnomaly
        fields = '__all__'
        exclude = ['id']  # Exclude the id field since it's not editable


@admin.register(GameObject)
class BaseModelAdmin(PolymorphicParentModelAdmin):
    base_model = GameObject
    list_filter = (PolymorphicChildModelFilter,)  # Optional

    def get_child_models(self):
        Character = apps.get_model('character.Character')
        DimensionAnomaly = apps.get_model('world.DimensionAnomaly')
        WorldItem = apps.get_model('items.WorldItem')
        return (Character, DimensionAnomaly, WorldItem)


@admin.register(StatObject)
class StatObjectAdmin(admin.ModelAdmin):
    base_model = StatObject
    list_filter = (PolymorphicChildModelFilter,)  # Optional

    def get_child_models(self, ):
        return []

    def get_child_type_choices(self, *args, **kwargs):
        return []


@admin.register(ViolationObject)
class ViolationObjectAdmin(admin.ModelAdmin):
    base_model = ViolationObject
    list_filter = (PolymorphicChildModelFilter,)

    def get_child_models(self, ):
        return []

    def get_child_type_choices(self, *args, **kwargs):
        return []


@admin.register(DimensionAnomaly)
class DimensionAnomalyAdmin(CampaignAdminMixin, admin.ModelAdmin):
    form = DimensionAnomalyForm
    list_display = ('id', 'colored_effect', 'level_display', 'known_status', 'is_active', 'dimension_link', 'position_link', 'campaign_link', 'created_at', 'updated_at')
    list_filter = (AnomalyEffectFilter, PositionGridZFilter, 'is_active', 'dimension', 'campaign')
    search_fields = ('id', 'effect')
    ordering = ('-created_at', 'level')
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at')
    actions = [
        'mark_as_known', 'mark_as_unknown', 
        'activate_anomalies', 'deactivate_anomalies', 
        'increase_level', 'decrease_level',
        'set_effect_positive', 'set_effect_negative', 'set_effect_neutral',
        'duplicate_anomalies', 'export_as_json'
    ]
    date_hierarchy = 'created_at'
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('effect', 'level', 'known')
        }),
        ('Location Information', {
            'fields': ('position', 'dimension')
        }),
        ('Status', {
            'fields': ('is_active', 'campaign')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        """
        Override to optimize query with select_related for related fields.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('dimension', 'position', 'campaign')

    def colored_effect(self, obj):
        """Display the effect with a color indicator."""
        colors = {
            'Positive': 'green',
            'Negative': 'red',
            'Neutral': 'blue'
        }
        color = colors.get(obj.effect, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.effect)
    colored_effect.short_description = 'Effect'
    colored_effect.admin_order_field = 'effect'

    def known_status(self, obj):
        """Display known status with an icon."""
        if obj.known:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
    known_status.short_description = 'Known'
    known_status.admin_order_field = 'known'

    def dimension_link(self, obj):
        """Display a link to the dimension admin."""
        if obj.dimension:
            return format_html('<a href="{}">{}</a>', 
                reverse('admin:world_dimension_change', args=[obj.dimension.id]), 
                obj.dimension)
        return '-'
    dimension_link.short_description = 'Dimension'
    dimension_link.admin_order_field = 'dimension'

    def position_link(self, obj):
        """Display a link to the position admin."""
        if obj.position:
            return format_html('<a href="{}">{}</a>', 
                reverse('admin:world_position_change', args=[obj.position.id]), 
                obj.position)
        return '-'
    position_link.short_description = 'Position'
    position_link.admin_order_field = 'position'

    def campaign_link(self, obj):
        """Display a link to the campaign admin."""
        if obj.campaign:
            return format_html('<a href="{}">{}</a>', 
                reverse('admin:game_campaign_change', args=[obj.campaign.id]), 
                obj.campaign)
        return '-'
    campaign_link.short_description = 'Campaign'
    campaign_link.admin_order_field = 'campaign'

    def mark_as_known(self, request, queryset):
        """Mark selected anomalies as known."""
        updated = queryset.update(known=True)
        self.message_user(request, f"{updated} anomalies marked as known.")
    mark_as_known.short_description = "Mark selected anomalies as known"

    def mark_as_unknown(self, request, queryset):
        """Mark selected anomalies as unknown."""
        updated = queryset.update(known=False)
        self.message_user(request, f"{updated} anomalies marked as unknown.")
    mark_as_unknown.short_description = "Mark selected anomalies as unknown"

    def activate_anomalies(self, request, queryset):
        """Activate selected anomalies."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} anomalies activated.")
    activate_anomalies.short_description = "Activate selected anomalies"

    def deactivate_anomalies(self, request, queryset):
        """Deactivate selected anomalies."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} anomalies deactivated.")
    deactivate_anomalies.short_description = "Deactivate selected anomalies"

    def level_display(self, obj):
        """Display level with a visual indicator."""
        # Define colors for different level ranges
        if obj.level <= 3:
            color = 'green'
            danger = 'Low'
        elif obj.level <= 6:
            color = 'orange'
            danger = 'Medium'
        else:
            color = 'red'
            danger = 'High'

        # Create a progress bar style indicator
        bar_width = min(obj.level * 10, 100)  # Scale to max 100% width

        return format_html(
            '<div style="display: flex; align-items: center;">'
            '<div style="width: 100px; background-color: #f0f0f0; height: 10px; margin-right: 10px;">'
            '<div style="width: {}%; background-color: {}; height: 10px;"></div>'
            '</div>'
            '<span style="color: {};">Level {} ({} Danger)</span>'
            '</div>',
            bar_width, color, color, obj.level, danger
        )
    level_display.short_description = 'Level'
    level_display.admin_order_field = 'level'

    def increase_level(self, request, queryset):
        """Increase the level of selected anomalies by 1."""
        from django.db.models import F
        updated = queryset.update(level=F('level') + 1)
        self.message_user(request, f"Level increased for {updated} anomalies.")
    increase_level.short_description = "Increase level by 1"

    def decrease_level(self, request, queryset):
        """Decrease the level of selected anomalies by 1, but not below 1."""
        from django.db.models import F, Case, When, Value, IntegerField
        updated = queryset.update(
            level=Case(
                When(level__gt=1, then=F('level') - 1),
                default=F('level'),
                output_field=IntegerField()
            )
        )
        self.message_user(request, f"Level decreased for {updated} anomalies.")
    decrease_level.short_description = "Decrease level by 1"

    def set_effect_positive(self, request, queryset):
        """Set the effect of selected anomalies to Positive."""
        updated = queryset.update(effect=DimensionAnomalyEffect.Positive)
        self.message_user(request, f"Effect set to Positive for {updated} anomalies.")
    set_effect_positive.short_description = "Set effect to Positive"

    def set_effect_negative(self, request, queryset):
        """Set the effect of selected anomalies to Negative."""
        updated = queryset.update(effect=DimensionAnomalyEffect.Negative)
        self.message_user(request, f"Effect set to Negative for {updated} anomalies.")
    set_effect_negative.short_description = "Set effect to Negative"

    def set_effect_neutral(self, request, queryset):
        """Set the effect of selected anomalies to Neutral."""
        updated = queryset.update(effect=DimensionAnomalyEffect.Neutral)
        self.message_user(request, f"Effect set to Neutral for {updated} anomalies.")
    set_effect_neutral.short_description = "Set effect to Neutral"

    def duplicate_anomalies(self, request, queryset):
        """Create duplicates of selected anomalies."""
        count = 0
        for anomaly in queryset:
            # Create a new anomaly with the same attributes
            new_anomaly = DimensionAnomaly.objects.create(
                level=anomaly.level,
                effect=anomaly.effect,
                known=anomaly.known,
                is_active=anomaly.is_active,
                position=anomaly.position,
                dimension=anomaly.dimension,
                campaign=anomaly.campaign
            )
            count += 1

        self.message_user(request, f"Successfully duplicated {count} anomalies.")
    duplicate_anomalies.short_description = "Duplicate selected anomalies"

    def export_as_json(self, request, queryset):
        """Export selected anomalies as JSON."""
        import json
        from django.http import HttpResponse
        from django.core.serializers.json import DjangoJSONEncoder

        # Prepare data for serialization
        anomalies_data = []
        for anomaly in queryset:
            anomaly_data = {
                'id': str(anomaly.id),
                'level': anomaly.level,
                'effect': anomaly.effect,
                'known': anomaly.known,
                'is_active': anomaly.is_active,
                'position_id': str(anomaly.position.id) if anomaly.position else None,
                'dimension_id': str(anomaly.dimension.id) if anomaly.dimension else None,
                'campaign_id': str(anomaly.campaign.id) if anomaly.campaign else None,
                'created_at': anomaly.created_at.isoformat() if anomaly.created_at else None,
                'updated_at': anomaly.updated_at.isoformat() if anomaly.updated_at else None,
            }
            anomalies_data.append(anomaly_data)

        # Create the HTTP response with JSON content
        response = HttpResponse(
            json.dumps(anomalies_data, cls=DjangoJSONEncoder, indent=4),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="anomalies_export.json"'

        return response
    export_as_json.short_description = "Export selected anomalies as JSON"
