from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.dice.models import Challenge, ChallengeModifier
from apps.action.models import DiceRollResult


class ChallengeModifierInline(admin.TabularInline):
    model = ChallengeModifier
    extra = 1
    fields = ("name", "icon_preview", "icon", "value", "created_at", "updated_at")
    readonly_fields = ("icon_preview", "created_at", "updated_at")

    def icon_preview(self, obj: ChallengeModifier):
        if obj and obj.icon:
            return format_html('<img src="{}" style="height:32px;width:32px;object-fit:cover;border-radius:4px;"/>', obj.icon.url)
        return mark_safe('<span style="color:#888;">No icon</span>')

    icon_preview.short_description = "Icon"


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    inlines = [ChallengeModifierInline]
    # Use raw_id_fields for better Django Jet compatibility
    raw_id_fields = ("target", "outcome")

    list_display = (
        "id",
        "target",
        "stat",
        "difficulty",
        "dice_sides",
        "advantage",
        "disadvantage",
        "roll_d20",
        "mod_sum",
        "effective_difficulty",
        "final_outcome",
        "created_at",
    )
    list_select_related = ("target", "outcome")
    list_filter = ("stat", "advantage", "disadvantage", "created_at", "updated_at")
    search_fields = ("id", "description", "target__name")
    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "roll_d20",
        "mod_sum",
        "effective_difficulty",
        "final_outcome",
        "outcome_preview",
    )

    fieldsets = (
        ("Challenge", {
            "fields": (
                ("target", "stat"),
                ("difficulty", "dice_sides"),
                ("advantage", "disadvantage"),
                "description",
            )
        }),
        ("Outcome", {
            "fields": (
                "outcome",
                "outcome_preview",
                ("mod_sum", "effective_difficulty"),
                ("roll_d20", "final_outcome"),
            )
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Prefetch modifiers to compute sums efficiently
        return qs.prefetch_related("modifiers")

    # Helper computations and rich columns
    def mod_sum(self, obj: Challenge) -> int:
        return sum(m.value for m in obj.modifiers.all())

    mod_sum.short_description = "Modifiers Σ"

    def effective_difficulty(self, obj: Challenge) -> int:
        return obj.difficulty - self.mod_sum(obj)

    effective_difficulty.short_description = "Effective DC"

    def roll_d20(self, obj: Challenge):
        # Show the rolled side if available
        if obj.outcome_id and obj.outcome:
            return obj.outcome.dice_side
        return "—"

    roll_d20.short_description = "Rolled"

    def final_outcome(self, obj: Challenge):
        """
        Display a convenient final value as: roll + Σmod vs DC (pass/fail)
        And include outcome enum if exists.
        """
        roll = obj.outcome.dice_side if obj.outcome_id and obj.outcome else None
        mod = self.mod_sum(obj)
        dc = obj.difficulty
        if roll is None:
            return mark_safe('<span style="color:#888;">No roll</span>')
        total = roll + mod
        passed = total >= dc
        color = "#15803d" if passed else "#b91c1c"
        outcome_label = obj.outcome.outcome if obj.outcome_id and obj.outcome else "—"
        return mark_safe(
            f'<span style="font-weight:600;color:{color};">{total}</span> '
            f'<span style="color:#666;">(roll {roll} + mod {mod} vs DC {dc})</span> '
            f'<span style="margin-left:6px;color:#334155;">[{outcome_label}]</span>'
        )

    final_outcome.short_description = "Final"

    def outcome_preview(self, obj: Challenge):
        if obj.outcome_id and obj.outcome:
            return mark_safe(
                f"<div>Roll: <b>{obj.outcome.dice_side}</b></div>"
                f"<div>Outcome: <b>{obj.outcome.outcome}</b></div>"
                f"<div>Multiplier: <b>{obj.outcome.multiplier if obj.outcome.multiplier is not None else '—'}</b></div>"
            )
        return mark_safe('<span style="color:#888;">No outcome yet</span>')

    outcome_preview.short_description = "Outcome details"


@admin.register(ChallengeModifier)
class ChallengeModifierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value", "challenge", "created_at")
    list_select_related = ("challenge",)
    search_fields = ("name", "challenge__id", "challenge__target__name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("challenge", "name", "icon", "value")
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )
