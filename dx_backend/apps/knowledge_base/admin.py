from django.contrib import admin
from django.utils.html import format_html
from .models import KnowledgeBaseItem, KnowledgeBaseItemTag, DXDate


@admin.register(KnowledgeBaseItemTag)
class KnowledgeBaseItemTagAdmin(admin.ModelAdmin):
    list_display = ('label', 'item_count')
    search_fields = ('label',)
    ordering = ('label',)

    def item_count(self, obj):
        return obj.knowledge_base_items.count()
    
    item_count.short_description = 'Items'


@admin.register(DXDate)
class DXDateAdmin(admin.ModelAdmin):
    list_display = ('dxCycle', 'BAG', 'era_decade_sol_display')
    list_filter = ('BAG',)
    search_fields = ('dxCycle',)
    ordering = ('dxCycle',)
    
    fieldsets = (
        ('Date Information', {
            'fields': ('dxCycle', 'BAG')
        }),
        ('Conversion Info', {
            'fields': ('era_decade_sol_display',),
            'classes': ('collapse',),
            'description': 'Era-Decade-Sol conversion: Sol = 100 cycles, Decade = 10 Sol, Era = 1000 Decade'
        }),
    )
    
    readonly_fields = ('era_decade_sol_display',)
    
    def era_decade_sol_display(self, obj):
        """Convert dxCycle to Era-Decade-Sol format"""
        if obj.dxCycle is None:
            return "N/A"
        
        # Sol = 100 cycles, Decade = 10 Sol, Era = 1000 Decade
        sol = obj.dxCycle // 100
        decade = sol // 10
        era = decade // 1000
        
        remaining_decade = decade % 1000
        remaining_sol = sol % 10
        remaining_cycle = obj.dxCycle % 100
        
        return f"Era {era}, Decade {remaining_decade}, Sol {remaining_sol}, Cycle {remaining_cycle}"
    
    era_decade_sol_display.short_description = 'Era-Decade-Sol'


class KnowledgeBaseItemTagInline(admin.TabularInline):
    model = KnowledgeBaseItem.tags.through
    extra = 0
    verbose_name = "Tag"
    verbose_name_plural = "Tags"


@admin.register(KnowledgeBaseItem)
class KnowledgeBaseItemAdmin(admin.ModelAdmin):
    list_display = ('description_preview', 'category', 'dxCycle', 'tag_count', 'breadcrumb_count', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('description', 'metadata')
    readonly_fields = ('created_at', 'updated_at', 'id', 'image_preview')
    filter_horizontal = ('tags', 'breadcrumbs')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'category', 'dxCycle', 'description')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Relationships', {
            'fields': ('breadcrumbs', 'tags')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def description_preview(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    
    description_preview.short_description = 'Description'
    
    def tag_count(self, obj):
        return obj.tags.count()
    
    tag_count.short_description = 'Tags'
    
    def breadcrumb_count(self, obj):
        return obj.breadcrumbs.count()
    
    breadcrumb_count.short_description = 'Breadcrumbs'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    
    image_preview.short_description = 'Image Preview'
