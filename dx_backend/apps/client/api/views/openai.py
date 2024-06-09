from rest_framework import viewsets, permissions

from apps.client.api.serializers.openapi import OpenAIClientManagementSerializer
from apps.client.models import Client


class OpenAIClientManagementViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_active=True, provider=Client.ClientProvider.openai)
    serializer_class = OpenAIClientManagementSerializer
    permission_classes = [permissions.IsAdminUser]

