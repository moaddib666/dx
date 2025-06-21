from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.db import transaction

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
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [CharacterStatTemplateInline]


@admin.register(CharacterBiographyTemplate)
class CharacterBiographyTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'randomize_gender', 'age_min', 'age_max')
    search_fields = ('name', 'description', 'background', 'appearance')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Age Settings', {
            'fields': ('age_min', 'age_max')
        }),
        ('Gender Settings', {
            'fields': ('gender', 'randomize_gender')
        }),
        ('Appearance & Background', {
            'fields': ('background', 'appearance', 'avatar')
        }),
        ('Randomization', {
            'fields': ('background_variations', 'appearance_variations'),
            'classes': ('collapse',),
        }),
    )


class CharacterSkillTemplateInline(admin.TabularInline):
    model = CharacterSkillTemplate
    extra = 1
    fields = ('skill', 'is_base')
    autocomplete_fields = ['skill']


class CharacterSchoolTemplateInline(admin.TabularInline):
    model = CharacterSchoolTemplate
    extra = 1
    fields = ('school', 'is_base')
    autocomplete_fields = ['school']


class CharacterModifierTemplateInline(admin.TabularInline):
    model = CharacterModifierTemplate
    extra = 1
    fields = ('stat', 'value', 'description')


class CharacterEquipmentTemplateInline(admin.TabularInline):
    model = CharacterEquipmentTemplate
    extra = 1
    fields = ('item', 'quantity', 'is_equipped')
    autocomplete_fields = ['item']


class CharacterNameTemplateInline(admin.TabularInline):
    model = CharacterNameTemplate
    extra = 1
    fields = ('name_type', 'names', 'gender_specific')


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
class CharacterTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'rank', 'behavior', 'campaign', 'clone_template', 'create_npc')
    list_filter = ('behavior', CampaignFilter, 'organization')
    search_fields = ('name', 'description', 'tags')
    autocomplete_fields = ['rank', 'organization', 'path', 'stats_template', 'biography_template', 'campaign', 'dimension']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'tags')
        }),
        ('Basic Properties', {
            'fields': ('rank', 'organization', 'path', 'behavior', 'dimension', 'campaign')
        }),
        ('Template Components', {
            'fields': ('stats_template', 'biography_template')
        }),
        ('Multipliers', {
            'fields': ('health_multiplier', 'energy_multiplier', 'action_points_multiplier'),
            'classes': ('collapse',),
        }),
        ('Name Generation', {
            'fields': ('randomize_name', 'name_pattern'),
            'classes': ('collapse',),
        }),
    )

    inlines = [
        CharacterSkillTemplateInline,
        CharacterSchoolTemplateInline,
        CharacterModifierTemplateInline,
        CharacterEquipmentTemplateInline,
        CharacterNameTemplateInline
    ]

    def clone_template(self, obj):
        """Button to clone a template"""
        return format_html(
            '<a class="button" href="{}">Clone</a>',
            reverse('admin:clone_npc_template', args=[obj.pk])
        )
    clone_template.short_description = 'Clone'

    def create_npc(self, obj):
        """Button to create an NPC from this template"""
        return format_html(
            '<a class="button" href="{}">Create NPC</a>',
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
                campaign=template.campaign
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

        # Create the NPC using the factory
        factory = NPCFactory()
        config = NPCFactoryConfig(template=template)

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
