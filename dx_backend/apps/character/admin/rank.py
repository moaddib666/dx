from django.contrib import admin

from ..models import Rank


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Rank model.
    """
    list_display = (
        "name",
        "grade",
        "grade_rank",
        "experience_needed",
        "additional_stat_points",
        "next_rank_display"
    )
    list_filter = ("grade", "grade_rank")
    search_fields = ("name", "description")
    ordering = ("-grade", "grade_rank")
    readonly_fields = ("experience_needed",)
    fieldsets = (
        (None, {
            "fields": ("name", "description")
        }),
        ("Rank Details", {
            "fields": ("grade", "grade_rank", "additional_stat_points", "experience_needed", "next_rank")
        }),
    )

    def next_rank_display(self, obj):
        """
        Display the name of the next rank, if it exists.
        """
        return obj.next_rank.name if obj.next_rank else "None"

    next_rank_display.short_description = "Next Rank"