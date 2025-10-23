"""
Google OAuth 2.0 Authentication
"""
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')

async def verify_google_token(token: str) -> dict:
    """
    Verify Google ID token and return user information
    """
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Check if the token is for our client ID
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            raise ValueError('Invalid audience')

        # Token is valid, return user info
        return {
            'google_id': idinfo['sub'],
            'email': idinfo['email'],
            'email_verified': idinfo.get('email_verified', False),
            'name': idinfo.get('name', ''),
            'picture': idinfo.get('picture', ''),
            'given_name': idinfo.get('given_name', ''),
            'family_name': idinfo.get('family_name', '')
        }
    except ValueError as e:
        # Invalid token
        raise ValueError(f'Invalid Google token: {str(e)}')
    except Exception as e:
        raise Exception(f'Error verifying Google token: {str(e)}')
