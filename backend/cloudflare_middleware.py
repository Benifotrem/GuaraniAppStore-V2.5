"""
GuaraniAppStore V2.5 Pro - Middleware para Cloudflare
Maneja correctamente IPs reales, headers especiales y configuraciones para producción con Cloudflare
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)


class CloudflareMiddleware(BaseHTTPMiddleware):
    """
    Middleware para manejar requests que pasan por Cloudflare
    
    Características:
    - Extrae IP real del cliente desde CF-Connecting-IP
    - Registra CF-Ray para debugging
    - Maneja CF-Visitor para detectar protocolo original
    - Agrega headers de seguridad adicionales
    """
    
    async def dispatch(self, request: Request, call_next):
        # Extraer IP real del cliente
        cf_connecting_ip = request.headers.get('CF-Connecting-IP')
        if cf_connecting_ip:
            # Cloudflare pasa la IP real en este header
            request.state.real_ip = cf_connecting_ip
            logger.debug(f"Real IP from Cloudflare: {cf_connecting_ip}")
        else:
            # Fallback a X-Forwarded-For o client IP directa
            x_forwarded_for = request.headers.get('X-Forwarded-For')
            if x_forwarded_for:
                # Tomar la primera IP de la lista
                request.state.real_ip = x_forwarded_for.split(',')[0].strip()
            else:
                request.state.real_ip = request.client.host if request.client else 'unknown'
        
        # Extraer CF-Ray para debugging (útil para reportar problemas a Cloudflare)
        cf_ray = request.headers.get('CF-Ray')
        if cf_ray:
            request.state.cf_ray = cf_ray
            logger.debug(f"CF-Ray: {cf_ray}")
        
        # Detectar si la request original era HTTPS
        cf_visitor = request.headers.get('CF-Visitor')
        if cf_visitor:
            # CF-Visitor es un JSON que indica el esquema original
            request.state.cf_visitor = cf_visitor
            logger.debug(f"CF-Visitor: {cf_visitor}")
        
        # Detectar país del visitante (útil para analytics y geolocalización)
        cf_ipcountry = request.headers.get('CF-IPCountry')
        if cf_ipcountry:
            request.state.country = cf_ipcountry
            logger.debug(f"Country: {cf_ipcountry}")
        
        # Procesar request
        response: Response = await call_next(request)
        
        # Agregar headers de seguridad (Cloudflare ya agrega algunos, pero reforzamos)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response


def get_real_ip(request: Request) -> str:
    """
    Helper function para obtener la IP real del cliente
    Usar esto en lugar de request.client.host cuando necesites la IP real
    
    Args:
        request: FastAPI Request object
    
    Returns:
        IP real del cliente
    """
    if hasattr(request.state, 'real_ip'):
        return request.state.real_ip
    
    # Fallback si el middleware no se ejecutó
    cf_connecting_ip = request.headers.get('CF-Connecting-IP')
    if cf_connecting_ip:
        return cf_connecting_ip
    
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    
    return request.client.host if request.client else 'unknown'


def get_cf_ray(request: Request) -> str:
    """
    Obtener CF-Ray ID (útil para debugging y reportes a Cloudflare)
    
    Args:
        request: FastAPI Request object
    
    Returns:
        CF-Ray ID o 'unknown'
    """
    if hasattr(request.state, 'cf_ray'):
        return request.state.cf_ray
    
    return request.headers.get('CF-Ray', 'unknown')


def get_country(request: Request) -> str:
    """
    Obtener país del visitante detectado por Cloudflare
    
    Args:
        request: FastAPI Request object
    
    Returns:
        Código ISO de país (ej: 'PY', 'US', 'BR') o 'XX' si no disponible
    """
    if hasattr(request.state, 'country'):
        return request.state.country
    
    return request.headers.get('CF-IPCountry', 'XX')
