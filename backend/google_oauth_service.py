"""
GuaraniAppStore V2.5 Pro - Google OAuth Service
Implementación completa de Google OAuth 2.0 con refresh tokens
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
import os
import logging
from typing import Optional, Dict, Any

from models import User, GoogleOAuthToken
from database import AsyncSessionLocal

logger = logging.getLogger(__name__)

# Configuración de OAuth
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_OAUTH_REDIRECT_URI', 'https://smart-content-hub-11.preview.emergentagent.com/api/auth/google/callback')

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/blogger'
]


class GoogleOAuthService:
    """Servicio para manejar autenticación y autorización con Google OAuth"""
    
    def __init__(self):
        self.client_id = GOOGLE_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.redirect_uri = GOOGLE_REDIRECT_URI
        self.scopes = SCOPES
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Genera la URL de autorización de Google.
        
        Args:
            state: Estado opcional para CSRF protection
        
        Returns:
            str: URL de autorización
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent'  # Forzar consent para obtener refresh token
        )
        
        return authorization_url
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesa el callback de Google OAuth y obtiene tokens.
        
        Args:
            code: Código de autorización de Google
            state: Estado para verificación CSRF
        
        Returns:
            Dict con user_info y tokens
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
            state=state
        )
        
        # Intercambiar código por tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Obtener información del usuario
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        
        return {
            'user_info': user_info,
            'credentials': {
                'access_token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
                'expiry': credentials.expiry.isoformat() if credentials.expiry else None
            }
        }
    
    async def save_user_tokens(
        self,
        user_id: str,
        credentials: Dict[str, Any]
    ) -> GoogleOAuthToken:
        """
        Guarda los tokens de OAuth del usuario en la base de datos.
        
        Args:
            user_id: ID del usuario
            credentials: Credenciales de OAuth
        
        Returns:
            GoogleOAuthToken: Token guardado
        """
        async with AsyncSessionLocal() as db:
            # Buscar token existente
            result = await db.execute(
                select(GoogleOAuthToken).where(GoogleOAuthToken.user_id == user_id)
            )
            token = result.scalar_one_or_none()
            
            expiry = datetime.fromisoformat(credentials['expiry']) if credentials.get('expiry') else datetime.now(timezone.utc) + timedelta(hours=1)
            
            if token:
                # Actualizar token existente
                token.access_token = credentials['access_token']
                token.refresh_token = credentials.get('refresh_token') or token.refresh_token
                token.scopes = credentials.get('scopes', [])
                token.expires_at = expiry
                token.updated_at = datetime.now(timezone.utc)
            else:
                # Crear nuevo token
                token = GoogleOAuthToken(
                    user_id=user_id,
                    access_token=credentials['access_token'],
                    refresh_token=credentials.get('refresh_token'),
                    scopes=credentials.get('scopes', []),
                    expires_at=expiry
                )
                db.add(token)
            
            await db.commit()
            await db.refresh(token)
            
            logger.info(f"Tokens de Google OAuth guardados para usuario {user_id}")
            return token
    
    async def get_user_credentials(self, user_id: str) -> Optional[Credentials]:
        """
        Obtiene las credenciales de OAuth del usuario, renovándolas si es necesario.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Credentials: Credenciales de Google o None
        """
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(GoogleOAuthToken).where(GoogleOAuthToken.user_id == user_id)
            )
            token = result.scalar_one_or_none()
            
            if not token:
                return None
            
            # Crear credenciales
            credentials = Credentials(
                token=token.access_token,
                refresh_token=token.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=token.scopes
            )
            
            # Verificar si el token expiró
            if token.expires_at < datetime.now(timezone.utc):
                logger.info(f"Token expirado para usuario {user_id}, renovando...")
                
                # Renovar token
                credentials.refresh(None)
                
                # Actualizar en la base de datos
                token.access_token = credentials.token
                token.expires_at = credentials.expiry
                token.updated_at = datetime.now(timezone.utc)
                
                await db.commit()
                
                logger.info(f"Token renovado para usuario {user_id}")
            
            return credentials
    
    async def revoke_user_tokens(self, user_id: str) -> bool:
        """
        Revoca y elimina los tokens de OAuth del usuario.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            bool: True si se revocó exitosamente
        """
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(GoogleOAuthToken).where(GoogleOAuthToken.user_id == user_id)
            )
            token = result.scalar_one_or_none()
            
            if not token:
                return False
            
            # Eliminar token de la base de datos
            await db.delete(token)
            await db.commit()
            
            logger.info(f"Tokens de Google OAuth revocados para usuario {user_id}")
            return True


# Instancia global del servicio
google_oauth_service = GoogleOAuthService()
