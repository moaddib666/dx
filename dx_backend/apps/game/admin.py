from django.contrib import admin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import messages

from apps.core.utils.models import TagsDescriptor
from apps.game.services.clone.clone import PolymorphicCloneService
from apps.game.services.clone.clone_strategy import CampaignCloneStrategy
from apps.game.services.clone.filter import TaggedContextFilter
from apps.game.services.clone.hook import SaveCloneHook
from apps.game.services.clone.new import InstanceDependencyGraph, InstanceDeepCloner
from apps.game.services.clone.present import DependencyGraphPresenter, ShapeDistiller
from apps.game.services.clone.rel_fix import get_default_relation_updater

from .models import Campaign, Session, CampaignStartItem


class CampaignStartItemInline(admin.TabularInline):
    """
    Inline admin for managing campaign start items directly from campaign admin.
    """
    model = CampaignStartItem
    extra = 1
    fields = ('item', 'quantity', 'chance', 'get_item_preview')
    readonly_fields = ('get_item_preview',)
    
    def get_item_preview(self, obj):
        """Display item preview with icon and basic info"""
        if not obj.item:
            return format_html('<span style="color: #999;">No item selected</span>')
            

        # Icon preview
        icon_html = ''
        if obj.item.icon and hasattr(obj.item.icon, 'url'):
            icon_html = format_html(
                '<img src="{}" style="height: 30px; width: 30px; border-radius: 3px; '
                'object-fit: cover; margin-right: 8px; vertical-align: middle;" alt="Item Icon" />',
                obj.item.icon.url
            )
        
        return format_html(
            '<div style="display: flex; align-items: center;">'
            '<div>'
            '<strong>{} {}</strong><br>'
            '</div>'
            '</div>',
            icon_html,
            obj.item.type.title(),
        )
    
    get_item_preview.short_description = 'Item Preview'


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """
    Admin interface for Campaign model.
    """
    list_display = ('name', 'description', 'is_active', 'is_completed', 'get_masters_count', 'get_players_count',
                    'display_background_image', 'view_characters', 'manage_start_items', 'clone_campaign')
    list_filter = ('is_active', 'is_completed', 'masters', 'players')
    filter_horizontal = ('masters', 'players')
    search_fields = ('name', 'description')
    inlines = [CampaignStartItemInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'background_image', 'start_position')
        }),
        ('Status', {
            'fields': ('is_active', 'is_completed', "default", "auto_play")
        }),
        ('Participants', {
            'fields': ('masters', 'players')
        }),
    )

    def get_masters_count(self, obj):
        """Get the number of masters for this campaign"""
        return obj.masters.count()

    get_masters_count.short_description = 'Masters'

    def get_players_count(self, obj):
        """Get the number of players for this campaign"""
        return obj.players.count()

    get_players_count.short_description = 'Players'

    def display_background_image(self, obj):
        """Display the background image as a thumbnail"""
        if obj.background_image and hasattr(obj.background_image, 'url'):
            return format_html(
                '<img src="{}" width="100" height="auto" style="object-fit: cover; border-radius: 4px;" />',
                obj.background_image.url
            )
        return format_html('<span style="color: #999;">No image</span>')

    display_background_image.short_description = 'Background Image'

    def view_characters(self, obj):
        """Button to view characters in this campaign"""
        return format_html(
            '<a class="button" style="display: inline-block; padding: 6px 10px; margin: 0 2px; '
            'background: #007bff; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 12px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2); white-space: nowrap; overflow: visible;" href="{}">'
            '<span style="margin-right: 4px;">👥</span>Characters</a>',
            f"/admin/character/character/?gameobject_ptr__campaign__id__exact={obj.pk}"
        )

    view_characters.short_description = 'Characters'

    def manage_start_items(self, obj):
        """Button to manage start items for this campaign"""
        start_items_count = obj.start_items.count()
        return format_html(
            '<a class="button" style="display: inline-block; padding: 6px 10px; margin: 0 2px; '
            'background: #17a2b8; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 12px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2); white-space: nowrap; overflow: visible;" href="{}">'
            '<span style="margin-right: 4px;">🎒</span>Start Items ({})</a>',
            f"/admin/game/campaignstartitem/?campaign__id__exact={obj.pk}",
            start_items_count
        )

    manage_start_items.short_description = 'Start Items'

    def clone_campaign(self, obj):
        """Button to clone a campaign"""
        return format_html(
            '<a class="button" style="display: inline-block; padding: 6px 10px; margin: 0 2px; '
            'background: #4CAF50; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 12px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2); white-space: nowrap; overflow: visible;" href="{}">'
            '<span style="margin-right: 4px;">🔄</span>Clone</a>',
            reverse('admin:clone_campaign', args=[obj.pk])
        )

    clone_campaign.short_description = 'Clone'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/clone/',
                self.admin_site.admin_view(self.clone_campaign_view),
                name='clone_campaign',
            ),
            path(
                '<path:object_id>/clone/preview/',
                self.admin_site.admin_view(self.clone_campaign_preview),
                name='clone_campaign_preview',
            ),
            path(
                '<path:object_id>/clone/execute/',
                self.admin_site.admin_view(self.clone_campaign_execute),
                name='clone_campaign_execute',
            ),
            path(
                '<path:object_id>/clone/graph/',
                self.admin_site.admin_view(self.clone_campaign_graph),
                name='clone_campaign_graph',
            ),
        ]
        return custom_urls + urls

    def clone_campaign_view(self, request, object_id):
        """View to show clone campaign options"""
        campaign = self.get_object(request, object_id)
        if campaign is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, object_id)

        context = {
            'title': f'Clone Campaign: {campaign.name}',
            'campaign': campaign,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'preview_url': reverse('admin:clone_campaign_preview', args=[campaign.pk]),
            'execute_url': reverse('admin:clone_campaign_execute', args=[campaign.pk]),
            'graph_url': reverse('admin:clone_campaign_graph', args=[campaign.pk]),
        }
        return render(request, 'admin/game/campaign/clone_campaign.html', context)

    def clone_campaign_preview(self, request, object_id):
        """View to preview campaign dependencies before cloning"""
        campaign = self.get_object(request, object_id)
        if campaign is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, object_id)

        # Create dependency graph
        graph = InstanceDependencyGraph(
            campaign,
            model_filter=TaggedContextFilter(tag=TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
        )
        dependencies = graph.discover()

        # Analyze dependencies
        presenter = DependencyGraphPresenter(dependencies, distiller=ShapeDistiller())
        analysis = presenter.analyze_graph()

        # Count models by type
        model_counts = {}
        for dep in dependencies:
            model_name = dep.target.__class__.__name__
            if model_name not in model_counts:
                model_counts[model_name] = 0
            model_counts[model_name] += 1

        # Sort model counts by count (descending)
        model_counts = {k: v for k, v in sorted(model_counts.items(), key=lambda item: item[1], reverse=True)}

        # Add model counts to analysis
        analysis['model_counts'] = model_counts

        context = {
            'title': f'Clone Campaign Preview: {campaign.name}',
            'campaign': campaign,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'dependencies': dependencies,
            'dependency_count': len(dependencies),
            'analysis': analysis,
            'execute_url': reverse('admin:clone_campaign_execute', args=[campaign.pk]),
            'graph_url': reverse('admin:clone_campaign_graph', args=[campaign.pk]),
        }
        return render(request, 'admin/game/campaign/clone_campaign_preview.html', context)

    def clone_campaign_graph(self, request, object_id):
        """View to show dependency graph visualization"""
        campaign = self.get_object(request, object_id)
        if campaign is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, object_id)

        # Create dependency graph
        graph = InstanceDependencyGraph(
            campaign,
            model_filter=TaggedContextFilter(tag=TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
        )
        dependencies = graph.discover()

        # Generate graph image
        presenter = DependencyGraphPresenter(dependencies, distiller=ShapeDistiller())
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name

        presenter.render_image(output_path=os.path.splitext(tmp_path)[0], format="png",
                               show_weights=True, color_by_layer=True)

        with open(tmp_path, 'rb') as f:
            image_data = f.read()

        # Clean up the temporary file
        os.unlink(tmp_path)

        response = HttpResponse(content_type='image/png')
        response.write(image_data)
        return response

    def clone_campaign_execute(self, request, object_id):
        """View to execute campaign cloning"""
        campaign = self.get_object(request, object_id)
        if campaign is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, object_id)

        # Create dependency graph
        graph = InstanceDependencyGraph(
            campaign,
            model_filter=TaggedContextFilter(tag=TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
        )
        dependencies = graph.discover()

        try:
            with transaction.atomic():
                # Clone campaign with dependencies
                cloner = InstanceDeepCloner(
                    root_instance=campaign,
                    dependencies=dependencies,
                    strategy=CampaignCloneStrategy(
                        cloner=PolymorphicCloneService(),
                        fixer=get_default_relation_updater(),
                        hook=SaveCloneHook(),
                    )
                )
                cloner.clone()

                # The root_instance attribute of the cloner contains the cloned campaign
                new_campaign = cloner.root_instance

                messages.success(request,
                                 f'Campaign "{campaign.name}" was successfully cloned to "{new_campaign.name}"')
                return HttpResponseRedirect(
                    reverse('admin:game_campaign_change', args=(new_campaign.pk,))
                )
        except Exception as e:
            messages.error(request, f'Error cloning campaign: {str(e)}')
            return HttpResponseRedirect(
                reverse('admin:game_campaign_change', args=(campaign.pk,))
            )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """
    Admin interface for Session model.
    """
    list_display = ('client', 'character')
    list_filter = ('client',)
    search_fields = ('client__name', 'character__name')


@admin.register(CampaignStartItem)
class CampaignStartItemAdmin(admin.ModelAdmin):
    """
    Admin interface for CampaignStartItem model.
    Provides comprehensive management of campaign start items with icons and good representation.
    """
    list_display = (
        'campaign', 'get_item_name', 'get_item_type', 'quantity', 'chance_percentage', 
        'icon_preview', 'get_item_price', 'view_item_details'
    )
    list_filter = ('campaign', 'item__type', 'item__canonical')
    search_fields = ('campaign__name', 'item__name', 'item__description')
    list_per_page = 25
    
    fieldsets = (
        (None, {
            'fields': ('campaign', 'item', 'quantity', 'chance')
        }),
        ('Item Preview', {
            'fields': ('icon_preview', 'get_item_details'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('id', 'created_at', 'updated_at', 'icon_preview', 'get_item_details')

    def get_item_name(self, obj):
        """Get the item name with emoji icon based on type"""
        type_icons = {
            'weapon': '⚔️',
            'armor': '🛡️',
            'consumable': '🧪',
            'tool': '🔧',
            'misc': '📦',
            'quest': '📜',
            'key': '🗝️',
        }
        icon = type_icons.get(obj.item.type.lower(), '📦')
        return format_html(
            '<span style="font-weight: bold;">{} {}</span>',
            icon, obj.item.name
        )
    get_item_name.short_description = 'Item Name'
    get_item_name.admin_order_field = 'item__name'

    def get_item_type(self, obj):
        """Get the item type with colored badge"""
        type_colors = {
            'weapon': '#dc3545',
            'armor': '#6c757d', 
            'consumable': '#28a745',
            'tool': '#ffc107',
            'misc': '#17a2b8',
            'quest': '#6f42c1',
            'key': '#fd7e14',
        }
        color = type_colors.get(obj.item.type.lower(), '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold; '
            'text-transform: uppercase;">{}</span>',
            color, obj.item.type
        )
    get_item_type.short_description = 'Type'
    get_item_type.admin_order_field = 'item__type'

    def chance_percentage(self, obj):
        """Display chance as percentage with color coding"""
        percentage = obj.chance * 100
        if percentage >= 90:
            color = '#28a745'  # Green for high chance
        elif percentage >= 50:
            color = '#ffc107'  # Yellow for medium chance
        else:
            color = '#dc3545'  # Red for low chance
            
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, percentage
        )
    chance_percentage.short_description = 'Chance'
    chance_percentage.admin_order_field = 'chance'

    def icon_preview(self, obj):
        """Display the item icon as a thumbnail"""
        if obj.item.icon and hasattr(obj.item.icon, 'url'):
            return format_html(
                '<img src="{}" style="height: 50px; width: 50px; border-radius: 5px; '
                'object-fit: cover; border: 2px solid #ddd;" alt="Item Icon" />',
                obj.item.icon.url
            )
        return format_html(
            '<div style="height: 50px; width: 50px; border-radius: 5px; '
            'background-color: #f8f9fa; border: 2px solid #ddd; '
            'display: flex; align-items: center; justify-content: center; '
            'font-size: 20px;">📦</div>'
        )
    icon_preview.short_description = 'Icon'

    def get_item_price(self, obj):
        """Display item base price with currency symbol"""
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">💰 {}</span>',
            obj.item.base_price
        )
    get_item_price.short_description = 'Base Price'
    get_item_price.admin_order_field = 'item__base_price'

    def view_item_details(self, obj):
        """Button to view item details"""
        return format_html(
            '<a class="button" style="display: inline-block; padding: 4px 8px; margin: 0 2px; '
            'background: #007bff; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 11px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2);" href="{}" target="_blank">'
            '<span style="margin-right: 4px;">🔍</span>View Item</a>',
            f"/admin/items/item/{obj.item.pk}/change/"
        )
    view_item_details.short_description = 'Actions'

    def get_item_details(self, obj):
        """Display detailed item information in readonly field"""
        if not obj.item:
            return "No item selected"
            
        details = []
        details.append(f"<strong>Name:</strong> {obj.item.name}")
        details.append(f"<strong>Type:</strong> {obj.item.type}")
        details.append(f"<strong>Weight:</strong> {obj.item.weight} kg")
        details.append(f"<strong>Base Price:</strong> {obj.item.base_price}")
        details.append(f"<strong>Charges:</strong> {obj.item.charges}")
        
        if obj.item.description:
            details.append(f"<strong>Description:</strong> {obj.item.description[:200]}{'...' if len(obj.item.description) > 200 else ''}")
            
        if obj.item.skill:
            details.append(f"<strong>Associated Skill:</strong> {obj.item.skill}")
            
        if obj.item.effect:
            details.append(f"<strong>Effect:</strong> {obj.item.effect}")
            
        return format_html('<br>'.join(details))
    get_item_details.short_description = 'Item Details'
