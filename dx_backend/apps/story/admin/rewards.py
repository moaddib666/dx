from django.contrib import admin
from apps.story.models.quest import Condition, Reward, TokenReward, ItemReward, EffectReward


class TokenRewardInline(admin.TabularInline):
    model = TokenReward
    extra = 0
    fields = ('token', 'amount')
    readonly_fields = ('created_at', 'updated_at')


class ItemRewardInline(admin.TabularInline):
    model = ItemReward
    extra = 0
    fields = ('item', 'amount')
    readonly_fields = ('created_at', 'updated_at')


class EffectRewardInline(admin.TabularInline):
    model = EffectReward
    extra = 0
    fields = ('effect', 'duration')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'trigger_count', 'starter_quest_count', 'objective_quest_count', 'created_at')
    list_filter = ('type', 'created_at', 'updated_at')
    search_fields = ('type',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('triggers',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('type', 'triggers')
        }),
        ('Usage Statistics', {
            'fields': ('starter_quest_count', 'objective_quest_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def trigger_count(self, obj):
        return obj.triggers.count()

    trigger_count.short_description = 'Triggers'

    def starter_quest_count(self, obj):
        return obj.starter_quests.count()

    starter_quest_count.short_description = 'Used as Starter'

    def objective_quest_count(self, obj):
        return obj.objective_quests.count()

    objective_quest_count.short_description = 'Used as Objective'


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'description_preview', 'experience', 'token_count', 'item_count', 'effect_count',
                    'success_quest_count', 'failure_quest_count', 'created_at')
    list_filter = ('experience', 'created_at', 'updated_at')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TokenRewardInline, ItemRewardInline, EffectRewardInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('description', 'experience')
        }),
        ('Usage Statistics', {
            'fields': ('success_quest_count', 'failure_quest_count'),
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

    def token_count(self, obj):
        return obj.tokens.count()

    token_count.short_description = 'Token Rewards'

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = 'Item Rewards'

    def effect_count(self, obj):
        return obj.effects.count()

    effect_count.short_description = 'Effect Rewards'

    def success_quest_count(self, obj):
        return obj.success_quests.count()

    success_quest_count.short_description = 'Success Quests'

    def failure_quest_count(self, obj):
        return obj.failure_quests.count()

    failure_quest_count.short_description = 'Failure Quests'


@admin.register(TokenReward)
class TokenRewardAdmin(admin.ModelAdmin):
    list_display = ('token', 'amount', 'reward_preview', 'created_at')
    list_filter = ('token', 'amount', 'created_at', 'updated_at')
    search_fields = ('token__name', 'reward__description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('token', 'amount', 'reward')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def reward_preview(self, obj):
        if obj.reward:
            return obj.reward.description[:30] + "..." if len(obj.reward.description) > 30 else obj.reward.description
        return "No reward"

    reward_preview.short_description = 'Reward'


@admin.register(ItemReward)
class ItemRewardAdmin(admin.ModelAdmin):
    list_display = ('item', 'amount', 'reward_preview', 'created_at')
    list_filter = ('item', 'amount', 'created_at', 'updated_at')
    search_fields = ('item__name', 'reward__description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('item', 'amount', 'reward')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def reward_preview(self, obj):
        if obj.reward:
            return obj.reward.description[:30] + "..." if len(obj.reward.description) > 30 else obj.reward.description
        return "No reward"

    reward_preview.short_description = 'Reward'


@admin.register(EffectReward)
class EffectRewardAdmin(admin.ModelAdmin):
    list_display = ('effect', 'duration', 'reward_preview', 'created_at')
    list_filter = ('effect', 'duration', 'created_at', 'updated_at')
    search_fields = ('effect__name', 'reward__description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('effect', 'duration', 'reward')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def reward_preview(self, obj):
        if obj.reward:
            return obj.reward.description[:30] + "..." if len(obj.reward.description) > 30 else obj.reward.description
        return "No reward"

    reward_preview.short_description = 'Reward'
