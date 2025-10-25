"""
Script de Migración: MongoDB → PostgreSQL
Migra datos de conocimiento y documentación para el RAG
"""
import os
import sys
from pymongo import MongoClient
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017/guarani_appstore")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://soporte_user_seguro:contrasena_fuerte_aqui@postgres_rag:5432/soporte_db_rag")

def connect_mongodb():
    """Conectar a MongoDB"""
    try:
        client = MongoClient(MONGO_URL)
        db = client.get_database()
        logger.info(f"✅ Conectado a MongoDB: {db.name}")
        return client, db
    except Exception as e:
        logger.error(f"❌ Error conectando a MongoDB: {str(e)}")
        sys.exit(1)

def connect_postgres():
    """Conectar a PostgreSQL"""
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        logger.info("✅ Conectado a PostgreSQL")
        return conn
    except Exception as e:
        logger.error(f"❌ Error conectando a PostgreSQL: {str(e)}")
        sys.exit(1)

def create_postgres_tables(conn):
    """Crear tablas en PostgreSQL si no existen"""
    try:
        cursor = conn.cursor()
        
        # Tabla de base de conocimiento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id VARCHAR(255) PRIMARY KEY,
                content TEXT NOT NULL,
                embedding TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de documentación migrade
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrated_docs (
                id SERIAL PRIMARY KEY,
                mongo_id VARCHAR(255) UNIQUE,
                doc_type VARCHAR(100),
                content TEXT,
                migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        logger.info("✅ Tablas PostgreSQL creadas/verificadas")
        
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {str(e)}")
        conn.rollback()
        raise

def migrate_services(mongo_db, pg_conn):
    """Migrar información de servicios como base de conocimiento"""
    try:
        services = mongo_db.services.find()
        cursor = pg_conn.cursor()
        count = 0
        
        for service in services:
            # Crear contenido descriptivo
            content = f"""
Servicio: {service.get('name', 'N/A')}
Descripción: {service.get('description', 'N/A')}
Slug: {service.get('slug', 'N/A')}
Categoría: {service.get('category', 'N/A')}
Estado: {service.get('status', 'N/A')}
            """.strip()
            
            # Insertar en knowledge_base
            cursor.execute("""
                INSERT INTO knowledge_base (id, content, metadata)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                str(service.get('_id')),
                content,
                f"type:service,slug:{service.get('slug')}"
            ))
            
            count += 1
        
        pg_conn.commit()
        logger.info(f"✅ Migrados {count} servicios")
        
    except Exception as e:
        logger.error(f"❌ Error migrando servicios: {str(e)}")
        pg_conn.rollback()
        raise

def migrate_users_info(mongo_db, pg_conn):
    """Migrar información agregada de usuarios (sin datos sensibles)"""
    try:
        total_users = mongo_db.users.count_documents({})
        admin_users = mongo_db.users.count_documents({'is_admin': True})
        
        cursor = pg_conn.cursor()
        
        content = f"""
Estadísticas de Usuarios:
- Total de usuarios: {total_users}
- Usuarios administradores: {admin_users}
- Usuarios regulares: {total_users - admin_users}
        """.strip()
        
        cursor.execute("""
            INSERT INTO knowledge_base (id, content, metadata)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            'user_stats',
            content,
            'type:stats,category:users'
        ))
        
        pg_conn.commit()
        logger.info("✅ Estadísticas de usuarios migradas")
        
    except Exception as e:
        logger.error(f"❌ Error migrando info de usuarios: {str(e)}")
        pg_conn.rollback()
        raise

def main():
    """Función principal de migración"""
    logger.info("🚀 Iniciando migración MongoDB → PostgreSQL")
    
    # Conectar a bases de datos
    mongo_client, mongo_db = connect_mongodb()
    pg_conn = connect_postgres()
    
    try:
        # Crear tablas
        create_postgres_tables(pg_conn)
        
        # Migrar datos
        logger.info("📦 Migrando servicios...")
        migrate_services(mongo_db, pg_conn)
        
        logger.info("📊 Migrando estadísticas de usuarios...")
        migrate_users_info(mongo_db, pg_conn)
        
        logger.info("✅ ¡Migración completada exitosamente!")
        
    except Exception as e:
        logger.error(f"❌ Error durante la migración: {str(e)}")
        sys.exit(1)
        
    finally:
        # Cerrar conexiones
        mongo_client.close()
        pg_conn.close()
        logger.info("🔒 Conexiones cerradas")

if __name__ == "__main__":
    main()
