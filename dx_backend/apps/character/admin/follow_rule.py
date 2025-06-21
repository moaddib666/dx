from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.character.models.npc import FollowRule


class FollowRuleAdmin(admin.ModelAdmin):
    """
    Admin interface for FollowRule model.
    """
    list_display = ('id', 'priority', 'type', 'leader_display', 'follower_display', 'cycles_left', 'permanent', 'status_display')
    list_filter = ('type', 'permanent')
    search_fields = ('leader__name', 'follower__name')
    ordering = ('priority',)
    list_editable = ('priority', 'cycles_left')
    list_per_page = 20
    actions = ['make_permanent', 'make_temporary', 'add_cycles', 'remove_cycles', 'change_to_teleport', 'change_to_walk']

    fieldsets = (
        ('Rule Settings', {
            'fields': ('priority', 'type', 'cycles_left', 'permanent'),
            'description': 'Configure the follow rule settings. Lower priority values mean higher priority.'
        }),
        ('Characters', {
            'fields': ('leader', 'follower'),
            'description': 'Select the leader and follower characters for this rule.'
        }),
    )

    def leader_display(self, obj):
        """
        Display leader with avatar and position.
        """
        avatar_html = self.get_avatar_html(obj.leader)
        position_html = self.get_position_html(obj.leader)

        return format_html(
            '<div class="character-display">{}<div class="character-name">{}</div><div class="character-position">{}</div></div>',
            avatar_html,
            obj.leader.name,
            position_html
        )
    leader_display.short_description = 'Leader'

    def follower_display(self, obj):
        """
        Display follower with avatar and position.
        """
        avatar_html = self.get_avatar_html(obj.follower)
        position_html = self.get_position_html(obj.follower)

        return format_html(
            '<div class="character-display">{}<div class="character-name">{}</div><div class="character-position">{}</div></div>',
            avatar_html,
            obj.follower.name,
            position_html
        )
    follower_display.short_description = 'Follower'

    def get_avatar_html(self, character):
        """
        Get HTML for character avatar.
        """
        try:
            if hasattr(character, 'biography') and character.biography and character.biography.avatar:
                return format_html(
                    '<img src="{}" class="character-avatar" width="50" height="50" />',
                    character.biography.avatar.url
                )
        except Exception:
            pass

        return format_html('<div class="no-avatar">No Avatar</div>')

    def get_position_html(self, character):
        """
        Get HTML for character position.
        """
        if character.position:
            return format_html(
                'X={}, Y={}, Z={}',
                character.position.grid_x,
                character.position.grid_y,
                character.position.grid_z
            )
        return 'No position'

    def status_display(self, obj):
        """
        Display the status of the follow rule.
        """
        if obj.permanent:
            return format_html('<span style="color: green; font-weight: bold;">Permanent</span>')
        elif obj.cycles_left > 0:
            return format_html('<span style="color: blue;">Active ({} cycles left)</span>', obj.cycles_left)
        else:
            return format_html('<span style="color: red;">Expired</span>')
    status_display.short_description = 'Status'

    def make_permanent(self, request, queryset):
        """
        Make selected follow rules permanent.
        """
        updated = queryset.update(permanent=True)
        self.message_user(request, f"{updated} follow rules were made permanent.")
    make_permanent.short_description = "Make selected rules permanent"

    def make_temporary(self, request, queryset):
        """
        Make selected follow rules temporary.
        """
        updated = queryset.update(permanent=False)
        self.message_user(request, f"{updated} follow rules were made temporary.")
    make_temporary.short_description = "Make selected rules temporary"

    def add_cycles(self, request, queryset):
        """
        Add 10 cycles to selected follow rules.
        """
        for rule in queryset:
            rule.cycles_left += 10
            rule.save()
        self.message_user(request, f"Added 10 cycles to {queryset.count()} follow rules.")
    add_cycles.short_description = "Add 10 cycles to selected rules"

    def remove_cycles(self, request, queryset):
        """
        Remove 10 cycles from selected follow rules.
        """
        for rule in queryset:
            rule.cycles_left = max(0, rule.cycles_left - 10)
            rule.save()
        self.message_user(request, f"Removed 10 cycles from {queryset.count()} follow rules.")
    remove_cycles.short_description = "Remove 10 cycles from selected rules"

    def change_to_teleport(self, request, queryset):
        """
        Change selected follow rules to teleport type.
        """
        from apps.core.models import MoveTypes
        updated = queryset.update(type=MoveTypes.TELEPORT)
        self.message_user(request, f"{updated} follow rules were changed to teleport type.")
    change_to_teleport.short_description = "Change selected rules to teleport type"

    def change_to_walk(self, request, queryset):
        """
        Change selected follow rules to walk type.
        """
        from apps.core.models import MoveTypes
        updated = queryset.update(type=MoveTypes.WALK)
        self.message_user(request, f"{updated} follow rules were changed to walk type.")
    change_to_walk.short_description = "Change selected rules to walk type"

    class Media:
        css = {
            'all': ('admin/css/follow_rule.css',)
        }


# Register the model with the admin site
admin.site.register(FollowRule, FollowRuleAdmin)
