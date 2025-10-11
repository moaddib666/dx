from rest_framework import serializers

from apps.knowledge_base.api.serializers import DocumentSerializer
from apps.knowledge_base.models import TimeLineEvent, DateTimeInfo, Document, DocumentCategory


class DateTimeInfoSerializer(serializers.ModelSerializer):
    """Serializer for DateTimeInfo objects"""

    class Meta:
        model = DateTimeInfo
        fields = ['id', 'active_glow', 'sol', 'solar_year']
        read_only_fields = ['id']


class TimeLineEventSerializer(serializers.ModelSerializer):
    """Serializer for TimeLineEvent objects with nested representations"""
    document = DocumentSerializer(read_only=True)
    date_time = DateTimeInfoSerializer(read_only=True)

    class Meta:
        model = TimeLineEvent
        fields = ['id', 'document', 'date_time']
        read_only_fields = ['id']


class TimeLineEventImportSerializer(serializers.Serializer):
    """
    Serializer for importing TimeLineEvent with nested Document and DateTimeInfo.
    This serializer handles get_or_create logic for Document and DateTimeInfo.
    """
    document = DocumentSerializer()
    date_time = DateTimeInfoSerializer()

    def validate_document(self, value):
        """Validate document data"""
        if 'title' not in value:
            raise serializers.ValidationError("Document must have a 'title' field")
        if 'content' not in value:
            raise serializers.ValidationError("Document must have a 'content' field")
        return value

    def validate_date_time(self, value):
        """Validate date_time data"""
        if 'active_glow' not in value:
            raise serializers.ValidationError("DateTimeInfo must have an 'active_glow' field")
        if 'sol' not in value:
            raise serializers.ValidationError("DateTimeInfo must have a 'sol' field")
        if 'solar_year' not in value:
            raise serializers.ValidationError("DateTimeInfo must have a 'solar_year' field")
        return value

    def create(self, validated_data):
        """
        Create or get Document and DateTimeInfo, then create TimeLineEvent.
        """
        document_data = validated_data['document']
        date_time_data = validated_data['date_time']

        # Extract categories from document_data (if present)
        categories_data = document_data.pop('categories', [])

        # Get or create Document (match by title and content)
        document, _ = Document.objects.get_or_create(
            title=document_data['title'],
            content=document_data['content'],
            defaults={'image': document_data.get('image')}
        )

        # Handle categories if provided
        if categories_data:
            # Clear existing categories and add new ones
            document.categories.clear()
            for category_name in categories_data:
                try:
                    category = DocumentCategory.objects.get(name=category_name)
                    document.categories.add(category)
                except DocumentCategory.DoesNotExist:
                    pass  # Skip invalid categories

        # Get or create DateTimeInfo (match by active_glow, sol, and solar_year)
        date_time, _ = DateTimeInfo.objects.get_or_create(
            active_glow=date_time_data['active_glow'],
            sol=date_time_data['sol'],
            solar_year=date_time_data['solar_year']
        )

        # Create TimeLineEvent
        timeline_event = TimeLineEvent.objects.create(
            document=document,
            date_time=date_time
        )

        return timeline_event
