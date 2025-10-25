from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import UserRole, ServiceStatus, PaymentStatus, LeadStatus

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    phone: Optional[str] = None
    company: Optional[str] = None
    country: str = 'Paraguay'  # País del usuario
    timezone: Optional[str] = None  # Se calcula automáticamente si no se provee

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    two_factor_token: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    email: str
    full_name: str
    role: UserRole
    is_admin: bool = False
    is_active: bool
    is_verified: bool
    two_factor_enabled: bool
    phone: Optional[str] = None
    company: Optional[str] = None
    country: str
    timezone: str
    profile_picture: Optional[str] = None
    google_id: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse

# Service Schemas
class ServiceCreate(BaseModel):
    name: str
    slug: str
    description: str
    short_description: Optional[str] = None
    price_monthly: float
    price_annual: Optional[float] = None
    price_annual_crypto: Optional[float] = None
    price_crypto: Optional[float] = None
    currency: str = 'USD'
    billing_type: Optional[str] = 'subscription'  # one_time, subscription, freemium_packs
    no_expiration: Optional[bool] = False
    requires_messaging: Optional[bool] = False
    multi_purchase: Optional[bool] = False
    packs: Optional[List[dict]] = None
    status: ServiceStatus = ServiceStatus.COMING_SOON
    icon: Optional[str] = None
    features: Optional[List[str]] = None
    ai_model: Optional[str] = None
    category: Optional[str] = None
    order: int = 0

class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str
    slug: str
    description: str
    short_description: Optional[str] = None
    price_monthly: float
    price_annual: Optional[float] = None
    price_annual_crypto: Optional[float] = None
    price_crypto: Optional[float] = None
    price_monthly_telegram: Optional[float] = None
    price_annual_telegram: Optional[float] = None
    price_annual_crypto_telegram: Optional[float] = None
    currency: str
    billing_type: Optional[str] = 'subscription'
    billing_period: Optional[str] = None
    no_expiration: Optional[bool] = False
    requires_messaging: Optional[bool] = False
    platform: Optional[str] = None
    telegram_discount: Optional[int] = None
    multi_purchase: Optional[bool] = False
    packs: Optional[List[dict]] = None
    included_services: Optional[List[dict]] = None
    status: ServiceStatus
    icon: Optional[str] = None
    features: Optional[List[str]] = None
    ai_model: Optional[str] = None
    category: Optional[str] = None
    order: int
    created_at: datetime

# Lead Schemas
class LeadCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = 'website'

class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    status: LeadStatus
    score: int
    source: Optional[str] = None
    created_at: datetime

# Conversation Schemas
class MessageCreate(BaseModel):
    content: str
    agent_name: Optional[str] = 'Junior'

class ConversationCreate(BaseModel):
    agent_name: str = 'Junior'
    channel: str = 'chatbot'
    initial_message: Optional[str] = None

class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    agent_name: str
    channel: str
    messages: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime

# Chatbot Schemas
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    agent_name: str = 'Junior'
    conversation_id: Optional[str] = None
    user_email: Optional[str] = None
    user_id: Optional[str] = None  # ID de usuario registrado
    visitor_id: Optional[str] = None  # ID de visitante anónimo
    user_agent: Optional[str] = None  # User-Agent del navegador

class ChatResponse(BaseModel):
    response: str
    agent_name: str
    conversation_id: str
    timestamp: datetime

# Blog Schemas
class BlogPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    slug: str
    excerpt: str
    content: str
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None
    author_name: str
    author_role: str
    author_avatar: Optional[str] = None
    author_id: Optional[int] = None
    day_of_week: Optional[int] = None
    meta_description: Optional[str] = None
    tags: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    published: bool
    published_at: Optional[datetime] = None
    pending_approval: bool = False
    requested_by: Optional[str] = None
    requested_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    search_query: Optional[str] = None
    generation_type: str = 'scheduled'
    views: int = 0
    reading_time: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class ManualArticleRequest(BaseModel):
    """Request para generar artículo bajo demanda"""
    search_query: str
    target_keywords: Optional[List[str]] = []
    agent_id: Optional[int] = None
    tone: str = "profesional"
    length: str = "medium"
    include_faq: bool = True


class BlogStatsResponse(BaseModel):
    """Estadísticas del blog"""
    total_posts: int
    published_posts: int
    draft_posts: int
    total_views: int
    avg_views_per_post: float

# Payment Schemas
class PaymentCreate(BaseModel):
    amount: float
    currency: str = 'USD'
    payment_method: str
    metadata: Optional[Dict[str, Any]] = None

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    amount: float
    currency: str
    payment_method: str
    transaction_id: Optional[str] = None
    status: PaymentStatus
    created_at: datetime

# Password Reset Schemas
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

# 2FA Schemas
class TwoFactorEnable(BaseModel):
    password: str

class TwoFactorVerify(BaseModel):
    token: str

# Order Schemas
class OrderCreate(BaseModel):
    service_id: str
    plan_type: str  # 'monthly', 'annual', 'one_time'
    platform: Optional[str] = None  # 'whatsapp', 'telegram', 'web'
    payment_method: str  # 'pagopar', 'btc', 'eth', 'usdt'

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    order_number: str
    service_id: str
    plan_type: str
    platform: Optional[str] = None
    base_price: float
    discount_percentage: float
    final_price: float
    currency: str
    payment_method: str
    payment_status: str
    payment_url: Optional[str] = None
    crypto_address: Optional[str] = None
    crypto_amount: Optional[str] = None
    created_at: datetime

class CryptoPaymentVerify(BaseModel):
    order_id: str
    tx_hash: str
