# Estructura del Proyecto

```
riesgo-ai-agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app principal
│   │   ├── config.py               # Configuración
│   │   ├── database.py             # Conexión DB
│   │   │
│   │   ├── api/                    # Endpoints API
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # Chat con IA
│   │   │   ├── weather.py          # Pronósticos
│   │   │   ├── alerts.py           # Alertas
│   │   │   ├── roads.py            # Estado vías
│   │   │   └── reports.py          # Reportes
│   │   │
│   │   ├── models/                 # Modelos SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── alert.py
│   │   │   ├── weather.py
│   │   │   ├── road.py
│   │   │   └── report.py
│   │   │
│   │   ├── ai/                     # Sistema IA
│   │   │   ├── __init__.py
│   │   │   ├── agent.py            # Agente principal
│   │   │   ├── tools.py            # Herramientas para IA
│   │   │   ├── prompts.py          # Prompts del sistema
│   │   │   └── rag.py              # RAG para documentos
│   │   │
│   │   ├── integrations/           # APIs externas
│   │   │   ├── __init__.py
│   │   │   ├── ideam.py            # Cliente IDEAM
│   │   │   ├── sgc.py              # Servicio Geológico
│   │   │   ├── ungrd.py            # UNGRD
│   │   │   └── osm.py              # OpenStreetMap
│   │   │
│   │   ├── services/               # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── weather_service.py
│   │   │   ├── alert_service.py
│   │   │   └── prediction_service.py
│   │   │
│   │   └── utils/                  # Utilidades
│   │       ├── __init__.py
│   │       ├── geo.py              # Funciones geoespaciales
│   │       └── cache.py            # Redis helpers
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.tsx
│   │   │   ├── Map.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   └── Alerts.tsx
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
│
├── data/
│   ├── documents/                  # Papers, PDFs para RAG
│   └── vector_store/               # ChromaDB
│
├── scripts/
│   ├── setup.sh                    # Instalación
│   ├── seed_db.py                  # Datos iniciales
│   └── fetch_historical.py         # Descargar históricos
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Descripción de Componentes

### Backend (`/backend`)
Servidor FastAPI que maneja toda la lógica

### Frontend (`/frontend`)
Interfaz React con mapas y dashboards

### Data (`/data`)
Almacenamiento local de documentos y vectores

### Scripts (`/scripts`)
Utilidades de setup y mantenimiento
