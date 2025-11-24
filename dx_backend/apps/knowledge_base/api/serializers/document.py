from rest_framework import serializers

from apps.knowledge_base.models import Document, DocumentCategory


class DocumentCategorySerializer(serializers.ModelSerializer):
    """Serializer for DocumentCategory objects"""
    description = serializers.CharField(max_length=5000, required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'image']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document objects"""
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DocumentCategory.objects.all(),
        required=False
    )
    content = serializers.CharField(max_length=50000)
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'categories', 'image']
