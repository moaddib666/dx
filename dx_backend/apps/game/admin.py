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

from .models import Campaign, Session


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """
    Admin interface for Campaign model.
    """
    list_display = ('name', 'description', 'is_active', 'is_completed', 'clone_campaign')
    list_filter = ('is_active', 'is_completed')
    search_fields = ('name', 'description')

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
