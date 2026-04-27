# Arquitectura del Sistema - Agente IA Gestión de Riesgo Colombia

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Web/Mobile)                     │
│              React + Leaflet Maps + Chart.js                 │
└─────────────────────────────────────────────────────────────┘
                              ↕️
┌─────────────────────────────────────────────────────────────┐
│                   API BACKEND (FastAPI)                      │
│  - Endpoints REST                                            │
│  - WebSockets (tiempo real)                                  │
│  - Autenticación JWT                                         │
└─────────────────────────────────────────────────────────────┘
                              ↕️
┌──────────────────┬──────────────────┬──────────────────────┐
│   AGENTE IA      │   DATA LAYER     │   EXTERNAL APIs      │
│                  │                  │                      │
│ Ollama/Llama 3.1 │ PostgreSQL +     │ - IDEAM              │
│ + LangChain      │ PostGIS          │ - SGC (Ingeominas)   │
│ + RAG System     │                  │ - UNGRD              │
│                  │ Redis (cache)    │ - OpenStreetMap      │
│                  │                  │ - Noticias APIs      │
└──────────────────┴──────────────────┴──────────────────────┘
```

## 🎯 Componentes Principales

### 1. BACKEND API (FastAPI)
**Ubicación**: Cloud (Railway/Render)
**Responsabilidades**:
- Servir API REST para frontend
- Orquestar llamadas a fuentes de datos
- Gestionar cache con Redis
- WebSockets para alertas en tiempo real
- Autenticación de usuarios

### 2. AGENTE IA (Ollama + LangChain)
**Ubicación**: Local/Servidor dedicado
**Responsabilidades**:
- Procesamiento de lenguaje natural
- Análisis de documentos científicos (RAG)
- Generación de reportes
- Predicciones basadas en datos históricos
- Respuestas a consultas de usuarios

### 3. DATA LAYER
**Ubicación**: Cloud (Supabase/Railway)
**Componentes**:
- **PostgreSQL + PostGIS**: Datos geoespaciales
- **Redis**: Cache de pronósticos y alertas
- **S3/R2**: Almacenamiento de reportes y documentos

### 4. INTEGRACIONES EXTERNAS
**APIs a conectar**:
- **IDEAM**: Meteorología, hidrología
- **SGC (Servicio Geológico)**: Sismología, volcanes
- **UNGRD**: Alertas oficiales
- **OpenStreetMap**: Estado de vías
- **Sistema de denuncias**: Comunidad

## 📦 Stack Tecnológico

### Backend
- **Python 3.11+**
- **FastAPI** (API moderna y rápida)
- **SQLAlchemy + GeoAlchemy2** (ORM geoespacial)
- **LangChain** (orquestación IA)
- **Ollama** (servidor de modelos)
- **Celery** (tareas asíncronas)

### Frontend
- **React 18** + **TypeScript**
- **Leaflet** (mapas interactivos)
- **Recharts** (visualizaciones)
- **TailwindCSS** (estilos)

### Base de Datos
- **PostgreSQL 15** + **PostGIS**
- **Redis** (cache)

### IA/ML
- **Llama 3.1 70B** (modelo principal)
- **Groq API** (respaldo rápido)
- **ChromaDB** (vectores para RAG)

## 🔄 Flujo de Datos

### Consulta de Usuario:
1. Usuario pregunta en frontend
2. Frontend → Backend API
3. Backend → Agente IA (local)
4. IA consulta fuentes necesarias (IDEAM, BD, etc)
5. IA genera respuesta + visualizaciones
6. Backend → Frontend (respuesta formateada)

### Alertas en Tiempo Real:
1. Celery task cada 5 min consulta IDEAM/SGC
2. Detecta cambios/alertas
3. Guarda en BD + Redis
4. WebSocket notifica a usuarios conectados
5. Frontend muestra notificación

## 🚀 Despliegue

### Fase 1 (MVP):
- Backend: Railway (gratis)
- BD: Supabase (gratis)
- IA: Local en tu PC
- Frontend: Vercel (gratis)

### Fase 2 (Producción):
- Backend: Railway/Render (pago bajo)
- BD: Railway Postgres
- IA: Servidor dedicado + Groq API
- Frontend: Vercel Pro

## 💰 Costos Estimados

**Fase 1 (Desarrollo)**: $0/mes
- Todo en tiers gratuitos

**Fase 2 (100 usuarios)**: ~$20-30/mes
- Railway: $5-10
- Supabase: $0-10
- Groq API: $0 (tier gratuito)
- Dominio: $10/año

**Fase 3 (1000+ usuarios)**: ~$100-150/mes
- Servidor dedicado para IA: $50-80
- BD escalada: $30-50
- APIs premium: $20-30

## 🔐 Seguridad

- JWT para autenticación
- Rate limiting en APIs
- Validación de datos geoespaciales
- HTTPS obligatorio
- Sanitización de inputs SQL
