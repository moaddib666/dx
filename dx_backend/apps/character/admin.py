from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from polymorphic.admin import PolymorphicChildModelAdmin

from .models import Organization, Rank, Character, CharacterBiography, Stat
from ..effects.models import ActiveEffect
from ..items.models import CharacterItem
from ..shields.models import ActiveShield
from ..skills.models import LearnedSchool, LearnedSkill


class BulkChangeAvatarForm(forms.Form):
    """
    Form to upload a new avatar for bulk action.
    """
    avatar = forms.ImageField(label="New Avatar")


class BulkChangeOrganizationForm(forms.Form):
    """
    Form to select an organization for bulk action.
    """
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label="Select Organization",
        required=True
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_needed', 'grade')
    search_fields = ('name',)
    list_filter = ('experience_needed',)


class CharacterBiographyInline(admin.StackedInline):
    """
    Inline admin for managing CharacterBiography directly within Character admin.
    """
    model = CharacterBiography
    extra = 0  # No extra blank forms
    fields = ('age', 'gender', 'background', 'appearance', 'avatar', 'avatar_preview')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        """
        Displays the avatar image as a preview in the admin interface.
        """
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.avatar.url)
        return "No Image"

    avatar_preview.short_description = "Avatar Preview"


class SubLocationFilter(admin.SimpleListFilter):
    """
    Custom filter for filtering by sublocation.
    """
    title = 'SubLocation'
    parameter_name = 'position__sublocation'

    def lookups(self, request, model_admin):
        sublocations = set(
            obj.position.sub_location for obj in Character.objects.select_related('position__sub_location') if
            obj.position
        )
        return [(s.id, s.name) for s in sublocations]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__sub_location_id=self.value())
        return queryset


class GridZFilter(admin.SimpleListFilter):
    """
    Custom filter for filtering by grid_z.
    """
    title = 'Grid Z'
    parameter_name = 'position__grid_z'

    def lookups(self, request, model_admin):
        grid_z_values = set(
            obj.position.grid_z for obj in Character.objects.select_related('position') if obj.position
        )
        return [(z, f'Grid Z: {z}') for z in grid_z_values]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__grid_z=self.value())
        return queryset


class StatInline(admin.TabularInline):
    """
    Inline for displaying and editing stats directly in the Character admin interface.
    """
    model = Stat
    extra = 1  # Number of extra blank rows
    fields = ('name', 'value',)
    readonly_fields = ('name',)
    can_delete = False


class OwnedItemsInline(admin.TabularInline):
    model = CharacterItem
    extra = 1
    fields = ('world_item', 'item_details', 'duplicate_item')
    readonly_fields = ('item_details', 'duplicate_item')
    can_delete = True

    def item_details(self, obj):
        if obj.world_item and obj.world_item.item and obj.world_item.item.icon:
            return mark_safe(
                f'''
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="{obj.world_item.item.icon.url}"
                         alt="Item Icon"
                         style="height: 50px; width: 50px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />
                    <div>
                        <strong style="color: #333; font-size: 14px;">{obj.world_item.item.name}</strong>
                        <div style="font-size: 12px; color: #555;">Charges: {obj.world_item.charges_left}</div>
                        <div style="font-size: 12px; color: #555;">{obj.world_item.item.description}</div>
                    </div>
                </div>
                '''
            )
        return "No Item Data Available"

    item_details.short_description = "Item Details"

    def duplicate_item(self, obj):
        if obj.pk:  # Ensure the object is saved
            duplicate_url = reverse('admin:duplicate_item', args=[obj.pk])
            return format_html(
                f'<a href="{duplicate_url}" class="button">Duplicate</a>'
            )
        return "Save to duplicate"

    duplicate_item.short_description = "Duplicate Item"


class ActiveShieldsInline(admin.TabularInline):
    model = ActiveShield
    extra = 1
    fields = ('shield', 'shield_details', 'health', 'cycles_left',)
    readonly_fields = ('shield_details',)
    can_delete = True

    def shield_details(self, obj):
        if obj.shield and obj.shield.icon:
            return mark_safe(
                f'''
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="{obj.shield.icon.url}"
                         alt="Shield Icon"
                         style="height: 50px; width: 50px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />
                    <div>
                        <strong style="color: #333; font-size: 14px;">{obj.shield.id} Lv. {obj.level} ({obj.efficiency})</strong>
                        <div style="font-size: 12px; color: #555;">Base Health: {obj.health}</div>
                    </div>
                </div>
                '''
            )
        return "No Shield Data Available"

    shield_details.short_description = "Shield Details"


