from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.client.api.serializers.openapi import (
    OpenAIClientManagementSerializer,
    RegistrationFormSerializer,
    OpenAICampaignSerializer,
    CurrentCampaignSerializer,
    CurrentClientInfoSerializer
)
from apps.client.models import Client
from apps.game.models import Campaign


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


class OpenAICampaignManagementViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing campaigns for OpenAI clients.

    This viewset provides functionality to:
    - List all campaigns for the current client (both as player and as master)
    - Get the current campaign
    - Update the current campaign

    This viewset is used on Game UI for clients so they can choose which campaign they want to play in.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OpenAICampaignSerializer
    queryset = Campaign.objects.all()

    def get_queryset(self):
        """
        Return all campaigns where the current user is either a player or a master.
        Only return active campaigns.
        """
        if not self.request.user.is_authenticated:
            return Campaign.objects.none()

        client = self.request.user
        return (Campaign.objects.filter(players=client, is_active=True) |
                Campaign.objects.filter(masters=client, is_active=True)).distinct()

    @action(detail=False, methods=['get'])
    def list_campaigns(self, request):
        """
        List all campaigns for the current client (both as player and as master).
        Returns only active campaigns.
        """
        queryset = self.get_queryset()

        # Add filtering options
        is_completed = request.query_params.get('is_completed', None)
        if is_completed is not None:
            is_completed = is_completed.lower() == 'true'
            queryset = queryset.filter(is_completed=is_completed)

        # Add sorting options
        sort_by = request.query_params.get('sort_by', 'name')
        if sort_by not in ['name', '-name', 'id', '-id']:
            sort_by = 'name'
        queryset = queryset.order_by(sort_by)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def current_campaign(self, request):
        """
        Get the current campaign for the client.

        Returns the current campaign ID and its details. If no current campaign is set,
        the current_campaign field will be null.
        """
        client = request.user
        serializer = CurrentCampaignSerializer(client, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, methods=['post'], serializer_class=serializers.Serializer)
    def set_current_campaign(self, request, pk=None):
        """
        Set the current campaign for the client.

        The campaign must be active and the client must be either a player or a master in the campaign.
        """
        campaign = self.get_object()  # Ensure the viewset is properly initialized
        client = request.user
        client.current_campaign = campaign
        client.save()
        serializer = CurrentCampaignSerializer(client)
        return Response(serializer.data)


class CurrentClientViewSet(viewsets.GenericViewSet):
    """
    ViewSet to get the current authenticated client.

    This viewset provides a single endpoint to retrieve the current client's details.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrentClientInfoSerializer

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get'])
    def info(self, request):
        """
        Get the basic information of the current authenticated client.
        This enpoint used by game client to get current client information
        It contains information about: is_active, current_campaign, main_character, play_campaigns, master_campaigns, owned_characters
        """
        client = self.get_object()
        serializer = CurrentClientInfoSerializer(client, context=self.get_serializer_context())
        return Response(serializer.data)
