"""
API Principal - FastAPI
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

from config import get_settings
from agent import riesgo_agent

# Configuración
settings = get_settings()

# App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gestión de riesgo de desastres en Colombia"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== MODELOS PYDANTIC ====================

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    sources: List[str] = []


class WeatherQuery(BaseModel):
    city: str
    days: int = 7


class AlertsResponse(BaseModel):
    alerts: List[Dict[str, Any]]
    count: int
    last_updated: datetime


class LocationQuery(BaseModel):
    latitude: float
    longitude: float


# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Endpoint principal de chat con el agente de IA
    
    Ejemplo:
    ```
    POST /chat
    {
        "message": "¿Cuál es el pronóstico para Bogotá?",
        "session_id": "user123"
    }
    ```
    """
    try:
        logger.info(f"Nueva consulta de chat: {message.message}")
        
        # Procesar con el agente de IA
        result = await riesgo_agent.query(message.message)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Error procesando consulta"))
        
        return ChatResponse(
            response=result["response"],
            timestamp=datetime.now(),
            sources=[]  # TODO: Extraer fuentes de intermediate_steps
        )
        
    except Exception as e:
        logger.error(f"Error en chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/weather/forecast")
async def get_weather_forecast(query: WeatherQuery):
    """
    Obtiene pronóstico del tiempo para una ciudad
    
    Ejemplo:
    ```
    POST /weather/forecast
    {
        "city": "Bogotá",
        "days": 7
    }
    ```
    """
    try:
        from ideam_client import ideam_client
        
        forecast = await ideam_client.get_weather_forecast(
            city=query.city,
            days=query.days
        )
        
        if not forecast:
            raise HTTPException(status_code=404, detail=f"No se encontró pronóstico para {query.city}")
        
        return forecast
        
    except Exception as e:
        logger.error(f"Error obteniendo pronóstico: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts", response_model=AlertsResponse)
async def get_active_alerts():
    """
    Obtiene todas las alertas activas (meteorológicas y geológicas)
    
    Ejemplo:
    ```
    GET /alerts
    ```
    """
    try:
        from ideam_client import ideam_client
        from sgc_client import sgc_client
        
        # Obtener alertas de múltiples fuentes
        weather_alerts = await ideam_client.get_active_alerts()
        geo_alerts = await sgc_client.get_geological_alerts()
        
        all_alerts = weather_alerts + geo_alerts
        
        return AlertsResponse(
            alerts=all_alerts,
            count=len(all_alerts),
            last_updated=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo alertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/earthquakes/recent")
async def get_recent_earthquakes(hours: int = 24, min_magnitude: float = 2.5):
    """
    Obtiene sismos recientes
    
    Parámetros:
    - hours: Últimas N horas (default: 24)
    - min_magnitude: Magnitud mínima (default: 2.5)
    
    Ejemplo:
    ```
    GET /earthquakes/recent?hours=48&min_magnitude=3.0
    ```
    """
    try:
        from sgc_client import sgc_client
        
        earthquakes = await sgc_client.get_recent_earthquakes(
            hours=hours,
            min_magnitude=min_magnitude
        )
        
        return {
            "earthquakes": earthquakes,
            "count": len(earthquakes),
            "period_hours": hours,
            "min_magnitude": min_magnitude,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo sismos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/volcanoes/status")
async def get_volcano_status(volcano_name: Optional[str] = None):
    """
    Obtiene estado de volcanes
    
    Parámetros:
    - volcano_name: Nombre específico o None para todos
    
    Ejemplo:
    ```
    GET /volcanoes/status?volcano_name=Nevado del Ruiz
    ```
    """
    try:
        from sgc_client import sgc_client
        
        status = await sgc_client.get_volcano_status(volcano_name)
        
        return {
            "volcanoes": status,
            "count": len(status),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado volcanes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/landslide/risk")
async def get_landslide_risk(location: LocationQuery):
    """
    Evalúa riesgo de deslizamiento para una ubicación
    
    Ejemplo:
    ```
    POST /landslide/risk
    {
        "latitude": 4.60971,
        "longitude": -74.08175
    }
    ```
    """
    try:
        from sgc_client import sgc_client
        
        risk = await sgc_client.get_landslide_susceptibility(
            lat=location.latitude,
            lon=location.longitude
        )
        
        if not risk:
            raise HTTPException(status_code=404, detail="No se pudo evaluar el riesgo")
        
        return risk
        
    except Exception as e:
        logger.error(f"Error evaluando riesgo deslizamiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== WEBSOCKET ====================

class ConnectionManager:
    """Gestiona conexiones WebSocket para alertas en tiempo real"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nueva conexión WebSocket. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Conexión WebSocket cerrada. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Envía mensaje a todos los clientes conectados"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error enviando mensaje: {e}")


manager = ConnectionManager()


@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """
    WebSocket para recibir alertas en tiempo real
    
    Ejemplo de uso en JS:
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/ws/alerts');
    ws.onmessage = (event) => {
        const alert = JSON.parse(event.data);
        console.log('Nueva alerta:', alert);
    };
    ```
    """
    await manager.connect(websocket)
    try:
        while True:
            # Mantener conexión viva
            data = await websocket.receive_text()
            
            # Echo para ping/pong
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Inicialización de la app"""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} iniciando...")
    
    # TODO: Conectar a BD
    # TODO: Iniciar tareas de background (Celery)
    
    logger.info("App lista ✓")


@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al cerrar"""
    logger.info("Cerrando aplicación...")
    
    # TODO: Cerrar conexiones BD
    # TODO: Detener tareas background


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
