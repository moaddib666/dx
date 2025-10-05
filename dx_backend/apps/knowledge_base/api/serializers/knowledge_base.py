from rest_framework import serializers
from apps.knowledge_base.models import KnowledgeBaseItem, KnowledgeBaseItemTag, DXDate


class KnowledgeBaseItemTagSerializer(serializers.ModelSerializer):
    """
    Serializer for KnowledgeBaseItemTag model.
    """
    item_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = KnowledgeBaseItemTag
        fields = ['label', 'item_count']

    def get_item_count(self, obj):
        return obj.knowledge_base_items.count()


class DXDateSerializer(serializers.ModelSerializer):
    """
    Serializer for DXDate model.
    """
    era_decade_sol = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DXDate
        fields = ['dxCycle', 'BAG', 'era_decade_sol']

    def get_era_decade_sol(self, obj):
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
        
        return {
            'era': era,
            'decade': remaining_decade,
            'sol': remaining_sol,
            'cycle': remaining_cycle,
            'formatted': f"Era {era}, Decade {remaining_decade}, Sol {remaining_sol}, Cycle {remaining_cycle}"
        }


class KnowledgeBaseItemSerializer(serializers.ModelSerializer):
    """
    Serializer for KnowledgeBaseItem model.
    """
    # Read-only nested serializers for display
    breadcrumbs = serializers.SerializerMethodField(read_only=True)
    tags = KnowledgeBaseItemTagSerializer(many=True, read_only=True)
    
    # Write-only fields for creating/updating relationships
    breadcrumb_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
        help_text="List of KnowledgeBaseItem IDs for breadcrumbs"
    )
    tag_labels = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of tag labels"
    )
    
    # Additional computed fields
    tag_count = serializers.SerializerMethodField(read_only=True)
    breadcrumb_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = KnowledgeBaseItem
        fields = [
            'id', 'category', 'dxCycle', 'description', 'metadata',
            'breadcrumbs', 'tags', 'breadcrumb_ids', 'tag_labels',
            'tag_count', 'breadcrumb_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_breadcrumbs(self, obj):
        """Return simplified breadcrumb data to avoid deep nesting"""
        return [
            {
                'id': breadcrumb.id,
                'category': breadcrumb.category,
                'description': breadcrumb.description[:100] + "..." if len(breadcrumb.description) > 100 else breadcrumb.description,
                'dxCycle': breadcrumb.dxCycle
            }
            for breadcrumb in obj.breadcrumbs.all()
        ]

    def get_tag_count(self, obj):
        return obj.tags.count()

    def get_breadcrumb_count(self, obj):
        return obj.breadcrumbs.count()

    def create(self, validated_data):
        breadcrumb_ids = validated_data.pop('breadcrumb_ids', [])
        tag_labels = validated_data.pop('tag_labels', [])

        knowledge_base_item = KnowledgeBaseItem.objects.create(**validated_data)

        # Handle breadcrumbs
        if breadcrumb_ids:
            knowledge_base_item.breadcrumbs.set(breadcrumb_ids)

        # Handle tags - create if they don't exist
        if tag_labels:
            tags = []
            for label in tag_labels:
                tag, created = KnowledgeBaseItemTag.objects.get_or_create(label=label)
                tags.append(tag)
            knowledge_base_item.tags.set(tags)

        return knowledge_base_item

    def update(self, instance, validated_data):
        breadcrumb_ids = validated_data.pop('breadcrumb_ids', None)
        tag_labels = validated_data.pop('tag_labels', None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle breadcrumbs
        if breadcrumb_ids is not None:
            instance.breadcrumbs.set(breadcrumb_ids)

        # Handle tags
        if tag_labels is not None:
            tags = []
            for label in tag_labels:
                tag, created = KnowledgeBaseItemTag.objects.get_or_create(label=label)
                tags.append(tag)
            instance.tags.set(tags)

        return instance