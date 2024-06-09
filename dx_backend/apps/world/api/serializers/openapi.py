from rest_framework import serializers


from apps.world.models import Area, Location, Dimension, City, SubLocation


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocation
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    sub_locations = SubLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = "__all__"