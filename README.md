# 🌍 RiesgoAI Agent - Sistema de Gestión de Riesgo para Colombia

Agente de IA especializado en monitoreo y análisis de riesgos naturales en Colombia, con integración a fuentes oficiales (IDEAM, SGC, UNGRD).

---

## 🎯 Características Principales

### ✅ Fase 1 (MVP - Actual)
- 💬 **Chat con IA especializada** en gestión de riesgo
- 🌦️ **Consultas meteorológicas** (pronósticos, alertas)
- 🌋 **Monitoreo sísmico y volcánico**
- 🏔️ **Evaluación de riesgo de deslizamientos**
- ⚡ **Alertas en tiempo real** vía WebSocket
- 🔌 **API REST completa** para integraciones

### 🚧 Fase 2 (Próximamente)
- 📊 **Dashboard interactivo** con mapas
- 📈 **Análisis predictivo** con ML
- 🚗 **Estado de vías** y denuncias comunitarias
- 📄 **Generación de reportes** automáticos
- 📱 **App móvil** responsiva

---

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Frontend      │  React + Leaflet Maps
│   (Fase 2)      │
└────────┬────────┘
         │
┌────────▼────────┐
│   FastAPI       │  API REST + WebSockets
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┬───────────┬──────────┐
    │         │           │          │
┌───▼───┐ ┌──▼──┐  ┌─────▼─────┐ ┌─▼──┐
│Ollama │ │Redis│  │PostgreSQL │ │APIs│
│Llama  │ │Cache│  │ + PostGIS │ │Ext │
│3.1 70B│ │     │  │           │ │    │
└───────┘ └─────┘  └───────────┘ └────┘
```

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.11+
- PostgreSQL 15+ con PostGIS
- Redis 7+
- Ollama con Llama 3.1
- 16GB+ RAM (32GB recomendado)

### Instalación en 5 pasos

```bash
# 1. Instalar Ollama y descargar modelo
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:70b

# 2. Clonar repositorio
git clone <tu-repo>
cd riesgo-ai-agent

# 3. Instalar dependencias Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Iniciar servidor
python main.py
```

**La API estará en:** http://localhost:8000

**Documentación interactiva:** http://localhost:8000/docs

📖 **Guía completa:** Ver [INSTALACION.md](INSTALACION.md)

---

## 💡 Ejemplos de Uso

### Chat con el Agente

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuál es el pronóstico para Bogotá esta semana?"
  }'
```

### Consultar Sismos Recientes

```bash
curl "http://localhost:8000/earthquakes/recent?hours=48&min_magnitude=3.0"
```

### Evaluar Riesgo de Deslizamiento

```bash
curl -X POST http://localhost:8000/landslide/risk \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 4.60971,
    "longitude": -74.08175
  }'
```

### WebSocket para Alertas en Tiempo Real

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/alerts');

ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  console.log('🚨 Nueva alerta:', alert);
};
```

---

## 📁 Estructura del Proyecto

```
riesgo-ai-agent/
├── main.py                 # API FastAPI principal
├── config.py               # Configuración
├── agent.py                # Agente de IA (LangChain)
├── ideam_client.py         # Cliente IDEAM
├── sgc_client.py           # Cliente SGC
├── requirements.txt        # Dependencias Python
├── .env.example            # Variables de entorno
├── INSTALACION.md          # Guía de instalación
├── ARQUITECTURA.md         # Documentación técnica
└── README.md               # Este archivo
```

---

## 🔌 Integraciones de Datos

### Fuentes Oficiales
- **IDEAM** - Instituto de Hidrología, Meteorología y Estudios Ambientales
  - Pronósticos meteorológicos
  - Alertas por lluvia e inundaciones
  - Datos históricos de estaciones

- **SGC** - Servicio Geológico Colombiano
  - Actividad sísmica en tiempo real
  - Monitoreo de volcanes
  - Mapas de amenaza

- **UNGRD** - Unidad Nacional para la Gestión del Riesgo
  - Alertas oficiales
  - Declaratorias de emergencia

### APIs Adicionales
- **OpenStreetMap** - Datos de vías
- **News APIs** - Noticias relevantes
- **Sentinel Hub** - Imágenes satelitales (Fase 2)

---

## 🤖 Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **LangChain** - Orquestación de LLMs
- **Ollama** - Servidor de modelos locales
- **SQLAlchemy** - ORM para PostgreSQL
- **Redis** - Cache y pub/sub

### IA/ML
- **Llama 3.1 70B** - Modelo de lenguaje principal
- **ChromaDB** - Base de datos vectorial para RAG
- **Sentence Transformers** - Embeddings

### Base de Datos
- **PostgreSQL 15** - Base de datos principal
- **PostGIS** - Extensión geoespacial

---

## 💰 Costos

### Desarrollo (Gratis)
- Ollama: Local, sin costo
- PostgreSQL: Local, sin costo
- Redis: Local, sin costo
- **Total: $0/mes**

### Producción
- **Railway/Render**: $5-10/mes (backend)
- **Supabase**: $0-10/mes (base de datos)
- **Groq API**: $0 (tier gratuito como respaldo)
- **Dominio**: ~$10/año
- **Total estimado: $20-30/mes** (para ~100 usuarios)

---

## 🛣️ Roadmap

### ✅ Fase 1: MVP Backend (Actual)
- [x] API REST con FastAPI
- [x] Agente de IA con LangChain + Ollama
- [x] Integración básica IDEAM/SGC
- [x] WebSockets para alertas
- [x] Documentación

### 🚧 Fase 2: Frontend & Visualización (4-6 semanas)
- [ ] Dashboard React con mapas interactivos
- [ ] Gráficos y visualizaciones
- [ ] Sistema de autenticación
- [ ] Responsive design (móvil)

### 🔮 Fase 3: Análisis Predictivo (8-10 semanas)
- [ ] Modelos ML para predicciones
- [ ] RAG con papers científicos
- [ ] Sistema de denuncias comunitarias
- [ ] Reportes PDF automáticos

### 🚀 Fase 4: Escala (12+ semanas)
- [ ] App móvil nativa
- [ ] Notificaciones push
- [ ] Integración con más fuentes
- [ ] API pública para terceros

---

## 🤝 Contribuir

Este es un proyecto en desarrollo activo. Contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

---

## 🆘 Soporte

- 📖 **Documentación**: Ver carpeta `/docs`
- 🐛 **Issues**: GitHub Issues
- 💬 **Discusiones**: GitHub Discussions

---

## 🙏 Agradecimientos

- **IDEAM** - Por datos meteorológicos públicos
- **SGC** - Por datos geológicos
- **Anthropic/Meta** - Por modelos de IA open source
- **Comunidad Python** - Por increíbles herramientas

---

## 📊 Estado del Proyecto

![Status](https://img.shields.io/badge/status-MVP_Funcional-green)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

**Última actualización:** Febrero 2026
