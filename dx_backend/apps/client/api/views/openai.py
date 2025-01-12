from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.client.api.serializers.openapi import OpenAIClientManagementSerializer, RegistrationFormSerializer
from apps.client.models import Client


class OpenAIClientManagementViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_active=True, provider=Client.ClientProvider.openai)
    serializer_class = OpenAIClientManagementSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['post'],
            permission_classes=[permissions.AllowAny],
            serializer_class=RegistrationFormSerializer,
            authentication_classes=[],
            )
    def register_local_client(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
