"""
GuaraniAppStore V2.5 Pro - Chat Memory Service
Sistema de memoria persistente para agentes de chat con retención de 30 días.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
import logging

from models import ChatSession, ChatMessage, User
from database import AsyncSessionLocal

logger = logging.getLogger(__name__)


class ChatMemoryService:
    """
    Servicio para gestionar la memoria persistente de los agentes de chat.
    
    Características:
    - Retención de contexto por 30 días
    - Detección de "primer mensaje del día"
    - Carga eficiente de contexto histórico
    - Limpieza automática de mensajes antiguos
    """
    
    RETENTION_DAYS = 30
    
    def __init__(self):
        self.retention_days = self.RETENTION_DAYS
    
    async def get_or_create_session(
        self,
        agent_name: str,
        user_id: Optional[str] = None,
        visitor_id: Optional[str] = None,
        session_metadata: Optional[Dict[str, Any]] = None
    ) -> ChatSession:
        """
        Obtiene una sesión existente o crea una nueva.
        
        Args:
            agent_name: Nombre del agente ('junior', 'jacinto', 'alex', 'rocio', 'silvia', 'blanca')
            user_id: ID del usuario registrado (opcional)
            visitor_id: ID del visitante anónimo (opcional)
            session_metadata: Metadata adicional de la sesión
        
        Returns:
            ChatSession: Sesión de chat activa
        """
        async with AsyncSessionLocal() as db:
            # Buscar sesión activa existente
            query = select(ChatSession).where(
                and_(
                    ChatSession.agent_name == agent_name,
                    ChatSession.is_active == True
                )
            )
            
            if user_id:
                query = query.where(ChatSession.user_id == user_id)
            elif visitor_id:
                query = query.where(ChatSession.visitor_id == visitor_id)
            
            result = await db.execute(query)
            session = result.scalar_one_or_none()
            
            if session:
                # Actualizar última interacción
                session.last_interaction_date = datetime.now(timezone.utc)
                await db.commit()
                await db.refresh(session)
                return session
            
            # Crear nueva sesión
            session = ChatSession(
                agent_name=agent_name,
                user_id=user_id,
                visitor_id=visitor_id,
                session_metadata=session_metadata or {},
                first_interaction_date=datetime.now(timezone.utc),
                last_interaction_date=datetime.now(timezone.utc)
            )
            
            db.add(session)
            await db.commit()
            await db.refresh(session)
            
            logger.info(f"Nueva sesión de chat creada: {session.id} con agente {agent_name}")
            return session
    
    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        token_count: Optional[int] = None,
        model_used: Optional[str] = None,
        sentiment: Optional[str] = None,
        intent: Optional[str] = None,
        message_metadata: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        """
        Agrega un mensaje a la sesión de chat.
        
        Args:
            session_id: ID de la sesión
            role: 'user', 'assistant', 'system'
            content: Contenido del mensaje
            token_count: Número de tokens (opcional)
            model_used: Modelo LLM usado (opcional)
            sentiment: Sentimiento detectado (opcional)
            intent: Intención detectada (opcional)
            message_metadata: Metadata adicional
        
        Returns:
            ChatMessage: Mensaje creado
        """
        async with AsyncSessionLocal() as db:
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                timestamp=datetime.now(timezone.utc),
                token_count=token_count,
                model_used=model_used,
                sentiment=sentiment,
                intent=intent,
                message_metadata=message_metadata or {}
            )
            
            db.add(message)
            
            # Actualizar contador de mensajes en la sesión
            session_query = select(ChatSession).where(ChatSession.id == session_id)
            session_result = await db.execute(session_query)
            session = session_result.scalar_one_or_none()
            
            if session:
                session.total_messages += 1
                session.last_interaction_date = datetime.now(timezone.utc)
            
            await db.commit()
            await db.refresh(message)
            
            return message
    
    async def get_session_history(
        self,
        session_id: str,
        limit: int = 50,
        include_system: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de mensajes de una sesión.
        
        Args:
            session_id: ID de la sesión
            limit: Número máximo de mensajes a retornar
            include_system: Incluir mensajes del sistema
        
        Returns:
            List[Dict]: Lista de mensajes en formato dict
        """
        async with AsyncSessionLocal() as db:
            query = select(ChatMessage).where(ChatMessage.session_id == session_id)
            
            if not include_system:
                query = query.where(ChatMessage.role != 'system')
            
            query = query.order_by(ChatMessage.timestamp.desc()).limit(limit)
            
            result = await db.execute(query)
            messages = result.scalars().all()
            
            # Retornar en orden cronológico (más antiguo primero)
            return [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'sentiment': msg.sentiment,
                    'intent': msg.intent
                }
                for msg in reversed(messages)
            ]
    
    async def is_first_message_today(
        self,
        agent_name: str,
        user_id: Optional[str] = None,
        visitor_id: Optional[str] = None
    ) -> bool:
        """
        Determina si este es el primer mensaje del día para el usuario/visitante.
        
        Args:
            agent_name: Nombre del agente
            user_id: ID del usuario registrado (opcional)
            visitor_id: ID del visitante anónimo (opcional)
        
        Returns:
            bool: True si es el primer mensaje del día
        """
        async with AsyncSessionLocal() as db:
            # Obtener inicio del día actual en UTC
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Buscar mensajes del usuario/visitante hoy
            query = select(ChatMessage).join(ChatSession).where(
                and_(
                    ChatSession.agent_name == agent_name,
                    ChatMessage.timestamp >= today_start
                )
            )
            
            if user_id:
                query = query.where(ChatSession.user_id == user_id)
            elif visitor_id:
                query = query.where(ChatSession.visitor_id == visitor_id)
            
            result = await db.execute(query)
            messages = result.scalars().all()
            
            # Si no hay mensajes hoy, es el primer mensaje del día
            return len(messages) == 0
    
    async def cleanup_old_messages(self) -> int:
        """
        Elimina mensajes con más de RETENTION_DAYS días.
        
        Returns:
            int: Número de mensajes eliminados
        """
        async with AsyncSessionLocal() as db:
            cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
            
            # Eliminar mensajes antiguos
            delete_query = delete(ChatMessage).where(
                ChatMessage.timestamp < cutoff_date
            )
            
            result = await db.execute(delete_query)
            deleted_count = result.rowcount
            
            await db.commit()
            
            logger.info(f"Limpieza de mensajes antiguos: {deleted_count} mensajes eliminados")
            return deleted_count
    
    async def cleanup_inactive_sessions(self, days_inactive: int = 30) -> int:
        """
        Marca sesiones inactivas como inactivas.
        
        Args:
            days_inactive: Días de inactividad para considerar sesión inactiva
        
        Returns:
            int: Número de sesiones marcadas como inactivas
        """
        async with AsyncSessionLocal() as db:
            cutoff_date = datetime.utcnow() - timedelta(days=days_inactive)
            
            # Buscar sesiones inactivas
            query = select(ChatSession).where(
                and_(
                    ChatSession.last_interaction_date < cutoff_date,
                    ChatSession.is_active == True
                )
            )
            
            result = await db.execute(query)
            sessions = result.scalars().all()
            
            count = 0
            for session in sessions:
                session.is_active = False
                count += 1
            
            await db.commit()
            
            logger.info(f"Sesiones marcadas como inactivas: {count}")
            return count
    
    async def get_user_stats(
        self,
        user_id: Optional[str] = None,
        visitor_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso del usuario.
        
        Args:
            user_id: ID del usuario registrado
            visitor_id: ID del visitante anónimo
        
        Returns:
            Dict: Estadísticas de uso
        """
        async with AsyncSessionLocal() as db:
            query = select(ChatSession)
            
            if user_id:
                query = query.where(ChatSession.user_id == user_id)
            elif visitor_id:
                query = query.where(ChatSession.visitor_id == visitor_id)
            
            result = await db.execute(query)
            sessions = result.scalars().all()
            
            total_messages = sum(s.total_messages for s in sessions)
            active_sessions = sum(1 for s in sessions if s.is_active)
            
            return {
                'total_sessions': len(sessions),
                'active_sessions': active_sessions,
                'total_messages': total_messages,
                'agents_used': list(set(s.agent_name for s in sessions))
            }


# Instancia global del servicio
chat_memory_service = ChatMemoryService()