class LearnedSchoolsInline(admin.TabularInline):
    """
    Inline for displaying and editing learned schools directly in the Character admin interface.
    """
    model = LearnedSchool
    extra = 1  # Number of extra blank rows
    fields = ('school_details',)
    readonly_fields = ('school_details',)
    can_delete = True  # Allow deletion of rows

    def school_details(self, obj):
        """
        Render the school details, including an icon and name, in the inline form.
        """
        if obj and obj.school and obj.school.icon:
            return mark_safe(
                f'''

                <div style="display: flex; align-items: center; gap: 10px;">
                <a href="/admin/school/school/{obj.school.id}/change/" style="color: #333; font-size: 14px;">
                    <img src="{obj.school.icon.url}"
                         alt="School Icon"
                         style="height: 50px; width: 50px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />
                     </a>
                    <div>

                            <strong style="color: #333; font-size: 14px;">{obj.school}</strong>

                        <div style="font-size: 12px; color: #555;">Base: {"Yes" if obj.is_base else "No"}</div>
                    </div>

                </div>
                '''
            )
        return "No School Data"

    school_details.short_description = "School Details"


class LearnedSkillsInline(admin.TabularInline):
    """
    Inline for displaying and editing learned skills directly in the Character admin interface.
    """
    model = LearnedSkill
    extra = 1  # Number of extra blank rows
    fields = ('skill_details',)
    readonly_fields = ('skill_details',)
    can_delete = True  # Allow deletion of rows

    def skill_details(self, obj):
        """
        Render the skill details, including an icon and name, in the inline form.
        """
        if obj and obj.skill and obj.skill.icon:
            return mark_safe(
                f'''
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="{obj.skill.icon.url}"
                         alt="Skill Icon"
                         style="height: 50px; width: 50px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />
                    <div>
                        <strong style="color: #333; font-size: 14px;">{obj.skill}</strong>
                        <div style="font-size: 12px; color: #555;">Grade: {obj.skill.grade}</div>
                    </div>
                </div>
                '''
            )
        return "No Skill Data"

    skill_details.short_description = "Skill Details"


class ActiveEffectsInline(admin.TabularInline):
    """
    Inline for displaying and editing Active Effects directly in the Character admin interface.
    """
    model = ActiveEffect
    extra = 1  # Number of extra blank rows
    fields = ('effect', 'effect_details', 'duration', 'active',)
    readonly_fields = ('effect_details',)
    can_delete = True  # Allow deletion of rows

    def effect_details(self, obj):
        """
        Render the effect details, including an icon and name, in the inline form.
        """
        if obj and obj.effect and obj.effect.icon:
            return mark_safe(
                f'''
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="{obj.effect.icon.url}"
                         alt="Effect Icon"
                         style="height: 50px; width: 50px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);" />
                    <div>
                        <strong style="color: #333; font-size: 14px;">{obj.effect.id}</strong>
                        <div style="font-size: 12px; color: #555;">Permanent: {"Yes" if obj.effect.permanent else "No"}</div>
                        <div style="font-size: 12px; color: #555;">Ends In: {obj.effect.ends_in or "N/A"}</div>
                    </div>
                </div>
                '''
            )
        return "No Effect Data"

    effect_details.short_description = "Effect Details"


@admin.register(Character)
class CharacterAdmin(PolymorphicChildModelAdmin):
    """
    Admin interface for Character with integrated CharacterBiography.
    """
    show_in_index = True
    base_model = Character
    list_display = (
        'name', 'pictogram', 'position', 'get_age', 'get_gender', 'rank',
        'current_health_points', 'current_energy_points', "current_active_points",
        'organization', 'is_active', 'npc',
    )
    search_fields = ('name', 'biography__background', 'biography__appearance', "id")
    list_filter = (
        'biography__gender', 'rank', 'organization', 'is_active', 'npc', SubLocationFilter, GridZFilter
    )
    inlines = [CharacterBiographyInline, StatInline, OwnedItemsInline, LearnedSchoolsInline, LearnedSkillsInline,
               ActiveEffectsInline, ActiveShieldsInline]
    actions = ['bulk_set_active', 'bulk_set_inactive', 'bulk_set_npc', 'reset_stats', 'duplicate_character']

    def pictogram(self, obj):
        """
        Displays the avatar image in the list view.
        """
        if obj.biography and obj.biography.avatar:
            return format_html('<img src="{}" style="height: 50px; width: 50px; border-radius: 50%;" />',
                               obj.biography.avatar.url)
        return "No Image"

    pictogram.short_description = "Avatar"

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
                stat.value = 0
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


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    """
    Admin interface for Stats management.
    """
    list_display = ('name', 'value', 'character')
    list_filter = ('name',)
    search_fields = ('character__name',)


@admin.register(CharacterBiography)
class CharacterBiographyAdmin(admin.ModelAdmin):
    """
    Admin interface for CharacterBiography.
    """
    list_display = ('character', 'age', 'gender', 'background', 'avatar_preview')
    search_fields = ('character__name', 'background', 'appearance')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.avatar.url)
        return "No Image"

    avatar_preview.short_description = "Avatar Preview"
