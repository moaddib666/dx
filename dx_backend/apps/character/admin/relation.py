from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import OrganizationRelation, CharacterRelation


@admin.register(OrganizationRelation)
class OrganizationRelationAdmin(admin.ModelAdmin):
    list_display = ('organization_from', 'type', 'organization_to', 'immutable')
    list_filter = ('type', 'immutable')
    search_fields = ('organization_from__name', 'organization_to__name', 'type')
    autocomplete_fields = ('organization_from', 'organization_to')
    list_per_page = 25
    ordering = ('organization_from__name', 'organization_to__name')


@admin.register(CharacterRelation)
class CharacterRelationAdmin(admin.ModelAdmin):
    list_display = ('character_from_with_avatar', 'type', 'character_to_with_avatar', 'immutable')
    list_filter = ('type', 'immutable')
    search_fields = ('character_from__name', 'character_to__name', 'type',
                     'character_from__biography__background', 'character_to__biography__background')
    autocomplete_fields = ('character_from', 'character_to')
    list_per_page = 25
    ordering = ('character_from__name', 'character_to__name')

    def character_from_with_avatar(self, obj):
        """Display character_from with avatar"""
        return self._get_character_display(obj.character_from)

    character_from_with_avatar.short_description = "Character From"
    character_from_with_avatar.admin_order_field = 'character_from__name'

    def character_to_with_avatar(self, obj):
        """Display character_to with avatar"""
        return self._get_character_display(obj.character_to)

    character_to_with_avatar.short_description = "Character To"
    character_to_with_avatar.admin_order_field = 'character_to__name'

    def _get_character_display(self, character):
        """Helper method to display character with avatar"""
        if hasattr(character, 'biography') and character.biography and character.biography.avatar:
            avatar_html = f"""
                <img src="{character.biography.avatar.url}" 
                     style="height: 40px; width: 40px; border-radius: 50%; margin-right: 10px; 
                            object-fit: cover; vertical-align: middle;"
                     alt="{character.name}" />
            """
        else:
            # Default avatar with first letter of character name
            name_initial = character.name[0].upper() if character.name else "?"
            bg_color = self._get_color_from_name(character.name)

            avatar_html = f"""
                <div style="height: 40px; width: 40px; border-radius: 50%; margin-right: 10px;
                           background-color: {bg_color}; color: white; display: flex; 
                           align-items: center; justify-content: center; font-weight: bold;">
                    {name_initial}
                </div>
            """

        # Add behavior indicator if available
        behavior_badge = ""
        if hasattr(character, 'behavior'):
            colors = {
                'PASSIVE': '#28a745',  # Green
                'NEUTRAL': '#6c757d',  # Gray
                'AGGRESSIVE': '#dc3545',  # Red
                'FRIENDLY': '#17a2b8',  # Blue
                'HOSTILE': '#fd7e14',  # Orange
            }
            color = colors.get(character.behavior, '#6c757d')
            behavior_badge = f"""
                <span style="background-color: {color}; color: white; padding: 2px 6px; 
                             border-radius: 10px; font-size: 0.7em; margin-left: 5px;">
                    {character.behavior}
                </span>
            """

        return mark_safe(f"""
            <div style="display: flex; align-items: center;">
                {avatar_html}
                <div>
                    <div>
                        <strong>{character.name}</strong>
                        {behavior_badge}
                    </div>
                    <div style="font-size: 0.8em; color: #666;">
                        {character.organization.name if character.organization else 'No Organization'}
                    </div>
                </div>
            </div>
        """)

    def _get_color_from_name(self, name):
        """Generate a consistent color based on the character name"""
        if not name:
            return "#6c757d"  # Default gray

        # Simple hash function to generate a color
        hash_value = sum(ord(c) for c in name)
        hue = hash_value % 360
        return f"hsl({hue}, 70%, 40%)"
