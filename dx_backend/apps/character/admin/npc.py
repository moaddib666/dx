from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.db import transaction

from apps.core.admin.mixins import CampaignAdminMixin

from apps.character.models.npc import (
    CharacterTemplate, CharacterStatsTemplate, CharacterStatTemplate,
    CharacterBiographyTemplate, CharacterSkillTemplate, CharacterSchoolTemplate,
    CharacterModifierTemplate, CharacterEquipmentTemplate, CharacterNameTemplate
)
from apps.game.services.npc.factory.default import NPCFactory
from apps.game.services.npc.factory.interface import NPCFactoryConfig


class CharacterStatTemplateInline(admin.TabularInline):
    model = CharacterStatTemplate
    extra = 1
    fields = ('stat', 'value')


@admin.register(CharacterStatsTemplate)
class CharacterStatsTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stats_summary')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'stats_visualization'),
            'description': 'Define a reusable set of character statistics.'
        }),
    )
    readonly_fields = ('stats_visualization',)
    inlines = [CharacterStatTemplateInline]

    def stats_summary(self, obj):
        """Display a compact summary of key stats in the list view"""
        stats = obj.get_all_stats()
        key_stats = ['PHYSICAL_STRENGTH', 'MENTAL_STRENGTH', 'SPEED', 'INTELLIGENCE']

        summary = []
        for stat in key_stats:
            if stat in stats:
                summary.append(f"{stat.replace('_', ' ').title()}: {stats[stat]}")

        return format_html('<div style="font-size: 12px;">{}</div>', ', '.join(summary))

    stats_summary.short_description = "Key Stats"

    def stats_visualization(self, obj):
        """Display a visual representation of all stats"""
        stats = obj.get_all_stats()

        # Group stats by category
        stat_groups = {
            'Physical': ['PHYSICAL_STRENGTH', 'SPEED', 'ENDURANCE', 'AGILITY'],
            'Mental': ['MENTAL_STRENGTH', 'INTELLIGENCE', 'PERCEPTION', 'WILLPOWER'],
            'Social': ['CHARISMA', 'EMPATHY', 'MANIPULATION', 'COMPOSURE'],
            'Other': []
        }

        # Add any stats that don't fit in the predefined categories to 'Other'
        for stat_name in stats:
            found = False
            for group in stat_groups.values():
                if stat_name in group:
                    found = True
                    break
            if not found:
                stat_groups['Other'].append(stat_name)

        # Generate HTML for each stat group
        html_parts = []
        for group_name, stat_names in stat_groups.items():
            if not stat_names:
                continue

            group_html = f'<div style="margin-bottom: 20px;"><h3 style="margin-bottom: 10px;">{group_name} Stats</h3>'

            for stat_name in stat_names:
                if stat_name in stats:
                    value = stats[stat_name]
                    # Calculate color based on value (green for high, red for low)
                    hue = min(120, max(0, (value - 1) * 120 / 99))  # 0 (red) to 120 (green)
                    color = f'hsl({hue}, 80%, 45%)'

                    # Calculate width based on value (percentage of max)
                    width_percent = value

                    group_html += f'''
                        <div style="margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                                <span style="font-weight: bold;">{stat_name.replace('_', ' ').title()}</span>
                                <span>{value}/100</span>
                            </div>
                            <div style="background-color: #f0f0f0; border-radius: 4px; height: 12px; width: 100%;">
                                <div style="background-color: {color}; width: {width_percent}%; height: 100%; border-radius: 4px;"></div>
                            </div>
                        </div>
                    '''

            group_html += '</div>'
            html_parts.append(group_html)

        return format_html('''
            <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                {}
            </div>
        ''', mark_safe(''.join(html_parts)))

    stats_visualization.short_description = "Stats Visualization"


@admin.register(CharacterBiographyTemplate)
class CharacterBiographyTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'avatar_thumbnail', 'gender', 'randomize_gender', 'age_min', 'age_max')
    search_fields = ('name', 'description', 'background', 'appearance')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Age Settings', {
            'fields': ('age_min', 'age_max'),
            'description': 'Define the age range for characters created from this template.'
        }),
        ('Gender Settings', {
            'fields': ('gender', 'randomize_gender'),
            'description': 'Set a specific gender or enable random gender selection.'
        }),
        ('Appearance & Background', {
            'fields': ('background', 'appearance', 'avatar', 'avatar_preview'),
            'description': 'Define the visual appearance and background story for the character.'
        }),
        ('Randomization', {
            'fields': ('background_variations', 'appearance_variations'),
            'classes': ('collapse',),
            'description': 'Add multiple variations for random selection during character creation.'
        }),
    )
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        """
        Displays the avatar image as a preview in the admin interface.
        """
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />', obj.avatar.url)
        return "No Image Uploaded"

    avatar_preview.short_description = "Avatar Preview"

    def avatar_thumbnail(self, obj):
        """
        Displays a small thumbnail of the avatar in the list view.
        """
        if obj.avatar:
            return format_html('<img src="{}" style="height: 50px; width: 50px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />', obj.avatar.url)
        return "No Image"

    avatar_thumbnail.short_description = "Avatar"


