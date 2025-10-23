"""
Utilidades para manejo de zonas horarias por país
"""
from datetime import datetime
import pytz

# Mapeo de países a zonas horarias (principales países de América Latina)
COUNTRY_TIMEZONES = {
    'Paraguay': 'America/Asuncion',
    'Argentina': 'America/Argentina/Buenos_Aires',
    'Brasil': 'America/Sao_Paulo',
    'Chile': 'America/Santiago',
    'Uruguay': 'America/Montevideo',
    'Bolivia': 'America/La_Paz',
    'Perú': 'America/Lima',
    'Colombia': 'America/Bogota',
    'Venezuela': 'America/Caracas',
    'Ecuador': 'America/Guayaquil',
    'México': 'America/Mexico_City',
    'España': 'Europe/Madrid',
    'Estados Unidos': 'America/New_York',
    'USA': 'America/New_York',
}

def get_timezone_for_country(country: str) -> str:
    """
    Obtiene la zona horaria para un país específico.
    Por defecto retorna America/Asuncion (Paraguay)
    """
    return COUNTRY_TIMEZONES.get(country, 'America/Asuncion')

def convert_to_user_timezone(utc_datetime: datetime, user_timezone: str) -> datetime:
    """
    Convierte un datetime UTC a la zona horaria del usuario
    """
    if utc_datetime.tzinfo is None:
        utc_datetime = pytz.utc.localize(utc_datetime)
    
    user_tz = pytz.timezone(user_timezone)
    return utc_datetime.astimezone(user_tz)

def convert_to_utc(local_datetime: datetime, user_timezone: str) -> datetime:
    """
    Convierte un datetime local a UTC
    """
    user_tz = pytz.timezone(user_timezone)
    if local_datetime.tzinfo is None:
        local_datetime = user_tz.localize(local_datetime)
    
    return local_datetime.astimezone(pytz.utc)

def get_current_time_for_user(user_timezone: str) -> datetime:
    """
    Obtiene la hora actual en la zona horaria del usuario
    """
    user_tz = pytz.timezone(user_timezone)
    return datetime.now(user_tz)

def format_datetime_for_user(dt: datetime, user_timezone: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Formatea un datetime para mostrar al usuario en su zona horaria
    """
    user_dt = convert_to_user_timezone(dt, user_timezone)
    return user_dt.strftime(format_str)

# Lista de países soportados (para frontend)
SUPPORTED_COUNTRIES = list(COUNTRY_TIMEZONES.keys())
