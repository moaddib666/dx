from django.contrib import admin
from .models import ThePath, School, Skill

@admin.register(ThePath)
class ThePathAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('path',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'multi_target')
    search_fields = ('name', 'grade')
    list_filter = ('grade', 'multi_target')
    fieldsets = (
        (None, {
            'fields': ('name', 'grade', 'description', 'multi_target')
        }),
        ('JSON Fields', {
            'fields': ('impact', 'cost', 'effect'),
        }),
    )

    def clean(self):
        # Call the clean method of the Skill model to validate JSON fields
        super().clean()
        for skill in Skill.objects.all():
            skill.clean()
