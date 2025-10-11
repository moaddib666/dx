from rest_framework import serializers

from apps.knowledge_base.models import Document, DocumentCategory


class DocumentCategorySerializer(serializers.ModelSerializer):
    """Serializer for DocumentCategory objects"""
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
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'categories', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
