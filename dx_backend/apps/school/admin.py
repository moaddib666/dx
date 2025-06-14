from django.contrib import admin
from .models import ThePath, School, Skill


@admin.register(ThePath)
class ThePathAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon_display')
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    def icon_display(self, obj):
        if obj.icon:
            return f"Icon Uploaded: {obj.icon.url.split('/')[-1]}"
        return "No Icon"
    icon_display.short_description = "Icon Status"


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('name', 'grade', 'type', 'multi_target', 'impact', 'cost', 'effect', 'icon')
    verbose_name = "Skill"
    verbose_name_plural = "Skills"


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon_display')
    search_fields = ('name',)
    filter_horizontal = ('path',)
    inlines = [SkillInline]
    readonly_fields = ('id', 'created_at', 'updated_at')

    def icon_display(self, obj):
        if obj.icon:
            return f"Icon Uploaded: {obj.icon.url.split('/')[-1]}"
        return "No Icon"
    icon_display.short_description = "Icon Status"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'type', 'multi_target', 'school_name', 'view_impact')
    search_fields = ('name', 'type', 'school__name')
    list_filter = ('type', 'multi_target', 'grade', 'school')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'grade', 'description', 'type', 'special', 'multi_target', 'school', 'icon')
        }),
        ('JSON Fields', {
            'fields': ('impact', 'cost', 'effect'),
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )

    def school_name(self, obj):
        return obj.school.name if obj.school else "No School"

    school_name.short_description = "School"

    def view_impact(self, obj):
        """
        Display a summary of the impact field for quick reference.
        """
        return f"{len(obj.impact)} impacts" if obj.impact else "No impacts"

    view_impact.short_description = "Impact Summary"
