from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

# Enums
class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'

class ServiceStatus(str, enum.Enum):
    ACTIVE = 'active'
    COMING_SOON = 'coming_soon'
    INACTIVE = 'inactive'

class PaymentStatus(str, enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class LeadStatus(str, enum.Enum):
    NEW = 'new'
    CONTACTED = 'contacted'
    QUALIFIED = 'qualified'
    CONVERTED = 'converted'
    LOST = 'lost'

# Models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)  # Nullable para usuarios de Google OAuth
    full_name = Column(String, nullable=False)
    google_id = Column(String, unique=True, nullable=True, index=True)  # Google OAuth ID
    profile_picture = Column(String, nullable=True)  # URL de foto de perfil
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    country = Column(String, default='Paraguay', nullable=False)  # País del usuario
    timezone = Column(String, default='America/Asuncion', nullable=False)  # Zona horaria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    leads = relationship('Lead', back_populates='user')
    subscriptions = relationship('Subscription', back_populates='user')
    payments = relationship('Payment', back_populates='user')
    conversations = relationship('Conversation', back_populates='user')

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String, nullable=True)
    price_monthly = Column(Float, nullable=False)
    price_annual = Column(Float, nullable=True)
    currency = Column(String, default='USD')
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.COMING_SOON)
    icon = Column(String, nullable=True)
    features = Column(JSON, nullable=True)  # List of features
    ai_model = Column(String, nullable=True)  # Claude, GPT-4, etc.
    category = Column(String, nullable=True)  # 'automation', 'crypto', 'analysis'
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
    
    # Relationships
    subscriptions = relationship('Subscription', back_populates='service')

class Lead(Base):
    __tablename__ = 'leads'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    source = Column(String, nullable=True)  # 'website', 'chatbot', 'telegram'
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW)
    score = Column(Integer, default=0)  # 0-100 scoring
    extra_data = Column(JSON, nullable=True)  # Additional data
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
    
    # Relationships
    user = relationship('User', back_populates='leads')
    conversations = relationship('Conversation', back_populates='lead')

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    lead_id = Column(String, ForeignKey('leads.id'), nullable=True)
    agent_name = Column(String, nullable=False)  # Junior, Jacinto, Alex, etc.
    channel = Column(String, nullable=False)  # 'chatbot', 'telegram', 'email'
    messages = Column(JSON, nullable=False, default=list)  # Array of messages
    context = Column(JSON, nullable=True)  # Conversation context
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
    
    # Relationships
    user = relationship('User', back_populates='conversations')
    lead = relationship('Lead', back_populates='conversations')

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    service_id = Column(String, ForeignKey('services.id'), nullable=False)
    plan_type = Column(String, nullable=False)  # 'monthly', 'annual'
    status = Column(String, nullable=False)  # 'active', 'cancelled', 'expired'
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)
    price_paid = Column(Float, nullable=False)
    currency = Column(String, default='USD')
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
    
    # Relationships
    user = relationship('User', back_populates='subscriptions')
    service = relationship('Service', back_populates='subscriptions')

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default='USD')
    payment_method = Column(String, nullable=False)  # 'paypal', 'pagopar', 'crypto', etc.
    transaction_id = Column(String, nullable=True)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
    
    # Relationships
    user = relationship('User', back_populates='payments')

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Content
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    excerpt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)  # Markdown
    image_url = Column(Text, nullable=True)
    image_prompt = Column(Text, nullable=True)  # Prompt usado para generar la imagen
    
    # Author (Agent)
    author_name = Column(String(255), nullable=False)
    author_role = Column(String(255), nullable=False)
    author_avatar = Column(Text, nullable=True)
    author_id = Column(Integer, nullable=True)  # 1-6 for agents, 0 for CEO
    day_of_week = Column(Integer, nullable=True)  # 0-6 (Monday-Sunday), NULL para manuales
    
    # SEO
    meta_description = Column(String(500), nullable=True)
    tags = Column(JSON, nullable=True, default=list)  # ['tag1', 'tag2']
    keywords = Column(JSON, nullable=True, default=list)  # ['keyword1', 'keyword2']
    
    # Publishing
    published = Column(Boolean, default=False)
    published_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Approval System
    pending_approval = Column(Boolean, default=False)
    requested_by = Column(String(255), nullable=True)
    requested_at = Column(TIMESTAMP(timezone=True), nullable=True)
    approved_by = Column(String(255), nullable=True)
    approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    search_query = Column(Text, nullable=True)  # Consulta original del admin
    generation_type = Column(String(50), default='scheduled')  # 'scheduled' o 'manual'
    
    # Analytics
    views = Column(Integer, default=0)
    reading_time = Column(Integer, nullable=True)  # Minutos estimados
    
    # Metadata
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, index=True)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class PasswordReset(Base):
    __tablename__ = 'password_resets'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    token = Column(String, nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    service_id = Column(String, ForeignKey('services.id'), nullable=False)
    order_number = Column(String, unique=True, nullable=False, index=True)  # ORD-XXXXXX
    
    # Pricing
    plan_type = Column(String, nullable=False)  # 'monthly', 'annual', 'one_time'
    platform = Column(String, nullable=True)  # 'whatsapp', 'telegram', 'web', null
    base_price = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0)  # 20% telegram, 25% crypto
    final_price = Column(Float, nullable=False)
    currency = Column(String, default='PYG')
    
    # Payment
    payment_method = Column(String, nullable=False)  # 'pagopar', 'btc', 'eth', 'usdt'
    payment_status = Column(String, default='pending')  # 'pending', 'completed', 'failed', 'expired'
    payment_id = Column(String, nullable=True)  # External payment ID
    payment_url = Column(String, nullable=True)  # Payment redirect URL
    payment_expires_at = Column(DateTime, nullable=True)
    
    # Crypto specific
    crypto_address = Column(String, nullable=True)  # Wallet address to send
    crypto_amount = Column(String, nullable=True)  # Amount in crypto
    crypto_tx_hash = Column(String, nullable=True)  # Transaction hash
    
    # Metadata
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id])
    service = relationship('Service', foreign_keys=[service_id])

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, ForeignKey('orders.id'), nullable=False)
    transaction_type = Column(String, nullable=False)  # 'payment', 'refund', 'chargeback'
    amount = Column(Float, nullable=False)
    currency = Column(String, default='PYG')
    status = Column(String, nullable=False)  # 'pending', 'completed', 'failed'
    
    # Payment gateway data
    gateway = Column(String, nullable=False)  # 'pagopar', 'crypto'
    gateway_transaction_id = Column(String, nullable=True)
    gateway_response = Column(JSON, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship('Order', foreign_keys=[order_id])


class PaymentGatewayConfig(Base):
    __tablename__ = 'payment_gateway_configs'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    gateway_name = Column(String, unique=True, nullable=False)  # 'paypal', 'bancard', etc.
    is_enabled = Column(Boolean, default=False)
    
    # Configuration fields (JSON for flexibility)
    config = Column(JSON, nullable=False)  # Stores all API keys, secrets, etc.
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String, ForeignKey('users.id'), nullable=True)



