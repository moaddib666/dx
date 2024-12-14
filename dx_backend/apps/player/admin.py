from django.contrib import admin

from .models import Organization, Rank, Player, Stat


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_needed', 'grade')
    search_fields = ('name',)
    list_filter = ('experience_needed',)


@admin.register(Player)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'rank', 'current_health_points', 'current_energy_points')
    search_fields = ('name', 'bio')
    list_filter = ('gender', 'rank', 'organization')


@admin.register(Stat)
class CharacterStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'name', 'value')
    search_fields = ('name', 'player__name', 'player__id')
