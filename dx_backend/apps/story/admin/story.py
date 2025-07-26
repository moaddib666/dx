from django.contrib import admin
from django.utils.html import format_html
from apps.story.models.story import Story, Chapter


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    fields = ('title', 'description', 'order', 'image')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'canonical', 'chapter_count', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('canonical', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    inlines = [ChapterInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'canonical')
        }),
        ('Media & Metadata', {
            'fields': ('image', 'image_preview', 'tags')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def chapter_count(self, obj):
        return obj.chapters.count()

    chapter_count.short_description = 'Chapters'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = 'Image Preview'


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'story', 'order', 'quest_count', 'image_preview', 'created_at')
    list_filter = ('story', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'story__title')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    ordering = ('story', 'order')

    fieldsets = (
        ('Basic Information', {
            'fields': ('story', 'title', 'description', 'order')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def quest_count(self, obj):
        return obj.quests.count()

    quest_count.short_description = 'Quests'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = 'Image Preview'
