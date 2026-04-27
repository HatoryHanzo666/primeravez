# 🚀 Guía de Instalación - RiesgoAI Agent

## Requisitos Previos

### Hardware
- **RAM**: Mínimo 16GB (recomendado 32GB para Llama 3.1 70B)
- **GPU**: NVIDIA con 8GB+ VRAM (recomendado) o CPU potente
- **Disco**: 50GB libres (modelos de IA ocupan espacio)

### Software
- **Python**: 3.11 o superior
- **PostgreSQL**: 15 o superior con extensión PostGIS
- **Redis**: 7.0 o superior
- **Ollama**: Para ejecutar modelos localmente
- **Node.js**: 18+ (para frontend, Fase 2)

---

## 📋 Instalación Paso a Paso

### 1. Instalar Ollama (Motor de IA Local)

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Descargar de https://ollama.com/download

**Verificar instalación:**
```bash
ollama --version
```

**Descargar modelo Llama 3.1:**
```bash
# Modelo 70B (recomendado, requiere ~40GB RAM)
ollama pull llama3.1:70b

# O modelo 8B (más liviano, ~8GB RAM)
ollama pull llama3.1:8b
```

---

### 2. Instalar PostgreSQL + PostGIS

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql-15 postgresql-15-postgis-3
sudo systemctl start postgresql
```

**Mac (Homebrew):**
```bash
brew install postgresql@15 postgis
brew services start postgresql@15
```

**Windows:**
Descargar de https://www.postgresql.org/download/windows/

**Crear base de datos:**
```bash
sudo -u postgres psql

# En el prompt de PostgreSQL:
CREATE DATABASE riesgo_db;
\c riesgo_db
CREATE EXTENSION postgis;
\q
```

---

### 3. Instalar Redis

**Ubuntu/Debian:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Windows:**
Usar Redis en Docker o WSL

**Verificar:**
```bash
redis-cli ping
# Debe responder: PONG
```

---

### 4. Configurar el Proyecto Python

**Clonar/crear estructura:**
```bash
mkdir riesgo-ai-agent
cd riesgo-ai-agent

# Copiar archivos del prototipo aquí
```

**Crear entorno virtual:**
```bash
python -m venv venv

# Activar:
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

**Instalar dependencias:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 5. Configurar Variables de Entorno

**Copiar archivo de ejemplo:**
```bash
cp .env.example .env
```

**Editar `.env` con tus valores:**
```bash
nano .env  # o tu editor preferido
```

**Valores mínimos necesarios:**
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/riesgo_db
REDIS_URL=redis://localhost:6379/0
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:70b  # o llama3.1:8b si usas el modelo pequeño
SECRET_KEY=genera-una-clave-aleatoria-segura
```

---

### 6. Iniciar Servicios

**Terminal 1 - Ollama (si no está corriendo):**
```bash
ollama serve
```

**Terminal 2 - Redis (si no está como servicio):**
```bash
redis-server
```

**Terminal 3 - Backend API:**
```bash
cd riesgo-ai-agent
source venv/bin/activate
python main.py
```

La API estará disponible en: http://localhost:8000

---

## 🧪 Probar la Instalación

### 1. Verificar API
```bash
curl http://localhost:8000/
```

Debe responder:
```json
{
  "app": "RiesgoAI Agent",
  "version": "0.1.0",
  "status": "online"
}
```

### 2. Probar el Agente de IA
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿qué puedes hacer?"}'
```

### 3. Interfaz Interactiva (Swagger)
Abrir en navegador:
```
http://localhost:8000/docs
```

Aquí puedes probar todos los endpoints de forma interactiva.

---

## 🔧 Solución de Problemas

### Error: "Cannot connect to Ollama"
```bash
# Verificar que Ollama esté corriendo:
ollama list

# Reiniciar Ollama:
# Linux/Mac:
pkill ollama
ollama serve

# Windows: cerrar y reabrir Ollama
```

### Error: "Connection to database failed"
```bash
# Verificar PostgreSQL:
sudo systemctl status postgresql

# Verificar credenciales en .env
psql -U postgres -d riesgo_db -c "SELECT version();"
```

### Error: "Redis connection refused"
```bash
# Verificar Redis:
redis-cli ping

# Iniciar si no está corriendo:
sudo systemctl start redis
```

### Modelo muy lento / Out of Memory
```bash
# Cambiar a modelo más pequeño en .env:
OLLAMA_MODEL=llama3.1:8b

# O usar Groq API (gratis) en vez de local:
GROQ_API_KEY=tu-api-key-de-groq
# Registrarse en: https://console.groq.com
```

---

## 📊 Próximos Pasos

Una vez instalado correctamente:

1. **✅ Fase 1 Completada**: Tienes el backend funcionando
2. **➡️ Siguiente**: Implementar scraping real de IDEAM/SGC
3. **➡️ Después**: Crear base de datos con modelos SQLAlchemy
4. **➡️ Luego**: Desarrollar frontend React

---

## 🆘 Obtener Ayuda

Si tienes problemas:
1. Revisa los logs en la consola
2. Verifica que todos los servicios estén corriendo
3. Consulta la documentación de cada componente

---

## 📝 Notas Importantes

- **Primera ejecución**: El modelo de IA puede tardar en cargar (30-60 seg)
- **Desarrollo**: Usa `DEBUG=True` en `.env`
- **Producción**: Cambia `SECRET_KEY` y `DEBUG=False`
- **RAM**: El modelo 70B necesita ~40GB RAM, usa 8B si tienes menos
