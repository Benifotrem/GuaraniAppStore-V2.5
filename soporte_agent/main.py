"""
Agente Developer - Backend Principal
Sistema de soporte inteligente con RAG y routing de modelos
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import logging

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Agente Developer API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://soporte_user_seguro:contrasena_fuerte_aqui@postgres_rag:5432/soporte_db_rag")
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(String, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Text)
    metadata = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class QueryRequest(BaseModel):
    question: str
    use_high_model: Optional[bool] = False
    context: Optional[dict] = None

class QueryResponse(BaseModel):
    answer: str
    model_used: str
    confidence: float
    sources: Optional[List[dict]] = None

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL_HIGH = os.getenv("OPENROUTER_MODEL_ID_HIGH", "anthropic/claude-sonnet-4.5")
OPENROUTER_MODEL_LOW = os.getenv("OPENROUTER_MODEL_ID_LOW", "openai/gpt-4o-mini")
ANTHROPIC_FALLBACK = os.getenv("ANTHROPIC_API_KEY_FALLBACK")

# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "soporte_agent",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/query", response_model=QueryResponse)
async def query_agent(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Procesa una consulta usando el agente con routing inteligente
    """
    try:
        # Determinar qué modelo usar
        model_id = OPENROUTER_MODEL_HIGH if request.use_high_model else OPENROUTER_MODEL_LOW
        
        # Buscar contexto relevante en la base de conocimiento (RAG)
        # TODO: Implementar búsqueda vectorial real
        relevant_context = "Contexto de la base de conocimiento..."
        
        # Construir prompt
        prompt = f"""Eres un asistente técnico experto en GuaraniAppStore.
        
Contexto relevante:
{relevant_context}

Pregunta del usuario:
{request.question}

Responde de manera clara y precisa."""
        
        # Llamar a OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://guaraniappstore.com",
            "X-Title": "GuaraniAppStore Agent",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model_id,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                
                return QueryResponse(
                    answer=answer,
                    model_used=model_id,
                    confidence=0.95,
                    sources=[]
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error from OpenRouter: {response.text}"
                )
                
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/knowledge/add")
async def add_knowledge(
    content: str,
    metadata: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """
    Agrega contenido a la base de conocimiento
    """
    try:
        import uuid
        
        knowledge = KnowledgeBase(
            id=str(uuid.uuid4()),
            content=content,
            metadata=str(metadata) if metadata else None
        )
        
        db.add(knowledge)
        db.commit()
        
        return {
            "status": "success",
            "id": knowledge.id,
            "message": "Conocimiento agregado exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error adding knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas del agente
    """
    try:
        knowledge_count = db.query(KnowledgeBase).count()
        
        return {
            "knowledge_base_entries": knowledge_count,
            "models_available": [OPENROUTER_MODEL_HIGH, OPENROUTER_MODEL_LOW],
            "status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
