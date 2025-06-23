from django.contrib import admin
from django.utils.html import format_html
from polymorphic.admin import PolymorphicChildModelAdmin

from apps.game.services.npc.factory import NPCFactory
from apps.core.admin.mixins import CampaignAdminMixin
from .filters import SubLocationFilter, GridZFilter
from .inlines import (
    CharacterBiographyInline, StatInline, StatModifierInline, OwnedItemsInline,
    LearnedSchoolsInline, LearnedSkillsInline, ActiveEffectsInline, ActiveShieldsInline
)
from ..models import Character, CharacterBiography


@admin.register(Character)
class CharacterAdmin(CampaignAdminMixin, PolymorphicChildModelAdmin):
    """
    Admin interface for Character with integrated CharacterBiography.
    """
    show_in_index = True
    base_model = Character
    list_display = (
        'name', 'pictogram', 'position', 'get_age', 'get_gender', 'rank',
        'current_health_points', 'current_energy_points', "current_active_points",
        'organization', 'is_active', 'npc', 'campaign',
    )
    search_fields = ('name', 'biography__background', 'biography__appearance', "id")
    list_filter = (
        'biography__gender', 'rank', 'organization', 'is_active', 'npc', 'campaign', SubLocationFilter, GridZFilter
    )
    inlines = [CharacterBiographyInline, StatInline, StatModifierInline, OwnedItemsInline, LearnedSchoolsInline, LearnedSkillsInline,
               ActiveEffectsInline, ActiveShieldsInline]
    actions = ['bulk_set_active', 'bulk_set_inactive', 'bulk_set_npc', 'reset_stats', 'duplicate_character', 'create_template_from_npc']

    def pictogram(self, obj):
        """
        Displays the avatar image in the list view.
        """
        if obj.biography and obj.biography.avatar:
            return format_html(
                '<img src="{}" style="height: 50px; width: 50px; border-radius: 50%; object-fit: cover;" />',
                               obj.biography.avatar.url)
        else:
            # Default avatar with first letter of character name
            name_initial = obj.name[0].upper() if obj.name else "?"
            bg_color = self._get_color_from_name(obj.name)

            return format_html(
                '<div style="height: 50px; width: 50px; border-radius: 50%; background-color: {}; '
                'color: white; display: flex; align-items: center; justify-content: center; '
                'font-weight: bold; font-size: 20px;">{}</div>',
                bg_color, name_initial
            )

    pictogram.short_description = "Avatar"

    def _get_color_from_name(self, name):
        """Generate a consistent color based on the character name"""
        if not name:
            return "#6c757d"  # Default gray

        # Simple hash function to generate a color
        hash_value = sum(ord(c) for c in name)
        hue = hash_value % 360
        return f"hsl({hue}, 70%, 40%)"

    def get_age(self, obj):
        """
        Retrieve age from the associated CharacterBiography.
        """
        return obj.biography.age if obj.biography else "N/A"

    get_age.short_description = "Age"

    def get_gender(self, obj):
        """
        Retrieve gender from the associated CharacterBiography.
        """
        return obj.biography.gender if obj.biography else "N/A"

    get_gender.short_description = "Gender"

    @admin.action(description='Set selected characters as Active')
    def bulk_set_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} character(s) set as active.")

    @admin.action(description='Set selected characters as NPC')
    def bulk_set_npc(self, request, queryset):
        updated = queryset.update(npc=True)
        self.message_user(request, f"{updated} character(s) set as NPC.")

    @admin.action(description='Set selected characters as Inactive')
    def bulk_set_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} character(s) set as inactive.")

    @admin.action(description='Reset stats for selected characters')
    def reset_stats(self, request, queryset):
        for character in queryset:
            for stat in character.stats.all():
                stat.base_value = 0
                stat.additional_value = 0
                stat.save()
        self.message_user(request, f"Stats reset for {queryset.count()} character(s).")

    @admin.action(description='Duplicate selected character(s)')
    def duplicate_character(self, request, queryset):
        for character in queryset:
            new_character = Character.objects.get(pk=character.pk)
            new_character.pk = None  # Reset primary key to create a new instance
            new_character.name = f"Copy: {character.name}"  # Rename duplicated character
            new_character.save()

            if character.biography:
                CharacterBiography.objects.create(
                    character=new_character,
                    age=character.biography.age,
                    gender=character.biography.gender,
                    background=character.biography.background,
                    appearance=character.biography.appearance,
                    avatar=character.biography.avatar
                )
        self.message_user(request, f"{queryset.count()} character(s) duplicated successfully.")

    @admin.action(description='Create template from selected NPC(s)')
    def create_template_from_npc(self, request, queryset):
        factory = NPCFactory()
        templates_created = 0
        skipped = 0

        for character in queryset:
            if not character.npc:
                skipped += 1
                continue

            template_name = f"{character.name} Template"
            factory.create_template_from_npc(character, template_name)
            templates_created += 1

        if templates_created > 0:
            self.message_user(request, f"Created {templates_created} template(s) from selected NPC(s).")
        if skipped > 0:
            self.message_user(request, f"Skipped {skipped} character(s) that were not NPCs.")