class CharacterSkillTemplateInline(admin.TabularInline):
    model = CharacterSkillTemplate
    extra = 1
    fields = ('skill', 'is_base', 'skill_details')
    readonly_fields = ('skill_details',)
    autocomplete_fields = ['skill']

    def skill_details(self, obj):
        """Display skill details with icon if available"""
        if not obj.pk or not obj.skill:
            return "Save to see skill details"

        icon_html = ""
        if hasattr(obj.skill, 'icon') and obj.skill.icon:
            icon_html = f'<img src="{obj.skill.icon.url}" style="height: 40px; width: 40px; border-radius: 8px; margin-right: 10px;" />'

        return format_html(f'''
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <div style="font-weight: bold;">{obj.skill.name}</div>
                    <div style="font-size: 12px; color: #666;">{obj.skill.description[:100]}{"..." if len(obj.skill.description) > 100 else ""}</div>
                </div>
            </div>
        ''')

    skill_details.short_description = "Skill Details"


class CharacterSchoolTemplateInline(admin.TabularInline):
    model = CharacterSchoolTemplate
    extra = 1
    fields = ('school', 'is_base', 'school_details')
    readonly_fields = ('school_details',)
    autocomplete_fields = ['school']

    def school_details(self, obj):
        """Display school details with icon if available"""
        if not obj.pk or not obj.school:
            return "Save to see school details"

        icon_html = ""
        if hasattr(obj.school, 'icon') and obj.school.icon:
            icon_html = f'<img src="{obj.school.icon.url}" style="height: 40px; width: 40px; border-radius: 8px; margin-right: 10px;" />'

        return format_html(f'''
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <div style="font-weight: bold;">{obj.school.name}</div>
                    <div style="font-size: 12px; color: #666;">{obj.school.description[:100]}{"..." if len(obj.school.description) > 100 else ""}</div>
                </div>
            </div>
        ''')

    school_details.short_description = "School Details"


