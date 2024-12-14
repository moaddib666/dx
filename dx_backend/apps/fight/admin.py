from django.contrib import admin

from .models import DuelInvitation, Fight, FightTurn, FightTurnAction


class DuelInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiator', 'target', 'is_accepted', 'is_rejected', 'fight')
    list_filter = ('is_accepted', 'is_rejected')
    search_fields = ('initiator__username', 'target__username')
    readonly_fields = ('created_at', 'updated_at')


class FightAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiator', 'target', 'is_open', 'is_ended', 'current_turn')
    list_filter = ('is_open', 'is_ended')
    search_fields = ('initiator__username', 'target__username')
    filter_horizontal = ('side_a_participants', 'side_b_participants')
    readonly_fields = ('created_at', 'updated_at')


class FightTurnAdmin(admin.ModelAdmin):
    list_display = ('id', 'fight', 'is_finished')
    list_filter = ('is_finished',)
    search_fields = ('fight__initiator__username', 'fight__target__username')
    readonly_fields = ('created_at', 'updated_at')


class FightTurnActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'created_at')  # Adjust list_display to actual fields in the model
    list_filter = ('created_at',)  # Adjust list_filter to actual fields in the model
    search_fields = ('turn__fight__initiator__username', 'turn__fight__target__username')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(DuelInvitation, DuelInvitationAdmin)
admin.site.register(Fight, FightAdmin)
admin.site.register(FightTurn, FightTurnAdmin)
admin.site.register(FightTurnAction, FightTurnActionAdmin)
