from rest_framework import serializers

from apps.gallery.models import Art


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = ['id', 'name', 'description', 'image']
