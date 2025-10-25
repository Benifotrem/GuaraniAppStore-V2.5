from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, UserRole
from database import get_db
from database_mongo import users_collection
import pyotp
import secrets
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# JWT settings
JWT_SECRET = os.environ.get('JWT_SECRET', 'guarani-app-store-secret-key-2025-ultra-secure')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', '720'))

# Security
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get('sub')
    if user_id is None:
        raise credentials_exception
    
    # Try PostgreSQL first
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise credentials_exception
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User account is inactive'
            )
        
        return user
        
    except Exception as e:
        # Fallback to MongoDB
        logger.warning(f"PostgreSQL not available for auth, using MongoDB fallback")
        
        # Try to find by string ID first, then by ObjectId
        from bson import ObjectId
        
        user_data = await users_collection.find_one({'id': user_id})
        if user_data is None:
            # Try with _id as ObjectId
            try:
                user_data = await users_collection.find_one({'_id': ObjectId(user_id)})
            except:
                pass
        
        if user_data is None:
            raise credentials_exception
        
        # Convert _id to string for ID
        mongo_user_id = str(user_data.get('_id', user_data.get('id', user_id)))
        
        # Create User object from MongoDB data
        user = User(
            id=mongo_user_id,
            email=user_data.get('email'),
            full_name=user_data.get('name', user_data.get('full_name', 'User')),
            hashed_password=user_data.get('password', user_data.get('hashed_password', '')),
            is_active=user_data.get('is_active', True),
            is_admin=user_data.get('is_admin', False),
            role=UserRole.ADMIN if user_data.get('is_admin') else UserRole.USER,
            created_at=user_data.get('created_at', datetime.utcnow()),
            country=user_data.get('country', 'Paraguay'),
            timezone=user_data.get('timezone', 'America/Asuncion'),
            language=user_data.get('language', 'es'),
            whatsapp_number=user_data.get('whatsapp_number'),
            telegram_username=user_data.get('telegram_username'),
            is_verified=user_data.get('is_verified', True),
            verification_token=user_data.get('verification_token'),
            two_factor_enabled=user_data.get('two_factor_enabled', False),
            two_factor_secret=user_data.get('two_factor_secret')
        )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User account is inactive'
            )
        
        return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions'
        )
    return current_user

def generate_2fa_secret() -> str:
    return pyotp.random_base32()

def verify_2fa_token(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)