# ========================================
# CHAT MEMORY SYSTEM - PostgreSQL Backend
# ========================================

class ChatSession(Base):
    """
    Almacena sesiones de chat entre usuarios/visitantes y agentes.
    Retiene contexto por 30 días.
    """
    __tablename__ = 'chat_sessions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Identificación
    user_id = Column(String, ForeignKey('users.id'), nullable=True)  # Usuario registrado (opcional)
    visitor_id = Column(String, nullable=True, index=True)  # ID anónimo para visitantes no registrados
    agent_name = Column(String, nullable=False, index=True)  # 'junior', 'jacinto', 'alex', 'rocio', 'silvia', 'blanca'
    
    # Metadata de sesión
    first_interaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_interaction_date = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    total_messages = Column(Integer, default=0)
    
    # Contexto persistente
    context_summary = Column(Text, nullable=True)  # Resumen del contexto para cargar rápidamente
    user_preferences = Column(JSON, nullable=True)  # Preferencias detectadas del usuario
    
    # Control de sesión
    is_active = Column(Boolean, default=True)
    session_metadata = Column(JSON, nullable=True)  # IP, User-Agent, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship('ChatMessage', back_populates='session', cascade='all, delete-orphan')
    user = relationship('User', foreign_keys=[user_id])


class ChatMessage(Base):
    """
    Almacena mensajes individuales de cada sesión de chat.
    Incluye lógica de limpieza automática para mensajes > 30 días.
    """
    __tablename__ = 'chat_messages'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey('chat_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Contenido del mensaje
    role = Column(String, nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    
    # Metadata del mensaje
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    token_count = Column(Integer, nullable=True)  # Conteo de tokens del mensaje
    model_used = Column(String, nullable=True)  # 'claude-3.5-sonnet', 'gpt-4', etc.
    
    # Análisis del mensaje
    sentiment = Column(String, nullable=True)  # 'positive', 'neutral', 'negative'
    intent = Column(String, nullable=True)  # Intención detectada
    
    # Metadata adicional
    message_metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship('ChatSession', back_populates='messages')


class GoogleOAuthToken(Base):
    """
    Almacena tokens de OAuth de Google para usuarios.
    Incluye refresh tokens para renovación automática.
    """
    __tablename__ = 'google_oauth_tokens'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Tokens
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_type = Column(String, default='Bearer')
    
    # Scopes y expiración
    scopes = Column(JSON, nullable=True)  # Lista de scopes autorizados
    expires_at = Column(DateTime, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id])
