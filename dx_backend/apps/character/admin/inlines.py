from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms

from ..models import Stat, StatModifier, CharacterBiography
from ...effects.models import ActiveEffect
from ...items.models import CharacterItem
from ...shields.models import ActiveShield
from ...skills.models import LearnedSchool, LearnedSkill
from ...school.models import Skill, School


class LearnedSkillForm(forms.ModelForm):
    """
    Custom form for LearnedSkill with improved skill selection and filtering.
    """
    school_filter = forms.ModelChoiceField(
        queryset=School.objects.all(),
        required=False,
        empty_label="All Schools",
        help_text="Filter skills by school"
    )
    
    class Meta:
        model = LearnedSkill
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Improve skill field widget with better help text
        self.fields['skill'].help_text = "Search by skill name or use the school filter above"
        
        # Add CSS classes for better styling
        self.fields['skill'].widget.attrs.update({
            'class': 'skill-autocomplete',
            'data-placeholder': 'Search for skills...'
        })
        
        # If we have a school filter value, filter the skills
        if 'school_filter' in self.data and self.data['school_filter']:
            try:
                school_id = int(self.data['school_filter'])
                self.fields['skill'].queryset = Skill.objects.filter(school_id=school_id)
            except (ValueError, TypeError):
                pass
    
    class Media:
        js = ('admin/js/learned_skills_filter.js',)
        css = {
            'all': ('admin/css/learned_skills.css',)
        }


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
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 8px; object-fit: cover;" />',
                obj.avatar.url)
        else:
            # Default avatar with first letter of character name
            name_initial = obj.character.name[0].upper() if obj.character and obj.character.name else "?"
            bg_color = self._get_color_from_name(obj.character.name if obj.character else "")

            return format_html(
                '<div style="height: 100px; width: 100px; border-radius: 8px; background-color: {}; '
                'color: white; display: flex; align-items: center; justify-content: center; '
                'font-weight: bold; font-size: 40px;">{}</div>',
                bg_color, name_initial
            )

    avatar_preview.short_description = "Avatar Preview"

    def _get_color_from_name(self, name):
        """Generate a consistent color based on the character name"""
        if not name:
            return "#6c757d"  # Default gray

        # Simple hash function to generate a color
        hash_value = sum(ord(c) for c in name)
        hue = hash_value % 360
        return f"hsl({hue}, 70%, 40%)"


class StatInline(admin.TabularInline):
    """
    Inline for displaying and editing stats directly in the Character admin interface.
    """
    model = Stat
    extra = 1  # Number of extra blank rows
    fields = ('name', 'base_value', "additional_value")
    readonly_fields = ('name', "value")
    can_delete = False


class StatModifierInline(admin.TabularInline):
    """
    Inline for displaying and editing stat modifiers directly in the Character admin interface.
    """
    model = StatModifier
    extra = 1  # Number of extra blank rows
    fields = ('name', 'value', 'applied_by_effect')
    readonly_fields = ('applied_by_effect', )
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
    fields = ('school', 'is_base', 'school_details')
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
    form = LearnedSkillForm
    extra = 1  # Number of extra blank rows
    fields = ('school_filter', 'skill', 'is_base', 'skill_details')
    readonly_fields = ('skill_details',)
    can_delete = True  # Allow deletion of rows
    autocomplete_fields = ('skill',)

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
    fields = ('effect', 'effect_details', 'duration', 'ends_in', 'cycle_left', 'active',)
    readonly_fields = ('effect_details', 'cycle_left')
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
