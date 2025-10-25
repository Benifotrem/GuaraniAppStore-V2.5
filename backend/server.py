from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from cloudflare_middleware import CloudflareMiddleware
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone, timedelta
import secrets

# Import modules
from database import get_db, engine, Base
from database_mongo import db as mongodb, services_collection, users_collection, orders_collection, transactions_collection
from models import User, Service, Lead, Conversation, BlogPost, PasswordReset, Payment, UserRole, Order, Transaction, ChatSession, ChatMessage
from schemas import (
    UserCreate, UserLogin, UserResponse, TokenResponse,
    ServiceCreate, ServiceResponse,
    LeadCreate, LeadResponse,
    ConversationCreate, ConversationResponse,
    ChatRequest, ChatResponse,
    BlogPostResponse, ManualArticleRequest, BlogStatsResponse,
    PaymentCreate, PaymentResponse,
    PasswordResetRequest, PasswordResetConfirm,
    TwoFactorEnable, TwoFactorVerify,
    OrderCreate, OrderResponse, CryptoPaymentVerify
)
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_current_admin_user,
    generate_2fa_secret, verify_2fa_token, generate_reset_token
)
from ai_service import chat_with_claude, generate_blog_content
from timezone_utils import get_timezone_for_country, SUPPORTED_COUNTRIES
from google_auth import verify_google_token
from payment_service import (
    calculate_price_with_discount,
    generate_order_number,
    create_pagopar_payment,
    get_crypto_wallet,
    convert_pyg_to_crypto,
    verify_crypto_payment
)
from external_apis_service import (
    vision_service,
    crypto_service,
    blockchain_service,
    google_oauth_service
)
from telegram_webhook_service import webhook_manager
from document_processor_service import document_processor

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create FastAPI app
app = FastAPI(title='GuaraniAppStore API', version='2.5.0')

# Create API router with /api prefix
api_router = APIRouter(prefix='/api')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add Cloudflare middleware (debe ir ANTES de CORS)
app.add_middleware(CloudflareMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=['*'],
    allow_headers=['*'],
)

# Startup event
@app.on_event('startup')
async def startup():
    logger.info('Starting GuaraniAppStore API...')
    
    # Create database tables (PostgreSQL)
    try:
        from database import engine, Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info('✅ PostgreSQL tables created successfully')
        
        # Iniciar Blog Scheduler (requiere PostgreSQL)
        try:
            from blog_scheduler import start_blog_scheduler
            start_blog_scheduler()
            logger.info('✅ Blog Scheduler started successfully')
        except Exception as e:
            logger.warning(f'⚠️ Blog Scheduler not started: {str(e)}')
            
    except Exception as e:
        logger.warning(f'⚠️ PostgreSQL not available: {str(e)}')
        logger.info('📌 Running in MongoDB-only mode (Blog features disabled)')
    
    logger.info('✅ API started successfully')

# Shutdown event
@app.on_event('shutdown')
async def shutdown():
    logger.info('Shutting down GuaraniAppStore API...')
    
    # Detener Blog Scheduler
    try:
        from blog_scheduler import stop_blog_scheduler
        stop_blog_scheduler()
        logger.info('Blog Scheduler stopped')
    except Exception as e:
        logger.error(f'Error stopping Blog Scheduler: {str(e)}')
    
    from database import engine
    await engine.dispose()

# ============================================
# PUBLIC ROUTES
# ============================================

@api_router.get('/')
async def root():
    return {
        'message': 'GuaraniAppStore API V2.5 Pro',
        'status': 'active',
        'version': '2.5.0'
    }

@api_router.get('/health')
async def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}

@api_router.get('/countries')
async def get_countries():
    """Get list of supported countries with their timezones"""
    from timezone_utils import COUNTRY_TIMEZONES
    return {
        'countries': [
            {'name': country, 'timezone': tz}
            for country, tz in COUNTRY_TIMEZONES.items()
        ],
        'default': 'Paraguay'
    }

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@api_router.post('/auth/register', response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    # Check if user exists
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    
    # Determine timezone from country
    timezone = user_data.timezone
    if not timezone:
        timezone = get_timezone_for_country(user_data.country)
    
    # Create user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        company=user_data.company,
        country=user_data.country,
        timezone=timezone,
        role=UserRole.USER
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token({'sub': new_user.id})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(new_user)
    )

@api_router.post('/auth/login', response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login user - Works with both PostgreSQL and MongoDB"""
    try:
        # Try PostgreSQL first
        result = await db.execute(select(User).filter(User.email == credentials.email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )
        
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )
        
        # Check 2FA if enabled
        if user.two_factor_enabled:
            if not credentials.two_factor_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='2FA token required'
                )
            
            if not verify_2fa_token(user.two_factor_secret, credentials.two_factor_token):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid 2FA token'
                )
        
        # Update last login
        user.last_login = datetime.utcnow()
        await db.commit()
        
        # Create access token
        access_token = create_access_token({'sub': user.id})
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user)
        )
        
    except Exception as pg_error:
        # Fallback to MongoDB if PostgreSQL fails
        logger.warning(f'PostgreSQL login failed, trying MongoDB: {str(pg_error)}')
        
        # Find user in MongoDB
        mongo_user = await users_collection.find_one({'email': credentials.email})
        
        if not mongo_user or not verify_password(credentials.password, mongo_user.get('password', '')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )
        
        # Create access token with MongoDB user ID
        user_id = str(mongo_user.get('_id', mongo_user.get('id', '')))
        access_token = create_access_token({'sub': user_id})
        
        # Return response with MongoDB user data
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user_id,
                email=mongo_user.get('email'),
                full_name=mongo_user.get('name', 'User'),
                role=UserRole.ADMIN if mongo_user.get('is_admin') else UserRole.USER,
                is_active=True,
                is_verified=True,
                two_factor_enabled=False,
                phone=mongo_user.get('phone'),
                company=mongo_user.get('company'),
                country=mongo_user.get('country', 'Paraguay'),
                timezone=mongo_user.get('timezone', 'America/Asuncion'),
                profile_picture=mongo_user.get('profile_picture'),
                google_id=mongo_user.get('google_id'),
                created_at=mongo_user.get('created_at', datetime.utcnow()),
                last_login=mongo_user.get('last_login')
            )
        )

@api_router.post('/auth/google', response_model=TokenResponse)
async def google_login(
    google_token: dict,
    db: AsyncSession = Depends(get_db)
):
    """Login or register with Google OAuth"""
    try:
        # Verify Google token
        user_info = await verify_google_token(google_token.get('token', ''))
        
        # Check if user exists by Google ID
        result = await db.execute(
            select(User).filter(User.google_id == user_info['google_id'])
        )
        user = result.scalar_one_or_none()
        
        # If not found by Google ID, check by email
        if not user:
            result = await db.execute(
                select(User).filter(User.email == user_info['email'])
            )
            user = result.scalar_one_or_none()
        
        # Create new user if doesn't exist
        if not user:
            # Get timezone from country (default Paraguay)
            timezone = get_timezone_for_country('Paraguay')
            
            user = User(
                email=user_info['email'],
                full_name=user_info['name'],
                google_id=user_info['google_id'],
                profile_picture=user_info.get('picture'),
                is_verified=user_info.get('email_verified', False),
                country='Paraguay',
                timezone=timezone,
                role=UserRole.USER
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            # Update Google ID and profile picture if not set
            if not user.google_id:
                user.google_id = user_info['google_id']
            if not user.profile_picture:
                user.profile_picture = user_info.get('picture')
            if not user.is_verified and user_info.get('email_verified'):
                user.is_verified = True
            
            user.last_login = datetime.utcnow()
            await db.commit()
            await db.refresh(user)
        
        # Create access token
        access_token = create_access_token({'sub': user.id})
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error in Google authentication: {str(e)}'
        )

@api_router.get('/auth/me', response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    user_response = UserResponse.model_validate(current_user)
    user_response.is_admin = current_user.role == UserRole.ADMIN
    return user_response

@api_router.post('/auth/2fa/enable')
async def enable_2fa(
    data: TwoFactorEnable,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Enable 2FA for user"""
    # Verify password
    if not verify_password(data.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid password'
        )
    
    # Generate secret
    secret = generate_2fa_secret()
    current_user.two_factor_secret = secret
    current_user.two_factor_enabled = True
    
    await db.commit()
    
    import pyotp
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=current_user.email, issuer_name='GuaraniAppStore')
    
    return {
        'secret': secret,
        'qr_code_uri': uri,
        'message': '2FA enabled successfully. Scan the QR code with your authenticator app.'
    }

@api_router.post('/auth/2fa/verify')
async def verify_2fa(
    data: TwoFactorVerify,
    current_user: User = Depends(get_current_user)
):
    """Verify 2FA token"""
    if not current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='2FA not enabled'
        )
    
    if verify_2fa_token(current_user.two_factor_secret, data.token):
        return {'valid': True, 'message': '2FA token is valid'}
    else:
        return {'valid': False, 'message': 'Invalid 2FA token'}

