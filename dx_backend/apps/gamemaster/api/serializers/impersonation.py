from rest_framework import serializers


class ImpersonationRequestSerializer(serializers.Serializer):
    """
    Serializer for the impersonation request.
    """
    character_id = serializers.UUIDField(
        help_text="UUID of the character to impersonate"
    )


class ImpersonationResponseSerializer(serializers.Serializer):
    """
    Serializer for the impersonation response.
    """
    refresh = serializers.CharField(
        help_text="JWT refresh token for the impersonated user"
    )
    access = serializers.CharField(
        help_text="JWT access token for the impersonated user"
    )