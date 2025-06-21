from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.character.models import Character
from apps.gamemaster.api.serializers.impersonation import ImpersonationRequestSerializer, ImpersonationResponseSerializer

User = get_user_model()


class GameMasterImpersonationViewSet(ViewSet):
    """
    ViewSet for game masters to impersonate users.
    This viewset provides an endpoint for game masters to get a login token for any user.
    """
    permission_classes = [permissions.IsAdminUser]

    @extend_schema(
        description="Get a login token for a user based on a character ID",
        request=ImpersonationRequestSerializer,
        responses={
            200: ImpersonationResponseSerializer,
            400: {"type": "object", "properties": {"detail": {"type": "string"}}},
            404: {"type": "object", "properties": {"detail": {"type": "string"}}},
            500: {"type": "object", "properties": {"detail": {"type": "string"}}}
        },
        tags=["gamemaster"]
    )
    @action(detail=False, methods=['post'])
    def impersonate(self, request):
        """
        Get a login token for a user based on a character ID.

        This endpoint allows game masters to impersonate any user by providing a character ID.
        It returns a refresh token and an access token that can be used to authenticate as the user.
        """
        # Validate request data
        serializer = ImpersonationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid request data.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        character_id = serializer.validated_data['character_id']

        try:
            # Find the character
            character = Character.objects.get(id=character_id)

            # Get the user who owns the character
            owner = character.owner

            if not owner:
                return Response(
                    {"detail": "Character has no associated owner."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Generate tokens for the user
            refresh = RefreshToken.for_user(owner)

            # Format response using the response serializer
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            response_serializer = ImpersonationResponseSerializer(data=response_data)
            response_serializer.is_valid()

            return Response(response_serializer.data)

        except Character.DoesNotExist:
            return Response(
                {"detail": "Character not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