class CharacterModifierTemplateInline(admin.TabularInline):
    model = CharacterModifierTemplate
    extra = 1
    fields = ('stat', 'value', 'description')
    classes = ('wide',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['stat'].widget.attrs['style'] = 'min-width: 150px;'
        formset.form.base_fields['value'].widget.attrs['style'] = 'width: 80px;'
        formset.form.base_fields['description'].widget.attrs['style'] = 'width: 300px;'
        return formset


class CharacterEquipmentTemplateInline(admin.TabularInline):
    model = CharacterEquipmentTemplate
    extra = 1
    fields = ('item', 'quantity', 'is_equipped', 'item_details')
    readonly_fields = ('item_details',)
    autocomplete_fields = ['item']

    def item_details(self, obj):
        """Display item details with icon if available"""
        if not obj.pk or not obj.item:
            return "Save to see item details"

        icon_html = ""
        if hasattr(obj.item, 'icon') and obj.item.icon:
            icon_html = f'<img src="{obj.item.icon.url}" style="height: 40px; width: 40px; border-radius: 8px; margin-right: 10px;" />'

        return format_html(f'''
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <div style="font-weight: bold;">{obj.item.name}</div>
                    <div style="font-size: 12px; color: #666;">{obj.item.description[:100]}{"..." if len(obj.item.description) > 100 else ""}</div>
                </div>
            </div>
        ''')

    item_details.short_description = "Item Details"


class CharacterNameTemplateInline(admin.TabularInline):
    model = CharacterNameTemplate
    extra = 1
    fields = ('name_type', 'names', 'gender_specific')
    classes = ('wide',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['names'].widget.attrs['style'] = 'width: 400px;'
        formset.form.base_fields['name_type'].widget.attrs['style'] = 'min-width: 150px;'
        return formset


class CampaignFilter(SimpleListFilter):
    title = _('Campaign')
    parameter_name = 'campaign'

    def lookups(self, request, model_admin):
        campaigns = set([t.campaign for t in model_admin.model.objects.filter(campaign__isnull=False)])
        return [(c.id, c.name) for c in campaigns]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(campaign__id=self.value())
        return queryset


@admin.register(CharacterTemplate)
class CharacterTemplateAdmin(CampaignAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'avatar_thumbnail', 'organization', 'rank', 'behavior', 'campaign', 'clone_template', 'create_npc')
    list_filter = ('behavior', CampaignFilter, 'organization')
    search_fields = ('name', 'description', 'tags')
    autocomplete_fields = ['rank', 'organization', 'path', 'stats_template', 'biography_template', 'campaign', 'dimension']

    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
        js = ('admin/js/admin/RelatedObjectLookups.js',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Override to add custom styling to form fields"""
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if formfield:
            formfield.widget.attrs.update({
                'class': 'vTextField',
                'style': 'width: 90%; max-width: 800px; box-sizing: border-box;'
            })
        return formfield

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Fix select elements width
        if form.base_fields.get('rank'):
            form.base_fields['rank'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('organization'):
            form.base_fields['organization'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('path'):
            form.base_fields['path'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('behavior'):
            form.base_fields['behavior'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('dimension'):
            form.base_fields['dimension'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('campaign'):
            form.base_fields['campaign'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('stats_template'):
            form.base_fields['stats_template'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        if form.base_fields.get('biography_template'):
            form.base_fields['biography_template'].widget.attrs['style'] = 'width: 300px; min-width: 300px;'
        return form

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'tags'),
            'description': 'Basic information about this character template.'
        }),
        ('Basic Properties', {
            'fields': ('rank', 'organization', 'path', 'behavior', 'dimension', 'campaign'),
            'description': 'Define the character\'s role, affiliation, and behavior patterns.'
        }),
        ('Template Components', {
            'fields': ('stats_template', 'biography_template', 'biography_preview'),
            'description': 'Link to pre-defined stat and biography templates for this character.'
        }),
        ('Multipliers', {
            'fields': ('health_multiplier', 'energy_multiplier', 'action_points_multiplier'),
            'classes': ('collapse',),
            'description': 'Adjust the base health, energy, and action points calculations.'
        }),
        ('Name Generation', {
            'fields': ('randomize_name', 'name_pattern'),
            'classes': ('collapse',),
            'description': 'Configure how names are generated for characters created from this template.'
        }),
    )

    readonly_fields = ('biography_preview',)

    inlines = [
        CharacterSkillTemplateInline,
        CharacterSchoolTemplateInline,
        CharacterModifierTemplateInline,
        CharacterEquipmentTemplateInline,
        CharacterNameTemplateInline
    ]

    def avatar_thumbnail(self, obj):
        """
        Displays a small thumbnail of the avatar from the biography template in the list view.
        """
        if obj.biography_template and obj.biography_template.avatar:
            return format_html('<img src="{}" style="height: 40px; width: 40px; border-radius: 50%; object-fit: cover; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); display: block; margin: 0 auto;" />', 
                              obj.biography_template.avatar.url)
        return format_html('<div style="text-align: center; color: #999; font-size: 11px;">No Image</div>')

    avatar_thumbnail.short_description = "Avatar"

    def biography_preview(self, obj):
        """
        Displays a preview of the biography template information.
        """
        if not obj.biography_template:
            return "No biography template selected"

        bio = obj.biography_template
        avatar_html = ""
        if bio.avatar:
            avatar_html = f'<img src="{bio.avatar.url}" style="max-height: 150px; max-width: 150px; border-radius: 10px; float: right; margin-left: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />'

        return format_html(f'''
            <div style="display: flex; margin-top: 10px;">
                <div style="flex: 1;">
                    <div style="margin-bottom: 10px;">
                        <strong>Age Range:</strong> {bio.age_min} - {bio.age_max} years
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>Gender:</strong> {bio.get_gender_display()} {" (Randomized)" if bio.randomize_gender else ""}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>Background:</strong> 
                        <div style="padding: 8px; background-color: #f9f9f9; border-radius: 4px; margin-top: 5px;">
                            {bio.background[:150]}{"..." if len(bio.background) > 150 else ""}
                        </div>
                    </div>
                    <div>
                        <strong>Appearance:</strong>
                        <div style="padding: 8px; background-color: #f9f9f9; border-radius: 4px; margin-top: 5px;">
                            {bio.appearance[:150]}{"..." if len(bio.appearance) > 150 else ""}
                        </div>
                    </div>
                </div>
                <div style="margin-left: 20px;">
                    {avatar_html}
                </div>
            </div>
        ''')

    biography_preview.short_description = "Biography Preview"

    def clone_template(self, obj):
        """Button to clone a template"""
        return format_html(
            '<a class="button" style="display: inline-block; padding: 6px 10px; margin: 0 2px; '
            'background: #4CAF50; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 12px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2); white-space: nowrap; overflow: visible;" href="{}">'
            '<span style="margin-right: 4px;">🔄</span>Clone</a>',
            reverse('admin:clone_npc_template', args=[obj.pk])
        )
    clone_template.short_description = 'Clone'

    def create_npc(self, obj):
        """Button to create an NPC from this template"""
        return format_html(
            '<a class="button" style="display: inline-block; padding: 6px 10px; margin: 0 2px; '
            'background: #2196F3; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 12px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2); white-space: nowrap; overflow: visible;" href="{}">'
            '<span style="margin-right: 4px;">👤</span>Create</a>',
            reverse('admin:create_npc_from_template', args=[obj.pk])
        )
    create_npc.short_description = 'Create NPC'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/clone/',
                self.admin_site.admin_view(self.clone_template_view),
                name='clone_npc_template',
            ),
            path(
                '<path:object_id>/create-npc/',
                self.admin_site.admin_view(self.create_npc_view),
                name='create_npc_from_template',
            ),
        ]
        return custom_urls + urls

    def clone_template_view(self, request, object_id):
        """View to clone a template"""
        template = self.get_object(request, object_id)
        if template is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, object_id)

        # Get the current campaign from the session
        campaign_id = request.session.get('campaign_id')
        campaign = None
        if campaign_id:
            from apps.game.models import Campaign
            campaign = Campaign.objects.get(id=campaign_id)
        else:
            campaign = template.campaign

        with transaction.atomic():
            # Clone the main template
            new_template = CharacterTemplate.objects.create(
                name=f"Copy of {template.name}",
                description=template.description,
                rank=template.rank,
                organization=template.organization,
                path=template.path,
                tags=template.tags.copy() if template.tags else [],
                behavior=template.behavior,
                dimension=template.dimension,
                stats_template=template.stats_template,
                biography_template=template.biography_template,
                health_multiplier=template.health_multiplier,
                energy_multiplier=template.energy_multiplier,
                action_points_multiplier=template.action_points_multiplier,
                randomize_name=template.randomize_name,
                name_pattern=template.name_pattern,
                campaign=campaign
            )

            # Clone related objects
            for skill_template in template.skill_templates.all():
                CharacterSkillTemplate.objects.create(
                    template=new_template,
                    skill=skill_template.skill,
                    is_base=skill_template.is_base
                )

            for school_template in template.school_templates.all():
                CharacterSchoolTemplate.objects.create(
                    template=new_template,
                    school=school_template.school,
                    is_base=school_template.is_base
                )

            for modifier_template in template.modifier_templates.all():
                CharacterModifierTemplate.objects.create(
                    template=new_template,
                    stat=modifier_template.stat,
                    value=modifier_template.value,
                    description=modifier_template.description
                )

            for equipment_template in template.equipment_templates.all():
                CharacterEquipmentTemplate.objects.create(
                    template=new_template,
                    item=equipment_template.item,
                    quantity=equipment_template.quantity,
                    is_equipped=equipment_template.is_equipped
                )

            for name_template in template.name_templates.all():
                CharacterNameTemplate.objects.create(
                    template=new_template,
                    name_type=name_template.name_type,
                    names=name_template.names.copy() if name_template.names else [],
                    gender_specific=name_template.gender_specific
                )

        messages.success(request, f'Template "{template.name}" was successfully cloned to "{new_template.name}"')
        return HttpResponseRedirect(
            reverse('admin:character_charactertemplate_change', args=(new_template.pk,))
        )

    def create_npc_view(self, request, object_id):
        """View to create an NPC from a template"""
        template = self.get_object(request, object_id)
        if template is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, object_id)

        # Get the current campaign from the session
        campaign_id = request.session.get('campaign_id')
        campaign = None
        if campaign_id:
            from apps.game.models import Campaign
            campaign = Campaign.objects.get(id=campaign_id)
        else:
            # Fallback to the template's campaign if no campaign in session
            campaign = template.campaign

        # Create the NPC using the factory
        factory = NPCFactory()
        config = NPCFactoryConfig(template=template, campaign=campaign)

        try:
            npc = factory.create_npc(config)
            messages.success(request, f'NPC "{npc.name}" was successfully created from template "{template.name}"')
            return HttpResponseRedirect(
                reverse('admin:character_character_change', args=(npc.pk,))
            )
        except Exception as e:
            messages.error(request, f'Error creating NPC: {str(e)}')
            return HttpResponseRedirect(
                reverse('admin:character_charactertemplate_change', args=(template.pk,))
            )