@api_router.post('/auth/password-reset/request')
async def request_password_reset(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset"""
    # Find user
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalar_one_or_none()
    
    # Always return success (don't reveal if email exists)
    if not user:
        return {'message': 'If the email exists, a reset link has been sent'}
    
    # Generate reset token
    token = generate_reset_token()
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    reset_record = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    
    db.add(reset_record)
    await db.commit()
    
    # TODO: Send email with reset link
    logger.info(f'Password reset requested for {data.email}. Token: {token}')
    
    return {'message': 'If the email exists, a reset link has been sent'}

@api_router.post('/auth/password-reset/confirm')
async def confirm_password_reset(
    data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """Confirm password reset"""
    # Find reset record
    result = await db.execute(
        select(PasswordReset).filter(
            PasswordReset.token == data.token,
            PasswordReset.used == False
        )
    )
    reset_record = result.scalar_one_or_none()
    
    if not reset_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid or expired reset token'
        )
    
    # Check expiration
    if reset_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Reset token has expired'
        )
    
    # Update user password
    user_result = await db.execute(select(User).filter(User.id == reset_record.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    user.password_hash = hash_password(data.new_password)
    reset_record.used = True
    
    await db.commit()
    
    return {'message': 'Password reset successfully'}

# ============================================
# SERVICES ROUTES
# ============================================

@api_router.get('/services', response_model=list[ServiceResponse])
async def get_services(db: AsyncSession = Depends(get_db)):
    """Get all services - Works with both PostgreSQL and MongoDB"""
    try:
        # Try PostgreSQL first
        from database import get_db
        result = await db.execute(
            select(Service).order_by(Service.order, Service.name)
        )
        services = result.scalars().all()
        return [ServiceResponse.model_validate(s) for s in services]
        
    except Exception as pg_error:
        # Fallback to MongoDB if PostgreSQL fails
        logger.warning(f'PostgreSQL services query failed, using MongoDB: {str(pg_error)}')
        
        # Get services from MongoDB
        mongo_services = await services_collection.find().sort([('order', 1), ('name', 1)]).to_list(length=100)
        
        # Convert MongoDB documents to ServiceResponse
        response_services = []
        for service in mongo_services:
            service_id = str(service.get('_id', service.get('id', '')))
            # MongoDB services use 'price' field, map to 'price_monthly'
            price = service.get('price', service.get('price_monthly', 0.0))
            status_value = service.get('status', 'active' if service.get('active') else 'coming_soon')
            
            response_services.append(ServiceResponse(
                id=service_id,
                name=service.get('name', ''),
                slug=service.get('slug', ''),
                description=service.get('description', ''),
                short_description=service.get('short_description'),
                price_monthly=float(price),
                price_annual=service.get('price_annual'),
                price_annual_crypto=service.get('price_annual_crypto'),
                price_crypto=service.get('price_crypto'),
                price_monthly_telegram=service.get('price_monthly_telegram'),
                price_annual_telegram=service.get('price_annual_telegram'),
                price_annual_crypto_telegram=service.get('price_annual_crypto_telegram'),
                billing_type=service.get('billing_type', 'subscription'),
                billing_period=service.get('billing_period'),
                no_expiration=service.get('no_expiration', False),
                requires_messaging=service.get('requires_messaging', False),
                platform=service.get('platform'),
                telegram_discount=service.get('telegram_discount'),
                multi_purchase=service.get('multi_purchase', False),
                packs=service.get('packs'),
                included_services=service.get('included_services'),
                currency=service.get('currency', 'PYG'),
                status=status_value,
                icon=service.get('icon'),
                features=service.get('features', []),
                ai_model=service.get('ai_model'),
                category=service.get('category'),
                order=service.get('order', 0),
                created_at=service.get('created_at', datetime.utcnow())
            ))
        
        return response_services

@api_router.get('/services/{slug}', response_model=ServiceResponse)
async def get_service(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get service by slug"""
    result = await db.execute(select(Service).filter(Service.slug == slug))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    return ServiceResponse.model_validate(service)

@api_router.post('/services', response_model=ServiceResponse)
async def create_service(
    service_data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new service (Admin only)"""
    new_service = Service(**service_data.model_dump())
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    
    return ServiceResponse.model_validate(new_service)

# ============================================
# LEADS ROUTES
# ============================================

@api_router.post('/leads', response_model=LeadResponse)
async def create_lead(
    lead_data: LeadCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new lead"""
    new_lead = Lead(**lead_data.model_dump())
    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)
    
    return LeadResponse.model_validate(new_lead)

@api_router.get('/leads', response_model=list[LeadResponse])
async def get_leads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all leads (Admin only)"""
    result = await db.execute(
        select(Lead).order_by(Lead.created_at.desc())
    )
    leads = result.scalars().all()
    return [LeadResponse.model_validate(lead) for lead in leads]

# ============================================
# CHATBOT ROUTES
# ============================================

@api_router.post('/chat', response_model=ChatResponse)
async def chat(
    chat_data: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """Chat with AI agent - Con sistema de memoria persistente (30 días)"""
    from chat_memory_service import chat_memory_service
    
    # Obtener o crear sesión de chat
    session = await chat_memory_service.get_or_create_session(
        agent_name=chat_data.agent_name,
        user_id=chat_data.user_id if hasattr(chat_data, 'user_id') else None,
        visitor_id=chat_data.visitor_id if hasattr(chat_data, 'visitor_id') else None,
        session_metadata={
            'channel': 'web_chat',
            'user_agent': chat_data.user_agent if hasattr(chat_data, 'user_agent') else None
        }
    )
    
    # Obtener historial de la sesión (últimos 50 mensajes)
    conversation_history = await chat_memory_service.get_session_history(
        session_id=session.id,
        limit=50
    )
    
    # Verificar si es el primer mensaje del día
    is_first_today = await chat_memory_service.is_first_message_today(
        agent_name=chat_data.agent_name,
        user_id=chat_data.user_id if hasattr(chat_data, 'user_id') else None,
        visitor_id=chat_data.visitor_id if hasattr(chat_data, 'visitor_id') else None
    )
    
    # Guardar mensaje del usuario
    await chat_memory_service.add_message(
        session_id=session.id,
        role='user',
        content=chat_data.message,
        message_metadata={'channel': 'web_chat'}
    )
    
    # Get AI response con contexto mejorado
    ai_response = await chat_with_claude(
        message=chat_data.message,
        agent_name=chat_data.agent_name,
        conversation_history=conversation_history,
        is_first_message_today=is_first_today
    )
    
    # Guardar respuesta del agente
    await chat_memory_service.add_message(
        session_id=session.id,
        role='assistant',
        content=ai_response,
        model_used='claude-3.5-sonnet',
        message_metadata={'channel': 'web_chat'}
    )
    
    return ChatResponse(
        response=ai_response,
        agent_name=chat_data.agent_name,
        conversation_id=session.id,
        timestamp=now
    )

@api_router.get('/conversations/{conversation_id}', response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get conversation by ID"""
    result = await db.execute(
        select(Conversation).filter(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conversation not found'
        )
    
    return ConversationResponse.model_validate(conversation)

# ============================================
# BLOG ROUTES
# ============================================

@api_router.get('/blog/posts', response_model=list[BlogPostResponse])
async def get_blog_posts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get published blog posts (público)"""
    result = await db.execute(
        select(BlogPost)
        .filter(BlogPost.published == True)
        .order_by(BlogPost.published_at.desc())
        .limit(limit)
        .offset(skip)
    )
    posts = result.scalars().all()
    return [BlogPostResponse.model_validate(post) for post in posts]


# ============================================
# BLOG ADMIN ROUTES (Generación bajo demanda)
# ============================================

@api_router.get('/blog/posts/pending', response_model=list[BlogPostResponse])
async def get_pending_articles(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Obtener artículos en cola de aprobación (solo admin)"""
    result = await db.execute(
        select(BlogPost)
        .filter(BlogPost.pending_approval == True)
        .order_by(BlogPost.requested_at.desc())
    )
    posts = result.scalars().all()
    return [BlogPostResponse.model_validate(post) for post in posts]


@api_router.get('/blog/posts/{slug}', response_model=BlogPostResponse)
async def get_blog_post(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get blog post by slug (público, incrementa views)"""
    result = await db.execute(select(BlogPost).filter(BlogPost.slug == slug))
    post = result.scalar_one_or_none()
    
    if not post or not post.published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog post not found'
        )
    
    # Increment views
    post.views += 1
    await db.commit()
    
    return BlogPostResponse.model_validate(post)


# ============================================
# BLOG ADMIN ROUTES (Generación bajo demanda)
# ============================================

@api_router.post('/blog/generate/custom')
async def generate_custom_article(
    request: 'ManualArticleRequest',
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generar artículo personalizado bajo demanda (requiere admin)
    El artículo queda en cola de aprobación
    """
    from blog_generator_service import blog_generator
    from database import SessionLocal
    
    # Usar SessionLocal para operación síncrona
    sync_db = SessionLocal()
    
    try:
        blog_post = await blog_generator.generate_custom_article(
            search_query=request.search_query,
            target_keywords=request.target_keywords or [],
            agent_id=request.agent_id,
            tone=request.tone,
            length=request.length,
            include_faq=request.include_faq,
            db=sync_db
        )
        
        if blog_post:
            return {
                "success": True,
                "article_id": blog_post.id,
                "status": "pending_approval",
                "message": "Artículo generado. En cola de aprobación."
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generando artículo"
            )
    except Exception as e:
        logger.error(f"Error en generate_custom_article: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        sync_db.close()


@api_router.get('/blog/posts/{post_id}/preview', response_model=BlogPostResponse)
async def get_article_preview(
    post_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Preview de artículo SIN incrementar vistas (solo admin)"""
    result = await db.execute(select(BlogPost).filter(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog post not found'
        )
    
    return BlogPostResponse.model_validate(post)


@api_router.put('/blog/posts/{post_id}/approve')
async def approve_article(
    post_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Aprobar y publicar artículo (solo admin)"""
    result = await db.execute(
        select(BlogPost).filter(
            BlogPost.id == post_id,
            BlogPost.pending_approval == True
        )
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog post not found or not pending approval'
        )
    
    # Aprobar y publicar
    post.published = True
    post.pending_approval = False
    post.published_at = datetime.now(timezone.utc)
    post.approved_by = current_user.email
    post.approved_at = datetime.now(timezone.utc)
    
    await db.commit()
    await db.refresh(post)
    
    return {
        "success": True,
        "message": "Artículo aprobado y publicado",
        "article": BlogPostResponse.model_validate(post)
    }


@api_router.put('/blog/posts/{post_id}/reject')
async def reject_article(
    post_id: str,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Rechazar y eliminar artículo (solo admin)"""
    result = await db.execute(
        select(BlogPost).filter(
            BlogPost.id == post_id,
            BlogPost.pending_approval == True
        )
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog post not found or not pending approval'
        )
    
    # Eliminar artículo
    await db.delete(post)
    await db.commit()
    
    return {
        "success": True,
        "message": f"Artículo rechazado y eliminado. Razón: {reason or 'No especificada'}"
    }


@api_router.get('/blog/stats', response_model=BlogStatsResponse)
async def get_blog_stats(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Estadísticas del blog (solo admin)"""
    from sqlalchemy import func
    
    # Total posts
    total_result = await db.execute(select(func.count(BlogPost.id)))
    total_posts = total_result.scalar() or 0
    
    # Published posts
    published_result = await db.execute(
        select(func.count(BlogPost.id)).filter(BlogPost.published == True)
    )
    published_posts = published_result.scalar() or 0
    
    # Draft/pending posts
    draft_result = await db.execute(
        select(func.count(BlogPost.id)).filter(BlogPost.pending_approval == True)
    )
    draft_posts = draft_result.scalar() or 0
    
    # Total views
    views_result = await db.execute(select(func.sum(BlogPost.views)))
    total_views = views_result.scalar() or 0
    
    # Avg views per post
    avg_views = total_views / published_posts if published_posts > 0 else 0
    
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
        "total_views": total_views,
        "avg_views_per_post": round(avg_views, 2)
    }



# ============================================
# PAYMENT & CHECKOUT ROUTES
# ============================================

@api_router.post('/checkout/create-order', response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new order for checkout"""
    
    # Get service
    result = await db.execute(select(Service).filter(Service.id == order_data.service_id))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    # Determine base price
    if order_data.plan_type == 'monthly':
        base_price = service.price_monthly
    elif order_data.plan_type == 'annual':
        base_price = service.price_annual
    elif order_data.plan_type == 'one_time':
        base_price = service.price_monthly  # For one-time payments
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid plan type'
        )
    
    if base_price == 0 and order_data.plan_type != 'one_time':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This service does not support this plan type'
        )
    
    # Calculate final price with discounts
    final_price, discount_percentage = calculate_price_with_discount(
        base_price,
        order_data.platform,
        order_data.payment_method
    )
    
    # Generate order number
    order_number = generate_order_number()
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        service_id=service.id,
        order_number=order_number,
        plan_type=order_data.plan_type,
        platform=order_data.platform,
        base_price=base_price,
        discount_percentage=discount_percentage,
        final_price=final_price,
        payment_method=order_data.payment_method
    )
    
    # Process payment based on method
    if order_data.payment_method == 'pagopar':
        payment_result = await create_pagopar_payment(
            order_id=new_order.id,
            amount=final_price,
            description=f'{service.name} - {order_data.plan_type}',
            user_email=current_user.email
        )
        
        if payment_result['success']:
            new_order.payment_id = payment_result['payment_id']
            new_order.payment_url = payment_result['payment_url']
            new_order.payment_expires_at = payment_result['expires_at']
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=payment_result.get('error', 'Payment creation failed')
            )
    
    elif order_data.payment_method in ['btc', 'eth', 'usdt']:
        # Crypto payment
        wallet = get_crypto_wallet(order_data.payment_method)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Crypto wallet not configured'
            )
        
        crypto_amount = convert_pyg_to_crypto(final_price, order_data.payment_method)
        
        new_order.crypto_address = wallet
        new_order.crypto_amount = str(crypto_amount)
        new_order.payment_expires_at = datetime.utcnow() + timedelta(hours=2)
    
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    
    return OrderResponse.model_validate(new_order)

@api_router.get('/orders/my-orders', response_model=list[OrderResponse])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's orders"""
    result = await db.execute(
        select(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    return [OrderResponse.model_validate(order) for order in orders]

@api_router.get('/orders/{order_id}', response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get order by ID"""
    result = await db.execute(
        select(Order).filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )
    
    return OrderResponse.model_validate(order)

@api_router.post('/payments/crypto/verify')
async def verify_crypto_transaction(
    payment_data: CryptoPaymentVerify,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify crypto payment transaction"""
    
    # Get order
    result = await db.execute(
        select(Order).filter(
            Order.id == payment_data.order_id,
            Order.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )
    
    if order.payment_status == 'completed':
        return {
            'success': True,
            'message': 'Payment already verified',
            'status': 'completed'
        }
    
    # Verify transaction
    verification = await verify_crypto_payment(
        payment_method=order.payment_method,
        tx_hash=payment_data.tx_hash,
        expected_amount=float(order.crypto_amount),
        wallet_address=order.crypto_address
    )
    
    if verification['verified']:
        # Update order
        order.payment_status = 'completed'
        order.crypto_tx_hash = payment_data.tx_hash
        order.completed_at = datetime.utcnow()
        
        # Create transaction record
        transaction = Transaction(
            order_id=order.id,
            transaction_type='payment',
            amount=order.final_price,
            currency=order.currency,
            status='completed',
            gateway='crypto',
            gateway_transaction_id=payment_data.tx_hash,
            gateway_response=verification
        )
        
        db.add(transaction)
        await db.commit()
        
        return {
            'success': True,
            'message': 'Payment verified successfully',
            'status': 'completed'
        }
    else:
        return {
            'success': False,
            'message': verification.get('message', 'Payment verification failed'),
            'status': 'pending'
        }

@api_router.post('/payments/pagopar/webhook')
async def pagopar_webhook(
    webhook_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """Webhook for Pagopar payment notifications"""
    
    # Get order by external reference
    external_ref = webhook_data.get('external_reference')
    if not external_ref:
        return {'status': 'error', 'message': 'Missing external reference'}
    
    result = await db.execute(
        select(Order).filter(Order.id == external_ref)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        return {'status': 'error', 'message': 'Order not found'}
    
    # Update order status based on webhook
    payment_status = webhook_data.get('status')
    
    if payment_status == 'approved':
        order.payment_status = 'completed'
        order.completed_at = datetime.utcnow()
        
        # Create transaction
        transaction = Transaction(
            order_id=order.id,
            transaction_type='payment',
            amount=order.final_price,
            currency=order.currency,
            status='completed',
            gateway='pagopar',
            gateway_transaction_id=webhook_data.get('id'),
            gateway_response=webhook_data
        )
        db.add(transaction)
    
    elif payment_status in ['rejected', 'cancelled']:
        order.payment_status = 'failed'
    
    await db.commit()
    
    return {'status': 'success'}


# ============================================
# USER DASHBOARD ROUTES
# ============================================

@api_router.get('/user/dashboard/stats')
async def get_user_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics for current user"""
    
    # Total orders
    orders_result = await db.execute(
        select(Order).filter(Order.user_id == current_user.id)
    )
    all_orders = orders_result.scalars().all()
    total_orders = len(all_orders)
    
    # Orders by status
    completed_orders = len([o for o in all_orders if o.payment_status == 'completed'])
    pending_orders = len([o for o in all_orders if o.payment_status == 'pending'])
    
    # Total spent
    total_spent = sum([o.final_price for o in all_orders if o.payment_status == 'completed'])
    
    # Active subscriptions (completed orders)
    active_subscriptions = completed_orders
    
    # Recent orders (last 5)
    recent_orders = sorted(all_orders, key=lambda x: x.created_at, reverse=True)[:5]
    
    return {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'active_subscriptions': active_subscriptions,
        'total_spent': total_spent,
        'recent_orders': [OrderResponse.model_validate(o) for o in recent_orders]
    }


@api_router.get('/user/subscriptions')
async def get_user_subscriptions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get active subscriptions for current user"""
    
    try:
        # Try PostgreSQL first
        # Get completed orders (active subscriptions)
        orders_result = await db.execute(
            select(Order).filter(
                Order.user_id == current_user.id,
                Order.payment_status == 'completed'
            ).options(selectinload(Order.service))
        )
        orders = orders_result.scalars().all()
        
        # Transform orders to subscription format
        subscriptions = []
        for order in orders:
            if order.service:
                # Calculate expiration date based on plan type
                expires_at = None
                if order.completed_at:
                    if order.plan_type == 'monthly':
                        from datetime import timedelta
                        expires_at = order.completed_at + timedelta(days=30)
                    elif order.plan_type == 'annual':
                        from datetime import timedelta
                        expires_at = order.completed_at + timedelta(days=365)
                
                subscriptions.append({
                    'id': order.id,
                    'name': order.service.name,
                    'slug': order.service.slug,
                    'short_description': order.service.short_description,
                    'plan_type': order.plan_type,
                    'platform': order.platform,
                    'subscribed_at': order.completed_at.isoformat() if order.completed_at else None,
                    'expires_at': expires_at.isoformat() if expires_at else None,
                    'is_active': True
                })
        
        return subscriptions
        
    except Exception as e:
        # MongoDB fallback - return empty subscriptions for now
        logger.warning(f"PostgreSQL not available for subscriptions, using MongoDB fallback: {str(e)}")
        
        # In MongoDB mode, we don't have orders/subscriptions yet, so return empty list
        # This is expected behavior when PostgreSQL is not available
        return []

@api_router.get('/user/transactions')
async def get_user_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's transactions"""
    result = await db.execute(
        select(Transaction)
        .join(Order, Transaction.order_id == Order.id)
        .filter(Order.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
    )
    transactions = result.scalars().all()
    
    return [{
        'id': str(t.id),
        'order_id': str(t.order_id),
        'amount': t.amount,
        'currency': t.currency,
        'payment_method': t.payment_method if hasattr(t, 'payment_method') else 'N/A',
        'gateway': t.gateway,
        'status': t.status,
        'created_at': t.created_at.isoformat() if t.created_at else None
    } for t in transactions]

@api_router.put('/user/profile')
async def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile"""
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    # Update allowed fields
    if 'full_name' in profile_data:
        user.full_name = profile_data['full_name']
    if 'phone' in profile_data:
        user.phone = profile_data['phone']
    if 'company' in profile_data:
        user.company = profile_data['company']
    if 'country' in profile_data:
        user.country = profile_data['country']
    if 'timezone' in profile_data:
        user.timezone = profile_data['timezone']
    
    await db.commit()
    await db.refresh(user)
    
    return {'message': 'Profile updated successfully', 'user': UserResponse.model_validate(user)}

@api_router.delete('/user/account')
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar cuenta de usuario permanentemente
    ADVERTENCIA: Esta acción es irreversible
    """
    try:
        # Eliminar usuario y todas sus relaciones (cascade en DB)
        await db.delete(current_user)
        await db.commit()
        
        logger.info(f"Cuenta eliminada: {current_user.email}")
        
        return {
            "success": True,
            "message": "Cuenta eliminada exitosamente"
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error eliminando cuenta {current_user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la cuenta"
        )


@api_router.post('/subscription/cancel')
async def cancel_subscription(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancelar suscripción activa
    El usuario podrá seguir usando el servicio hasta el final del período actual
    """
    subscription_id = data.get('subscription_id')
    order_id = data.get('order_id')
    
    if not subscription_id or not order_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="subscription_id y order_id son requeridos"
        )
    
    try:
        # Buscar la orden para verificar que pertenece al usuario
        result = await db.execute(
            select(Order).filter(
                Order.id == order_id,
                Order.user_id == current_user.id
            )
        )
        order = result.scalar_one_or_none()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden no encontrada"
            )
        
        # Marcar como cancelada
        order.status = 'cancelled'
        order.updated_at = datetime.now(timezone.utc)
        
        # Buscar transacción asociada y marcar como cancelada
        tx_result = await db.execute(
            select(Payment).filter(
                Payment.order_id == order_id,
                Payment.status == 'completed'
            )
        )
        tx = tx_result.scalar_one_or_none()
        
        if tx:
            # No cambiar el status a cancelled si ya está completed
            # Solo agregar metadata de cancelación
            tx.updated_at = datetime.now(timezone.utc)
        
        await db.commit()
        
        logger.info(f"Suscripción cancelada: {subscription_id} por usuario {current_user.email}")
        
        return {
            "success": True,
            "message": "Suscripción cancelada exitosamente",
            "subscription_id": subscription_id,
            "order_id": order_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error cancelando suscripción {subscription_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cancelar la suscripción"
        )


@api_router.post('/user/2fa/enable')
async def enable_2fa_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Enable 2FA for user"""
    if current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='2FA already enabled'
        )
    
    secret = generate_2fa_secret()
    
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalar_one_or_none()
    user.two_factor_secret = secret
    
    await db.commit()
    
    # Generate QR code
    import pyotp
    import qrcode
    from io import BytesIO
    import base64
    
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user.email,
        issuer_name='GuaraniAppStore'
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        'secret': secret,
        'qr_code': f'data:image/png;base64,{qr_code}',
        'provisioning_uri': provisioning_uri
    }

@api_router.post('/user/2fa/verify-enable')
async def verify_enable_2fa(
    verify_data: TwoFactorVerify,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify and complete 2FA enable"""
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalar_one_or_none()
    
    if not user.two_factor_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='2FA setup not started'
        )
    
    if not verify_2fa_token(user.two_factor_secret, verify_data.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid 2FA code'
        )
    
    user.two_factor_enabled = True
    await db.commit()
    
    return {'message': '2FA enabled successfully'}

@api_router.post('/user/2fa/disable')
async def disable_2fa_user(
    verify_data: TwoFactorVerify,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Disable 2FA for user"""
    if not current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='2FA not enabled'
        )
    
    if not verify_2fa_token(current_user.two_factor_secret, verify_data.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid 2FA code'
        )
    
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalar_one_or_none()
    user.two_factor_enabled = False
    user.two_factor_secret = None
    
    await db.commit()
    
    return {'message': '2FA disabled successfully'}

# ============================================
# ADMIN ROUTES
# ============================================

@api_router.get('/admin/stats')
async def get_admin_stats(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get admin dashboard statistics"""
    
    try:
        # Try PostgreSQL first
        # Total users
        users_result = await db.execute(select(User))
        all_users = users_result.scalars().all()
        total_users = len(all_users)
        
        # Total orders
        orders_result = await db.execute(select(Order))
        all_orders = orders_result.scalars().all()
        total_orders = len(all_orders)
        
        # Orders by status
        completed_orders = len([o for o in all_orders if o.payment_status == 'completed'])
        pending_orders = len([o for o in all_orders if o.payment_status == 'pending'])
        failed_orders = len([o for o in all_orders if o.payment_status == 'failed'])
        
        # Total revenue (completed orders)
        total_revenue = sum([o.final_price for o in all_orders if o.payment_status == 'completed'])
        
        # Revenue by payment method
        revenue_by_method = {}
        for order in all_orders:
            if order.payment_status == 'completed':
                method = order.payment_method
                if method not in revenue_by_method:
                    revenue_by_method[method] = 0
                revenue_by_method[method] += order.final_price
        
        # Total services
        services_result = await db.execute(select(Service))
        total_services = len(services_result.scalars().all())
        
        return {
            'users': {
                'total': total_users,
                'verified': len([u for u in all_users if u.is_verified]),
                'with_2fa': len([u for u in all_users if u.two_factor_enabled])
            },
            'orders': {
                'total': total_orders,
                'completed': completed_orders,
                'pending': pending_orders,
                'failed': failed_orders
            },
            'revenue': {
                'total': total_revenue,
                'by_method': revenue_by_method
            },
            'services': {
                'total': total_services
            }
        }
        
    except Exception as e:
        # MongoDB fallback
        logger.warning(f"PostgreSQL not available for admin stats, using MongoDB fallback: {str(e)}")
        
        # Get users from MongoDB
        mongo_users = await users_collection.find().to_list(length=1000)
        total_users = len(mongo_users)
        verified_users = len([u for u in mongo_users if u.get('is_verified', False)])
        users_with_2fa = len([u for u in mongo_users if u.get('two_factor_enabled', False)])
        
        # Get services from MongoDB
        mongo_services = await services_collection.find().to_list(length=100)
        total_services = len(mongo_services)
        
        # Orders and revenue are 0 in MongoDB-only mode (no orders collection yet)
        return {
            'users': {
                'total': total_users,
                'verified': verified_users,
                'with_2fa': users_with_2fa
            },
            'orders': {
                'total': 0,
                'completed': 0,
                'pending': 0,
                'failed': 0
            },
            'revenue': {
                'total': 0.0,
                'by_method': {}
            },
            'services': {
                'total': total_services
            }
        }

@api_router.get('/admin/users')
async def get_all_users(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all users (Admin only)"""
    try:
        # Try PostgreSQL first
        result = await db.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().all()
        return [UserResponse.model_validate(user) for user in users]
        
    except Exception as e:
        # MongoDB fallback
        logger.warning(f"PostgreSQL not available for admin users, using MongoDB fallback: {str(e)}")
        
        # Get users from MongoDB with pagination
        mongo_users = await users_collection.find().skip(skip).limit(limit).to_list(length=limit)
        
        # Convert MongoDB users to UserResponse format
        user_responses = []
        for user_data in mongo_users:
            user_id = str(user_data.get('_id', user_data.get('id', '')))
            
            user_response = UserResponse(
                id=user_id,
                email=user_data.get('email', ''),
                full_name=user_data.get('name', user_data.get('full_name', 'User')),
                role=UserRole.ADMIN if user_data.get('is_admin') else UserRole.USER,
                is_active=user_data.get('is_active', True),
                is_verified=user_data.get('is_verified', True),
                two_factor_enabled=user_data.get('two_factor_enabled', False),
                phone=user_data.get('phone'),
                company=user_data.get('company'),
                country=user_data.get('country', 'Paraguay'),
                timezone=user_data.get('timezone', 'America/Asuncion'),
                profile_picture=user_data.get('profile_picture'),
                google_id=user_data.get('google_id'),
                created_at=user_data.get('created_at', datetime.utcnow()),
                last_login=user_data.get('last_login')
            )
            user_responses.append(user_response)
        
        return user_responses

@api_router.put('/admin/users/{user_id}/role')
async def update_user_role(
    user_id: str,
    role_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user role (Admin only)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    new_role = role_data.get('role')
    if new_role not in ['admin', 'user', 'guest']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid role'
        )
    
    user.role = UserRole(new_role)
    await db.commit()
    
    return {'message': 'Role updated successfully', 'user': UserResponse.model_validate(user)}

@api_router.put('/admin/users/{user_id}/status')
async def update_user_status(
    user_id: str,
    status_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user status (Admin only)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    if 'is_active' in status_data:
        user.is_active = status_data['is_active']
    
    if 'is_verified' in status_data:
        user.is_verified = status_data['is_verified']
    
    await db.commit()
    
    return {'message': 'Status updated successfully', 'user': UserResponse.model_validate(user)}

@api_router.get('/admin/orders')
async def get_all_orders_admin(
    skip: int = 0,
    limit: int = 50,
    payment_status: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders (Admin only)"""
    query = select(Order).order_by(Order.created_at.desc())
    
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)
    
    result = await db.execute(query.offset(skip).limit(limit))
    orders = result.scalars().all()
    
    return [OrderResponse.model_validate(order) for order in orders]

@api_router.put('/admin/orders/{order_id}/status')
async def update_order_status_admin(
    order_id: str,
    status_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update order status manually (Admin only)"""
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )
    
    new_status = status_data.get('status')
    if new_status not in ['pending', 'completed', 'failed', 'expired']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid status'
        )
    
    order.payment_status = new_status
    
    if new_status == 'completed' and not order.completed_at:
        order.completed_at = datetime.utcnow()
    
    await db.commit()


# ============================================
# SERVICE EXECUTION ROUTES
# ============================================

@api_router.post('/services/{service_slug}/initialize')
async def initialize_service(
    service_slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Initialize a service for the current user"""
    # Get service by slug
    result = await db.execute(select(Service).filter(Service.slug == service_slug))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    # Map service to implementation
    service_mapping = {
        'suite-cripto': 'CryptoSuiteService',
        'asistente-directivos': 'AsistenteDirectivosService',
        'preseleccion-curricular': 'PreseleccionCurricularService',
        'organizador-facturas': 'OrganizadorFacturasService',
        'organizador-agenda': 'OrganizadorAgendaService',
        'consultoria-tecnica': 'ConsultoriaTecnicaService',
        'generador-blogs': 'GeneradorBlogsService',
        'ecommerce-automation': 'EcommerceAutomationService',
        'redes-sociales': 'RedesSocialesService',
        'prospeccion-comercial': 'ProspeccionComercialService',
        'agente-ventas-ia': 'AgenteVentasIAService'
    }
    
    service_class_name = service_mapping.get(service_slug)
    
    if not service_class_name:
        return {
            'success': False,
            'error': 'Service implementation not available yet',
            'status': 'coming_soon'
        }
    
    # Dynamically import and instantiate service
    try:
        from services import (
            CryptoSuiteService, AsistenteDirectivosService,
            PreseleccionCurricularService, OrganizadorFacturasService,
            OrganizadorAgendaService, ConsultoriaTecnicaService,
            GeneradorBlogsService, EcommerceAutomationService,
            RedesSocialesService, ProspeccionComercialService,
            AgenteVentasIAService
        )
        
        service_classes = {
            'CryptoSuiteService': CryptoSuiteService,
            'AsistenteDirectivosService': AsistenteDirectivosService,
            'PreseleccionCurricularService': PreseleccionCurricularService,
            'OrganizadorFacturasService': OrganizadorFacturasService,
            'OrganizadorAgendaService': OrganizadorAgendaService,
            'ConsultoriaTecnicaService': ConsultoriaTecnicaService,
            'GeneradorBlogsService': GeneradorBlogsService,
            'EcommerceAutomationService': EcommerceAutomationService,
            'RedesSocialesService': RedesSocialesService,
            'ProspeccionComercialService': ProspeccionComercialService,
            'AgenteVentasIAService': AgenteVentasIAService
        }
        
        ServiceClass = service_classes[service_class_name]
        service_instance = ServiceClass(
            user_id=str(current_user.id),
            service_id=str(service.id),
            db=db
        )
        
        result = await service_instance.initialize()
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Service initialization failed: {str(e)}'
        }

@api_router.post('/services/{service_slug}/execute')
async def execute_service_action(
    service_slug: str,
    action_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Execute a service action"""
    result = await db.execute(select(Service).filter(Service.slug == service_slug))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    action = action_data.get('action')
    params = action_data.get('params', {})
    
    service_mapping = {
        'suite-cripto': 'CryptoSuiteService',
        'asistente-directivos': 'AsistenteDirectivosService',
        'preseleccion-curricular': 'PreseleccionCurricularService',
        'organizador-facturas': 'OrganizadorFacturasService',
        'organizador-agenda': 'OrganizadorAgendaService',
        'consultoria-tecnica': 'ConsultoriaTecnicaService',
        'generador-blogs': 'GeneradorBlogsService',
        'ecommerce-automation': 'EcommerceAutomationService',
        'redes-sociales': 'RedesSocialesService',
        'prospeccion-comercial': 'ProspeccionComercialService',
        'agente-ventas-ia': 'AgenteVentasIAService'
    }
    
    service_class_name = service_mapping.get(service_slug)
    
    if not service_class_name:
        return {'success': False, 'error': 'Service not available'}
    
    try:
        from services import (
            CryptoSuiteService, AsistenteDirectivosService,
            PreseleccionCurricularService, OrganizadorFacturasService,
            OrganizadorAgendaService, ConsultoriaTecnicaService,
            GeneradorBlogsService, EcommerceAutomationService,
            RedesSocialesService, ProspeccionComercialService,
            AgenteVentasIAService
        )
        
        service_classes = {
            'CryptoSuiteService': CryptoSuiteService,
            'AsistenteDirectivosService': AsistenteDirectivosService,
            'PreseleccionCurricularService': PreseleccionCurricularService,
            'OrganizadorFacturasService': OrganizadorFacturasService,
            'OrganizadorAgendaService': OrganizadorAgendaService,
            'ConsultoriaTecnicaService': ConsultoriaTecnicaService,
            'GeneradorBlogsService': GeneradorBlogsService,
            'EcommerceAutomationService': EcommerceAutomationService,
            'RedesSocialesService': RedesSocialesService,
            'ProspeccionComercialService': ProspeccionComercialService,
            'AgenteVentasIAService': AgenteVentasIAService
        }
        
        ServiceClass = service_classes[service_class_name]
        service_instance = ServiceClass(
            user_id=str(current_user.id),
            service_id=str(service.id),
            db=db
        )
        
        result = await service_instance.execute(action, params)
        return result
        
    except Exception as e:
        return {'success': False, 'error': f'Execution failed: {str(e)}'}

@api_router.get('/services/{service_slug}/status')
async def get_service_status(
    service_slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get service status for current user"""
    result = await db.execute(select(Service).filter(Service.slug == service_slug))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    service_mapping = {
        'suite-cripto': 'CryptoSuiteService',
        'asistente-directivos': 'AsistenteDirectivosService',
        'preseleccion-curricular': 'PreseleccionCurricularService',
        'organizador-facturas': 'OrganizadorFacturasService',
        'organizador-agenda': 'OrganizadorAgendaService',
        'consultoria-tecnica': 'ConsultoriaTecnicaService',
        'generador-blogs': 'GeneradorBlogsService',
        'ecommerce-automation': 'EcommerceAutomationService',
        'redes-sociales': 'RedesSocialesService',
        'prospeccion-comercial': 'ProspeccionComercialService',
        'agente-ventas-ia': 'AgenteVentasIAService'
    }
    
    service_class_name = service_mapping.get(service_slug)
    
    if not service_class_name:
        return {'success': False, 'error': 'Service not available', 'status': 'coming_soon'}
    
    try:
        from services import (
            CryptoSuiteService, AsistenteDirectivosService,
            PreseleccionCurricularService, OrganizadorFacturasService,
            OrganizadorAgendaService, ConsultoriaTecnicaService,
            GeneradorBlogsService, EcommerceAutomationService,
            RedesSocialesService, ProspeccionComercialService,
            AgenteVentasIAService
        )
        
        service_classes = {
            'CryptoSuiteService': CryptoSuiteService,
            'AsistenteDirectivosService': AsistenteDirectivosService,
            'PreseleccionCurricularService': PreseleccionCurricularService,
            'OrganizadorFacturasService': OrganizadorFacturasService,
            'OrganizadorAgendaService': OrganizadorAgendaService,
            'ConsultoriaTecnicaService': ConsultoriaTecnicaService,
            'GeneradorBlogsService': GeneradorBlogsService,
            'EcommerceAutomationService': EcommerceAutomationService,
            'RedesSocialesService': RedesSocialesService,
            'ProspeccionComercialService': ProspeccionComercialService,
            'AgenteVentasIAService': AgenteVentasIAService
        }
        
        ServiceClass = service_classes[service_class_name]
        service_instance = ServiceClass(
            user_id=str(current_user.id),
            service_id=str(service.id),
            db=db
        )
        
        result = await service_instance.get_status()
        return result
        
    except Exception as e:
        return {'success': False, 'error': f'Status check failed: {str(e)}'}

    
    return {'message': 'Order status updated successfully', 'order': OrderResponse.model_validate(order)}

@api_router.get('/admin/services/manage')
async def get_services_admin(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all services for admin management"""
    result = await db.execute(select(Service).order_by(Service.order))
    services = result.scalars().all()
    return [ServiceResponse.model_validate(s) for s in services]

@api_router.put('/admin/services/{service_id}')
async def update_service_admin(
    service_id: str,
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update service (Admin only)"""
    result = await db.execute(select(Service).filter(Service.id == service_id))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    # Update fields
    for field, value in service_data.model_dump().items():
        setattr(service, field, value)
    
    await db.commit()
    await db.refresh(service)
    
    return {'message': 'Service updated successfully', 'service': ServiceResponse.model_validate(service)}


@api_router.post('/admin/services')
async def create_service_admin(
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new service (Admin only)"""
    new_service = Service(**service_data.model_dump())
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    
    return {'message': 'Service created successfully', 'service': ServiceResponse.model_validate(new_service)}

@api_router.delete('/admin/services/{service_id}')
async def delete_service_admin(
    service_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete service (Admin only)"""
    result = await db.execute(select(Service).filter(Service.id == service_id))
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found'
        )
    
    await db.delete(service)
    await db.commit()
    
    return {'message': 'Service deleted successfully'}

@api_router.get('/admin/transactions')
async def get_all_transactions_admin(
    skip: int = 0,
    limit: int = 50,
    payment_method: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all transactions (Admin only)"""
    query = select(Transaction).order_by(Transaction.created_at.desc())
    
    if payment_method:
        query = query.filter(Transaction.payment_method == payment_method)
    
    result = await db.execute(query.offset(skip).limit(limit))
    transactions = result.scalars().all()
    
    return [{
        'id': str(t.id),
        'order_id': str(t.order_id),
        'user_id': str(t.user_id),
        'amount': t.amount,
        'payment_method': t.payment_method,
        'gateway': t.gateway,
        'transaction_id': t.transaction_id,
        'status': t.status,
        'created_at': t.created_at.isoformat() if t.created_at else None
    } for t in transactions]

@api_router.get('/admin/search')
async def admin_search(
    q: str,
    type: str = 'users',  # 'users', 'orders', 'services'
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Search functionality for admin panel"""
    if type == 'users':
        result = await db.execute(
            select(User).filter(
                (User.email.ilike(f'%{q}%')) | (User.full_name.ilike(f'%{q}%'))
            ).limit(20)
        )
        items = result.scalars().all()
        return [UserResponse.model_validate(u) for u in items]
    
    elif type == 'orders':
        result = await db.execute(
            select(Order).filter(Order.id.ilike(f'%{q}%')).limit(20)
        )
        items = result.scalars().all()
        return [OrderResponse.model_validate(o) for o in items]
    
    elif type == 'services':
        result = await db.execute(
            select(Service).filter(
                (Service.title.ilike(f'%{q}%')) | (Service.description.ilike(f'%{q}%'))
            ).limit(20)
        )
        items = result.scalars().all()
        return [ServiceResponse.model_validate(s) for s in items]
    
    return []

@api_router.get('/admin/analytics')
async def get_admin_analytics(
    days: int = 30,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics data for charts"""
    from datetime import timedelta
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Revenue over time
    result = await db.execute(
        select(Order).filter(
            Order.created_at >= start_date,
            Order.payment_status == 'completed'
        ).order_by(Order.created_at)
    )
    orders = result.scalars().all()
    
    # Group by date
    revenue_by_date = {}
    for order in orders:
        date_key = order.created_at.strftime('%Y-%m-%d')
        if date_key not in revenue_by_date:
            revenue_by_date[date_key] = 0
        revenue_by_date[date_key] += order.final_price
    
    # Users growth
    result = await db.execute(
        select(User).filter(User.created_at >= start_date).order_by(User.created_at)
    )
    users = result.scalars().all()
    
    users_by_date = {}
    for user in users:
        date_key = user.created_at.strftime('%Y-%m-%d')
        if date_key not in users_by_date:
            users_by_date[date_key] = 0
        users_by_date[date_key] += 1
    
    # Most popular services
    service_orders = {}
    for order in orders:
        if order.service_id not in service_orders:
            service_orders[order.service_id] = 0
        service_orders[order.service_id] += 1
    
    # Get service details
    popular_services = []
    for service_id, count in sorted(service_orders.items(), key=lambda x: x[1], reverse=True)[:5]:
        result = await db.execute(select(Service).filter(Service.id == service_id))
        service = result.scalar_one_or_none()
        if service:
            popular_services.append({
                'service': service.title,
                'orders': count
            })
    
    return {
        'revenue_by_date': revenue_by_date,
        'users_by_date': users_by_date,
        'popular_services': popular_services
    }



# Payment Gateway Configuration Endpoints
@api_router.get('/admin/payment-gateways', tags=["Admin - Payment Gateways"])
async def get_payment_gateways(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all payment gateway configurations"""
    from sqlalchemy import select
    from models import PaymentGatewayConfig
    
    result = await db.execute(select(PaymentGatewayConfig))
    gateways = result.scalars().all()
    
    return [{
        'id': gw.id,
        'gateway_name': gw.gateway_name,
        'is_enabled': gw.is_enabled,
        'config': gw.config,
        'updated_at': gw.updated_at.isoformat() if gw.updated_at else None
    } for gw in gateways]


@api_router.post('/admin/payment-gateways', tags=["Admin - Payment Gateways"])
async def create_or_update_gateway(
    gateway_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create or update a payment gateway configuration"""
    from sqlalchemy import select
    from models import PaymentGatewayConfig
    
    gateway_name = gateway_data.get('gateway_name')
    
    # Check if exists
    result = await db.execute(
        select(PaymentGatewayConfig).where(PaymentGatewayConfig.gateway_name == gateway_name)
    )
    gateway = result.scalar_one_or_none()
    
    if gateway:
        # Update
        gateway.config = gateway_data.get('config', {})
        gateway.is_enabled = gateway_data.get('is_enabled', False)
        gateway.updated_by = current_user.id
        gateway.updated_at = datetime.utcnow()
    else:
        # Create
        gateway = PaymentGatewayConfig(
            gateway_name=gateway_name,
            config=gateway_data.get('config', {}),
            is_enabled=gateway_data.get('is_enabled', False),
            updated_by=current_user.id
        )
        db.add(gateway)
    
    await db.commit()
    await db.refresh(gateway)
    
    return {
        'success': True,
        'gateway': {
            'id': gateway.id,
            'gateway_name': gateway.gateway_name,
            'is_enabled': gateway.is_enabled,
            'config': gateway.config
        }
    }


@api_router.delete('/admin/payment-gateways/{gateway_id}', tags=["Admin - Payment Gateways"])
async def delete_gateway(
    gateway_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a payment gateway configuration"""
    from sqlalchemy import select
    from models import PaymentGatewayConfig
    
    result = await db.execute(
        select(PaymentGatewayConfig).where(PaymentGatewayConfig.id == gateway_id)
    )
    gateway = result.scalar_one_or_none()
    
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")


# LLM Service Endpoints
@api_router.post('/user/llm/chat', tags=["User - LLM"])
async def llm_chat(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """General chat with LLM"""
    from llm_service import llm_service
    
    message = request.get('message')
    system_message = request.get('system_message', 'You are a helpful AI assistant.')
    session_id = request.get('session_id', f"user_{current_user.id}")
    
    result = await llm_service.chat(message, system_message, session_id)
    return result


@api_router.post('/user/llm/technical-consultation', tags=["User - LLM"])
async def technical_consultation(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Technical consultation"""
    from llm_service import llm_service
    
    question = request.get('question')
    session_id = request.get('session_id', f"tech_{current_user.id}")
    
    result = await llm_service.technical_consultation(question, session_id)
    return result


@api_router.post('/user/llm/generate-blog', tags=["User - LLM"])
async def generate_blog(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Generate blog content"""
    from llm_service import llm_service
    
    topic = request.get('topic')
    keywords = request.get('keywords', '')
    tone = request.get('tone', 'professional')
    length = request.get('length', 'medium')
    
    result = await llm_service.generate_blog(topic, keywords, tone, length)
    return result


@api_router.post('/user/llm/analyze-cv', tags=["User - LLM"])
async def analyze_cv(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Analyze CV/Resume"""
    from llm_service import llm_service
    
    cv_text = request.get('cv_text')
    position = request.get('position', '')
    
    result = await llm_service.analyze_cv(cv_text, position)
    return result


@api_router.post('/user/llm/extract-invoice', tags=["User - LLM"])
async def extract_invoice(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Extract invoice data"""
    from llm_service import llm_service
    
    invoice_text = request.get('invoice_text')
    
    result = await llm_service.extract_invoice_data(invoice_text)
    return result


@api_router.post('/user/llm/social-media-post', tags=["User - LLM"])
async def generate_social_post(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Generate social media post"""
    from llm_service import llm_service
    
    topic = request.get('topic')
    platform = request.get('platform', 'facebook')
    tone = request.get('tone', 'professional')
    
    result = await llm_service.generate_social_media_post(topic, platform, tone)
    return result


@api_router.post('/user/llm/find-leads', tags=["User - LLM"])
async def find_leads(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Generate lead finding strategy"""
    from llm_service import llm_service
    
    industry = request.get('industry')
    location = request.get('location')
    size = request.get('size', '')
    
    result = await llm_service.find_leads(industry, location, size)
    return result

    
    await db.delete(gateway)
    await db.commit()
    
    return {'success': True, 'message': 'Gateway deleted'}

# Telegram Bots Management Endpoints
@api_router.get('/admin/bots/status', tags=["Admin - Bots"])
async def get_bots_status(current_user: User = Depends(get_current_admin_user)):
    """Get status of all Telegram bots"""
    from bot_manager import get_bot_status
    try:
        status = get_bot_status()
        return {
            'success': True,
            'bots': status,
            'total_running': sum(1 for s in status.values() if s['running'])
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'bots': {}
        }


@api_router.post('/admin/bots/start/{bot_name}', tags=["Admin - Bots"])
async def start_telegram_bot(bot_name: str, current_user: User = Depends(get_current_admin_user)):
    """Start a specific Telegram bot"""
    from bot_manager import start_bot
    
    bot_modules = {
        'cryptoshield': 'cryptoshield',
        'pulse': 'pulse',
        'momentum': 'momentum',
        'agente_ventas': 'agente_ventas',
        'asistente': 'asistente'
    }
    
    if bot_name not in bot_modules:
        raise HTTPException(status_code=400, detail="Bot no válido")
    
    try:
        success = start_bot(bot_name.replace('_', ' ').title(), bot_modules[bot_name])
        return {
            'success': success,
            'message': f"Bot {bot_name} iniciado" if success else f"Bot {bot_name} ya está corriendo"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/admin/bots/stop/{bot_name}', tags=["Admin - Bots"])
async def stop_telegram_bot(bot_name: str, current_user: User = Depends(get_current_admin_user)):
    """Stop a specific Telegram bot"""
    from bot_manager import stop_bot
    
    try:
        success = stop_bot(bot_name.replace('_', ' ').title())
        return {
            'success': success,
            'message': f"Bot {bot_name} detenido" if success else f"Bot {bot_name} no está corriendo"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/admin/bots/start-all', tags=["Admin - Bots"])
async def start_all_telegram_bots(current_user: User = Depends(get_current_admin_user)):
    """Start all Telegram bots"""
    from bot_manager import start_all_bots
    
    try:
        start_all_bots()
        return {
            'success': True,
            'message': 'Todos los bots han sido iniciados'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/admin/bots/stop-all', tags=["Admin - Bots"])
async def stop_all_telegram_bots(current_user: User = Depends(get_current_admin_user)):
    """Stop all Telegram bots"""
    from bot_manager import stop_all_bots
    
    try:
        stop_all_bots()
        return {
            'success': True,
            'message': 'Todos los bots han sido detenidos'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# EXTERNAL APIS ENDPOINTS - Google Vision, CoinGecko, Blockchain
# ============================================

from fastapi import File, UploadFile
from pydantic import BaseModel

class OCRRequest(BaseModel):
    language_hint: Optional[str] = "es"

@api_router.post('/ocr/process')
async def process_ocr(
    file: UploadFile = File(...),
    language_hint: str = "es",
    current_user: User = Depends(get_current_user)
):
    """
    Procesar imagen para OCR (facturas, documentos) - Google Cloud Vision
    Requiere autenticación
    """
    try:
        content = await file.read()
        result = await vision_service.detect_text_from_image(content, language_hint)
        
        return {
            **result,
            "filename": file.filename,
            "user_id": current_user.id
        }
    except Exception as e:
        logger.error(f"Error en OCR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/ocr/process-pixtral')
async def process_ocr_pixtral(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Procesar documento con Mistral Pixtral (extracción estructurada)
    Extrae automáticamente: fecha, nombre, RUC, importe, concepto, moneda
    Requiere autenticación
    """
    try:
        content = await file.read()
        
        # Campos por defecto para facturas paraguayas
        custom_fields = {
            'fecha': 'Fecha de emisión',
            'nombre': 'Nombre del proveedor o emisor',
            'ruc': 'RUC del emisor',
            'importe': 'Total a pagar',
            'concepto': 'Descripción o concepto principal',
            'moneda': 'Moneda (PYG, USD, etc.)'
        }
        
        result = await document_processor.process_with_pixtral(
            image_bytes=content,
            custom_fields=custom_fields
        )
        
        return {
            **result,
            "filename": file.filename,
            "user_id": current_user.id
        }
    except Exception as e:
        logger.error(f"Error en Pixtral OCR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/ocr/process-hybrid')
async def process_ocr_hybrid(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Procesar documento con ambos engines (Pixtral + Google Vision)
    Combina extracción estructurada + OCR completo
    Requiere autenticación
    """
    try:
        content = await file.read()
        
        # Campos por defecto
        custom_fields = {
            'fecha': 'Fecha de emisión',
            'nombre': 'Nombre del proveedor',
            'ruc': 'RUC',
            'importe': 'Total',
            'moneda': 'Moneda'
        }
        
        result = await document_processor.process_document_hybrid(
            image_bytes=content,
            custom_fields=custom_fields,
            use_pixtral=True,
            use_google=True
        )
        
        return {
            **result,
            "filename": file.filename,
            "user_id": current_user.id
        }
    except Exception as e:
        logger.error(f"Error en OCR híbrido: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get('/crypto/price/{coin_id}')
async def get_crypto_price(coin_id: str, vs_currency: str = "usd"):
    """
    Obtener precio de criptomoneda
    Ejemplo: /api/crypto/price/bitcoin?vs_currency=usd
    """
    try:
        result = await crypto_service.get_crypto_price(coin_id, vs_currency)
        return result
    except Exception as e:
        logger.error(f"Error obteniendo precio crypto: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get('/crypto/top')
async def get_top_cryptocurrencies(limit: int = 50):
    """
    Obtener top criptomonedas por market cap
    Ejemplo: /api/crypto/top?limit=50
    """
    try:
        result = await crypto_service.get_top_cryptocurrencies(limit)
        return result
    except Exception as e:
        logger.error(f"Error obteniendo top cryptos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get('/blockchain/eth/balance/{address}')
async def get_eth_balance(address: str):
    """
    Obtener balance de ETH de una dirección
    Ejemplo: /api/blockchain/eth/balance/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
    """
    try:
        result = await blockchain_service.get_eth_balance(address)
        return result
    except Exception as e:
        logger.error(f"Error obteniendo balance ETH: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get('/blockchain/verify/{tx_hash}')
async def verify_blockchain_transaction(tx_hash: str, network: str = "ethereum"):
    """
    Verificar transacción blockchain
    Ejemplo: /api/blockchain/verify/0xabc123...?network=ethereum
    """
    try:
        result = await blockchain_service.verify_transaction(tx_hash, network)
        return result
    except Exception as e:
        logger.error(f"Error verificando transacción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get('/google/oauth/authorize')
async def google_oauth_authorize():
    """
    Obtener URL de autorización de Google OAuth
    El usuario debe visitar esta URL para autorizar acceso a Calendar, Sheets, Blogger
    """
    try:
        result = google_oauth_service.get_authorization_url()
        return result
    except Exception as e:
        logger.error(f"Error en Google OAuth: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# TELEGRAM WEBHOOK ENDPOINTS
# ============================================

from fastapi import Request, Header

@api_router.post('/telegram/webhook/setup/{bot_id}')
async def setup_telegram_webhook(
    bot_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Configurar webhook para un bot de Telegram específico
    Solo admins pueden configurar webhooks
    """
    try:
        result = await webhook_manager.setup_webhook(bot_id)
        return result
    except Exception as e:
        logger.error(f"Error configurando webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/telegram/webhook/setup-all')
async def setup_all_telegram_webhooks(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Configurar webhooks para todos los bots de Telegram
    Solo admins pueden configurar webhooks
    """
    try:
        result = await webhook_manager.setup_all_webhooks()
        return result
    except Exception as e:
        logger.error(f"Error configurando webhooks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete('/telegram/webhook/{bot_id}')
async def delete_telegram_webhook(
    bot_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Eliminar webhook de un bot específico
    Solo admins pueden eliminar webhooks
    """
    try:
        result = await webhook_manager.delete_webhook(bot_id)
        return result
    except Exception as e:
        logger.error(f"Error eliminando webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get('/telegram/webhook/info/{bot_id}')
async def get_telegram_webhook_info(
    bot_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtener información del webhook configurado
    Solo admins pueden ver info de webhooks
    """
    try:
        result = await webhook_manager.get_webhook_info(bot_id)
        return result
    except Exception as e:
        logger.error(f"Error obteniendo info webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post('/telegram/webhook/{bot_id}')
async def receive_telegram_webhook(
    bot_id: str,
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None)
):
    """
    Endpoint para recibir updates de Telegram vía webhook
    Este endpoint es llamado por Telegram, no por usuarios
    """
    try:
        # Verificar secret token
        if not webhook_manager.verify_webhook_request(x_telegram_bot_api_secret_token or ''):
            logger.warning(f"⚠️ Intento de webhook no autorizado para bot {bot_id}")
            raise HTTPException(status_code=403, detail="Unauthorized webhook request")
        
        # Obtener update data
        update = await request.json()
        
        # Procesar update
        result = await webhook_manager.process_update(bot_id, update)
        
        # Telegram espera 200 OK
        return {'ok': True}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando webhook de {bot_id}: {str(e)}")
        # Aún así devolver 200 para que Telegram no reintente
        return {'ok': False, 'error': str(e)}



# ========================================
# CHAT MEMORY MANAGEMENT ENDPOINTS
# ========================================

@api_router.post('/admin/chat/cleanup', tags=["Admin - Chat Memory"])
async def cleanup_old_chat_messages(current_user: User = Depends(get_current_admin_user)):
    """
    Limpia mensajes de chat con más de 30 días.
    Debe ejecutarse periódicamente (ej: cron diario).
    """
    from chat_memory_service import chat_memory_service
    
    try:
        deleted_count = await chat_memory_service.cleanup_old_messages()
        inactive_sessions = await chat_memory_service.cleanup_inactive_sessions()
        
        return {
            'success': True,
            'messages_deleted': deleted_count,
            'sessions_deactivated': inactive_sessions,
            'retention_days': 30
        }
    except Exception as e:
        logger.error(f"Error en limpieza de chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en limpieza: {str(e)}"
        )


@api_router.get('/admin/chat/stats', tags=["Admin - Chat Memory"])
async def get_chat_statistics(current_user: User = Depends(get_current_admin_user)):
    """Obtiene estadísticas generales del sistema de chat"""
    from sqlalchemy import func
    from chat_memory_service import ChatSession, ChatMessage
    
    async with AsyncSessionLocal() as db:
        # Total de sesiones
        total_sessions = await db.scalar(select(func.count(ChatSession.id)))
        active_sessions = await db.scalar(
            select(func.count(ChatSession.id)).where(ChatSession.is_active == True)
        )
        
        # Total de mensajes
        total_messages = await db.scalar(select(func.count(ChatMessage.id)))
        
        # Mensajes por agente
        agent_query = select(
            ChatSession.agent_name,
            func.count(ChatMessage.id).label('message_count')
        ).join(
            ChatMessage, ChatSession.id == ChatMessage.session_id
        ).group_by(ChatSession.agent_name)
        
        result = await db.execute(agent_query)
        messages_by_agent = {row.agent_name: row.message_count for row in result}
        
        return {
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'total_messages': total_messages,
            'messages_by_agent': messages_by_agent,
            'retention_days': 30
        }


@api_router.get('/user/chat/history', tags=["User - Chat"])
async def get_user_chat_history(
    agent_name: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """Obtiene el historial de chat del usuario"""
    from chat_memory_service import chat_memory_service
    from sqlalchemy import and_
    
    async with AsyncSessionLocal() as db:
        query = select(ChatSession).where(ChatSession.user_id == current_user.id)
        
        if agent_name:
            query = query.where(ChatSession.agent_name == agent_name)
        
        query = query.order_by(ChatSession.last_interaction_date.desc()).limit(10)
        
        result = await db.execute(query)
        sessions = result.scalars().all()
        
        sessions_data = []
        for session in sessions:
            messages = await chat_memory_service.get_session_history(
                session_id=session.id,
                limit=limit
            )
            
            sessions_data.append({
                'session_id': session.id,
                'agent_name': session.agent_name,
                'first_interaction': session.first_interaction_date.isoformat(),
                'last_interaction': session.last_interaction_date.isoformat(),
                'total_messages': session.total_messages,
                'messages': messages
            })
        


# ========================================
# GOOGLE OAUTH 2.0 ENDPOINTS
# ========================================

@api_router.get('/auth/google/login', tags=["Auth - Google OAuth"])
async def google_oauth_login(redirect_after: Optional[str] = None):
    """
    Inicia el flujo de Google OAuth.
    
    Args:
        redirect_after: URL a la que redirigir después del login (opcional)
    
    Returns:
        Redirección a la página de autorización de Google
    """
    from google_oauth_service import google_oauth_service
    from fastapi.responses import RedirectResponse
    import secrets
    
    # Generar estado CSRF
    state = secrets.token_urlsafe(32)
    
    # Guardar estado y redirect_after en sesión (puedes usar Redis en producción)
    # Por ahora lo incluimos en el state como base64
    if redirect_after:
        import base64
        state_data = f"{state}:{redirect_after}"
        state = base64.urlsafe_b64encode(state_data.encode()).decode()
    
    # Obtener URL de autorización
    authorization_url = google_oauth_service.get_authorization_url(state=state)
    
    return RedirectResponse(url=authorization_url)


@api_router.get('/auth/google/callback', tags=["Auth - Google OAuth"])
async def google_oauth_callback(
    code: str,
    state: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Callback de Google OAuth. Procesa el código y crea/actualiza el usuario.
    """
    from google_oauth_service import google_oauth_service
    from auth import create_access_token
    from fastapi.responses import RedirectResponse
    import base64
    
    try:
        # Decodificar state si tiene redirect_after
        redirect_after = None
        if state:
            try:
                decoded = base64.urlsafe_b64decode(state.encode()).decode()
                if ':' in decoded:
                    _, redirect_after = decoded.split(':', 1)
            except:
                pass
        
        # Procesar callback y obtener tokens
        result = await google_oauth_service.handle_callback(code=code, state=state)
        user_info = result['user_info']
        credentials = result['credentials']
        
        # Buscar o crear usuario
        email = user_info.get('email')
        google_id = user_info.get('id')
        
        result = await db.execute(
            select(User).where(
                (User.email == email) | (User.google_id == google_id)
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Crear nuevo usuario
            user = User(
                email=email,
                google_id=google_id,
                full_name=user_info.get('name', email.split('@')[0]),
                profile_picture=user_info.get('picture'),
                is_verified=True,
                password_hash=None  # Sin password para OAuth
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"Nuevo usuario creado vía Google OAuth: {email}")
        else:
            # Actualizar información del usuario
            if not user.google_id:
                user.google_id = google_id
            user.profile_picture = user_info.get('picture')
            user.is_verified = True
            user.last_login = datetime.now(timezone.utc)
            await db.commit()
            
            logger.info(f"Usuario existente autenticado vía Google OAuth: {email}")
        
        # Guardar tokens de OAuth
        await google_oauth_service.save_user_tokens(
            user_id=user.id,
            credentials=credentials
        )
        
        # Generar JWT token para nuestra aplicación
        access_token = create_access_token(data={'sub': user.email})
        
        # Redirigir al frontend con el token
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        redirect_url = redirect_after or f"{frontend_url}/dashboard"
        
        return RedirectResponse(
            url=f"{redirect_url}?token={access_token}&oauth=google"
        )
    
    except Exception as e:
        logger.error(f"Error en Google OAuth callback: {str(e)}")
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        return RedirectResponse(
            url=f"{frontend_url}/?error=oauth_failed&message={str(e)}"
        )


@api_router.post('/auth/google/revoke', tags=["Auth - Google OAuth"])
async def revoke_google_oauth(current_user: User = Depends(get_current_user)):
    """Revoca los permisos de Google OAuth del usuario"""
    from google_oauth_service import google_oauth_service
    
    success = await google_oauth_service.revoke_user_tokens(user_id=current_user.id)
    
    if success:
        return {
            'success': True,
            'message': 'Permisos de Google OAuth revocados exitosamente'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No se encontraron tokens de Google OAuth'
        )


@api_router.get('/user/google/status', tags=["User - Google OAuth"])
async def get_google_oauth_status(current_user: User = Depends(get_current_user)):
    """Verifica si el usuario tiene Google OAuth configurado"""
    from google_oauth_service import GoogleOAuthToken
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(GoogleOAuthToken).where(GoogleOAuthToken.user_id == current_user.id)
        )
        token = result.scalar_one_or_none()
        
        return {
            'has_google_oauth': token is not None,
            'scopes': token.scopes if token else [],
            'expires_at': token.expires_at.isoformat() if token else None
        }

        return {
            'success': True,
            'sessions': sessions_data
        }


# ============================================
# PULSE IA ENDPOINTS
# ============================================
try:
    from pulse_api import router as pulse_router
    app.include_router(pulse_router)
    logger.info("✅ Pulse IA endpoints loaded")
except Exception as e:
    logger.warning(f"⚠️ Pulse IA endpoints not loaded: {e}")


# ============================================
# MOMENTUM PREDICTOR IA ENDPOINTS
# ============================================
try:
    from momentum_api import router as momentum_router
    app.include_router(momentum_router)
    logger.info("✅ Momentum Predictor IA endpoints loaded")
except Exception as e:
    logger.warning(f"⚠️ Momentum Predictor IA endpoints not loaded: {e}")


# ============================================
# CRYPTOSHIELD IA ENDPOINTS
# ============================================
try:
    from cryptoshield_api import router as cryptoshield_router
    app.include_router(cryptoshield_router)
    logger.info("✅ CryptoShield IA endpoints loaded")
except Exception as e:
    logger.warning(f"⚠️ CryptoShield IA endpoints not loaded: {e}")


# ============================================
# SUITE CRYPTO IA UNIFIED ENDPOINTS
# ============================================
try:
    from suite_crypto_api import router as suite_crypto_router
    app.include_router(suite_crypto_router)
    logger.info("✅ Suite Crypto IA unified endpoints loaded")
except Exception as e:
    logger.warning(f"⚠️ Suite Crypto IA endpoints not loaded: {e}")


# Include router in app
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
