from django.conf import settings
from django.contrib.auth import login
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from google.auth.transport import requests
from google.oauth2 import id_token
import logging

from apps.client.models import Client

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_oauth_login(request):
    """
    Google OAuth login endpoint that handles Google ID token verification,
    user creation/authentication, and JWT token generation with cookie setting.
    
    Expected request data:
    {
        "id_token": "google_id_token_from_frontend"
    }
    
    Returns JWT tokens and sets dx_backend_token cookie for seamless integration
    with existing authentication system.
    """
    try:
        # Get the Google ID token from request
        google_id_token = request.data.get('id_token')
        if not google_id_token:
            return Response(
                {'error': 'Google ID token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify the Google ID token
        try:
            # You'll need to set GOOGLE_OAUTH2_CLIENT_ID in your settings
            idinfo = id_token.verify_oauth2_token(
                google_id_token, 
                requests.Request(), 
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )
            
            # Verify the token is for our application
            if idinfo['aud'] != settings.GOOGLE_OAUTH2_CLIENT_ID:
                return Response(
                    {'error': 'Invalid token audience'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ValueError as e:
            logger.error(f"Google token verification failed: {e}")
            return Response(
                {'error': 'Invalid Google token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract user information from Google token
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        
        if not email:
            return Response(
                {'error': 'Email not provided by Google'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create user
        client, created = Client.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'provider': Client.ClientProvider.google,
                'is_active': True,
            }
        )
        
        # If user exists but was created with different provider, update to Google
        if not created and client.provider != Client.ClientProvider.google:
            client.provider = Client.ClientProvider.google
            client.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(client)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Prepare response data
        response_data = {
            'access': access_token,
            'refresh': refresh_token,
            'user': {
                'id': str(client.id),
                'email': client.email,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'provider': client.provider,
            },
            'created': created
        }

        # Create response and set cookie
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set the dx_backend_token cookie to match existing authentication system
        response.set_cookie(
            'dx_backend_token',
            access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            secure=not settings.DEBUG,  # Use secure cookies in production
            samesite='Lax'
        )
        
        logger.info(f"Google OAuth login successful for user: {email}, created: {created}")
        return response

    except Exception as e:
        logger.error(f"Google OAuth login error: {e}")
        return Response(
            {'error': 'Internal server error'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_oauth_url(request):
    """
    Returns the Google OAuth URL for frontend to redirect users to.
    This is optional - frontend can construct this URL directly.
    """
    try:
        # Construct Google OAuth URL
        google_oauth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&"
            f"redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}&"
            f"scope=openid email profile&"
            f"response_type=code&"
            f"access_type=offline"
        )
        
        return Response({
            'oauth_url': google_oauth_url
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error generating Google OAuth URL: {e}")
        return Response(
            {'error': 'Failed to generate OAuth URL'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )