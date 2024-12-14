from rest_framework import serializers


class ConnectSerializer(serializers.Serializer):
    """
    "client": "435f309f-32f4-485d-9b88-6c2daca71555",
    "transport": "websocket",
    "protocol": "json",
    "encoding": "json",
    "name": "js"
    """
    client = serializers.UUIDField()
    transport = serializers.CharField()
    protocol = serializers.CharField()
    encoding = serializers.CharField()
    name = serializers.CharField()


class PublishSerializer(serializers.Serializer):
    channel = serializers.CharField()
    data = serializers.JSONField()


class SubscribeSerializer(serializers.Serializer):
    channel = serializers.CharField()
