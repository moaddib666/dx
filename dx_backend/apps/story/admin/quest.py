from django.contrib import admin
from django.utils.html import format_html
from apps.story.models.quest import Quest, Note


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = ('content', 'order', 'image')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'story_title', 'order', 'cycle_limit', 'note_count', 'image_preview',
                    'created_at')
    list_filter = ('chapter__story', 'chapter', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'chapter__title', 'chapter__story__title')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    inlines = [NoteInline]
    ordering = ('chapter__story', 'chapter', 'order')

    fieldsets = (
        ('Basic Information', {
            'fields': ('chapter', 'title', 'description', 'order')
        }),
        ('Quest Configuration', {
            'fields': ('cycle_limit',)
        }),
        ('Conditions', {
            'fields': ('starters', 'objectives'),
            'classes': ('collapse',)
        }),
        ('Rewards', {
            'fields': ('on_success', 'on_failure'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    filter_horizontal = ('starters', 'objectives')

    def story_title(self, obj):
        return obj.chapter.story.title

    story_title.short_description = 'Story'
    story_title.admin_order_field = 'chapter__story__title'

    def note_count(self, obj):
        return obj.notes.count()

    note_count.short_description = 'Notes'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = 'Image Preview'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('quest_title', 'chapter_title', 'story_title', 'order', 'content_preview', 'image_preview',
                    'created_at')
    list_filter = ('quest__chapter__story', 'quest__chapter', 'quest', 'created_at', 'updated_at')
    search_fields = ('content', 'quest__title', 'quest__chapter__title', 'quest__chapter__story__title')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    ordering = ('quest__chapter__story', 'quest__chapter', 'quest', 'order')

    fieldsets = (
        ('Basic Information', {
            'fields': ('quest', 'order', 'content')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def quest_title(self, obj):
        return obj.quest.title

    quest_title.short_description = 'Quest'
    quest_title.admin_order_field = 'quest__title'

    def chapter_title(self, obj):
        return obj.quest.chapter.title

    chapter_title.short_description = 'Chapter'
    chapter_title.admin_order_field = 'quest__chapter__title'

    def story_title(self, obj):
        return obj.quest.chapter.story.title

    story_title.short_description = 'Story'
    story_title.admin_order_field = 'quest__chapter__story__title'

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = 'Content Preview'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = 'Image Preview'
