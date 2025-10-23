"""
Base Service Class - Common functionality for all services
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """Base class for all GuaraniAppStore services"""
    
    def __init__(self, user_id: str, service_id: str, db: AsyncSession):
        self.user_id = user_id
        self.service_id = service_id
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def initialize(self) -> Dict[str, Any]:
        """
        Initialize service for user
        Called when user first subscribes
        Returns: Initial configuration data
        """
        pass
    
    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute service-specific action
        Args:
            action: Action name (e.g., 'scan_fraud', 'analyze_cv', 'generate_blog')
            params: Action parameters
        Returns: Action result
        """
        pass
    
    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """
        Get current service status for user
        Returns: Status information
        """
        pass
    
    async def validate_subscription(self) -> bool:
        """Check if user has active subscription for this service"""
        from sqlalchemy import select
        from models import Order
        
        result = await self.db.execute(
            select(Order).filter(
                Order.user_id == self.user_id,
                Order.service_id == self.service_id,
                Order.payment_status == 'completed'
            )
        )
        order = result.scalar_one_or_none()
        return order is not None
    
    def log_action(self, action: str, status: str, details: Optional[str] = None):
        """Log service action"""
        self.logger.info(
            f"User: {self.user_id} | Service: {self.service_id} | "
            f"Action: {action} | Status: {status} | Details: {details}"
        )
    
    async def save_service_data(self, data: Dict[str, Any]):
        """Save service-specific data to database"""
        # This would save to a service_data collection/table
        # For now, we'll implement a simple key-value store
        pass
    
    async def get_service_data(self, key: str) -> Optional[Any]:
        """Retrieve service-specific data from database"""
        pass
