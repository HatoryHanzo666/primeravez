"""
Agente de IA para Gestión de Riesgo - VERSIÓN COMPLETA
Con integración de datos reales del SGC (Servicio Geológico Colombiano)
"""
import requests
import json
import os
from datetime import datetime
from sgc_integration import (
    sgc_client, 
    formatear_info_sismos,
    formatear_info_volcanes,
    formatear_info_movimientos
)
from ideam_integration import (
    ideam_client,
    formatear_pronostico,
    formatear_alertas,
    formatear_info_lluvias
)

# Importar sistema de mapas
try:
    from mapas_helper import (
        generar_mapa_sismos_sgc,
        generar_mapa_volcanes_sgc,
        generar_mapa_estaciones_ideam,
        generar_mapa_integrado,
        verificar_sistema_mapas,
        MAPAS_DISPONIBLES
)
except ImportError:
    MAPAS_DISPONIBLES = False
    print("⚠️ Sistema de mapas no disponible. Instala: pip install geopandas matplotlib matplotlib-scalebar")

# CONFIGURACIÓN
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Archivos de datos
HISTORIAL_FILE = "historial.json"
FAVORITOS_FILE = "favoritos.json"
ESTADISTICAS_FILE = "estadisticas.json"


def cargar_datos(archivo, default=None):
    """Carga datos de un archivo JSON"""
    if default is None:
        default = []
    
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    return default


def guardar_datos(archivo, datos):
    """Guarda datos en un archivo JSON"""
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando datos: {e}")
        return False


def chat_con_agente(pregunta: str, contexto_sgc=None) -> str:
    """
    Habla con el agente usando Groq API
    
    Args:
        pregunta: Pregunta del usuario
        contexto_sgc: Datos del SGC para incluir en el contexto
    """
    
    # Prompt del sistema mejorado con capacidad de datos reales
    system_prompt = """Eres un asistente experto en gestión de riesgo de desastres en Colombia.

Tienes acceso a datos REALES de:
- **SGC (Servicio Geológico Colombiano)**: Sismos recientes, volcanes activos, movimientos en masa
- **IDEAM (Instituto de Hidrología, Meteorología y Estudios Ambientales)**: Clima, pronósticos, alertas meteorológicas, lluvias

Ayudas a las personas con información sobre:
- Fenómenos meteorológicos y pronósticos del clima
- Sismos, volcanes y actividad geológica  
- Riesgos de deslizamientos y movimientos en masa
- Alertas meteorológicas y geológicas
- Preparación para emergencias y planes de contingencia

Cuando te proporcionen datos del SGC o IDEAM en el contexto, úsalos para dar respuestas actualizadas y precisas.

Responde de forma clara, concisa y práctica en español colombiano."""

    messages = [{"role": "system", "content": system_prompt}]
    
    # Agregar contexto del SGC si existe
    if contexto_sgc:
        messages.append({
            "role": "system",
            "content": f"DATOS ACTUALES DEL SGC:\n\n{contexto_sgc}"
        })
    
    messages.append({"role": "user", "content": pregunta})
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500,
        "top_p": 1,
        "stream": False
    }
    
    print("🤔 Consultando a Groq AI...\n")
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def detectar_consulta_sgc(pregunta):
    """
    Detecta si la pregunta requiere datos del SGC o IDEAM
    
    Returns:
        tuple: (requiere_datos, tipo_dato, fuente)
    """
    pregunta_lower = pregunta.lower()
    
    # Palabras clave para sismos (SGC)
    if any(palabra in pregunta_lower for palabra in ['sismo', 'temblor', 'terremoto', 'últimos sismos']):
        return True, 'sismos', 'SGC'
    
    # Palabras clave para volcanes (SGC)
    if any(palabra in pregunta_lower for palabra in ['volcán', 'volcan', 'erupción', 'alerta volcánica', 'nevado del ruiz']):
        return True, 'volcanes', 'SGC'
    
    # Palabras clave para movimientos en masa (SGC)
    if any(palabra in pregunta_lower for palabra in ['deslizamiento', 'derrumbe', 'remoción en masa', 'movimiento en masa', 'susceptibilidad']):
        return True, 'movimientos', 'SGC'
    
    # Palabras clave para clima y pronóstico (IDEAM)
    if any(palabra in pregunta_lower for palabra in ['clima', 'pronóstico', 'temperatura', 'tiempo', 'hace frío', 'hace calor']):
        # Detectar si menciona una ciudad específica
        ciudades = ['bogotá', 'bogota', 'medellín', 'medellin', 'cali', 'barranquilla', 'cartagena', 
                    'bucaramanga', 'manizales', 'pereira', 'cúcuta', 'cucuta', 'ibagué', 'ibague']
        for ciudad in ciudades:
            if ciudad in pregunta_lower:
                return True, ('pronostico', ciudad), 'IDEAM'
        return True, 'clima_general', 'IDEAM'
    
    # Palabras clave para lluvias (IDEAM)
    if any(palabra in pregunta_lower for palabra in ['lluvia', 'lluvias', 'precipitación', 'precipitacion', 'aguacero']):
        return True, 'lluvias', 'IDEAM'
    
    # Palabras clave para alertas (IDEAM)
    if any(palabra in pregunta_lower for palabra in ['alerta meteorológica', 'alerta clima', 'alertas ideam']):
        return True, 'alertas_ideam', 'IDEAM'
    
    return False, None, None


def obtener_datos_sgc(tipo_dato, fuente):
    """Obtiene datos del SGC o IDEAM según el tipo solicitado"""
    if fuente == 'SGC':
        if tipo_dato == 'sismos':
            datos = sgc_client.obtener_sismos_recientes()
            return formatear_info_sismos(datos)
        
        elif tipo_dato == 'volcanes':
            datos = sgc_client.obtener_volcanes_activos()
            return formatear_info_volcanes(datos)
        
        elif tipo_dato == 'movimientos':
            datos = sgc_client.obtener_info_movimientos_masa()
            return formatear_info_movimientos(datos)
    
    elif fuente == 'IDEAM':
        if isinstance(tipo_dato, tuple) and tipo_dato[0] == 'pronostico':
            ciudad = tipo_dato[1]
            datos = ideam_client.obtener_pronostico_ciudad(ciudad)
            return formatear_pronostico(datos)
        
        elif tipo_dato == 'lluvias':
            datos = ideam_client.obtener_info_lluvias()
            return formatear_info_lluvias(datos)
        
        elif tipo_dato == 'alertas_ideam':
            datos = ideam_client.obtener_alertas_activas()
            return formatear_alertas(datos)
        
        elif tipo_dato == 'clima_general':
            return "Para pronóstico del clima, especifica una ciudad (ej: '¿Cómo está el clima en Bogotá?')"
    
    return None


def guardar_en_historial(pregunta, respuesta):
    """Guarda la conversación en el historial"""
    historial = cargar_datos(HISTORIAL_FILE, [])
    
    nueva_entrada = {
        "id": len(historial) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pregunta": pregunta,
        "respuesta": respuesta
    }
    
    historial.append(nueva_entrada)
    guardar_datos(HISTORIAL_FILE, historial)


def actualizar_estadisticas(pregunta):
    """Actualiza las estadísticas de uso"""
    stats = cargar_datos(ESTADISTICAS_FILE, {
        "total_preguntas": 0,
        "primera_consulta": None,
        "ultima_consulta": None,
        "temas": {},
        "consultas_sgc": 0
    })
    
    stats["total_preguntas"] += 1
    stats["ultima_consulta"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not stats["primera_consulta"]:
        stats["primera_consulta"] = stats["ultima_consulta"]
    
    # Detectar temas
    palabras_clave = {
        "sismos": ["sismo", "terremoto", "temblor"],
        "volcanes": ["volcán", "erupción", "lava"],
        "deslizamientos": ["deslizamiento", "derrumbe", "movimiento en masa"],
        "inundación": ["inundación", "lluvia", "desbordamiento"],
        "emergencia": ["emergencia", "evacuación", "kit", "preparación"]
    }
    
    pregunta_lower = pregunta.lower()
    
    # Detectar si usó datos del SGC
    if detectar_consulta_sgc(pregunta)[0]:
        stats["consultas_sgc"] = stats.get("consultas_sgc", 0) + 1
    
    for tema, keywords in palabras_clave.items():
        if any(kw in pregunta_lower for kw in keywords):
            stats["temas"][tema] = stats["temas"].get(tema, 0) + 1
            break
    
    guardar_datos(ESTADISTICAS_FILE, stats)


def mostrar_historial():
    """Muestra el historial de conversaciones"""
    historial = cargar_datos(HISTORIAL_FILE, [])
    
    if not historial:
        print("\n📭 No hay conversaciones guardadas aún.\n")
        return
    
    print("\n" + "=" * 75)
    print("📚 HISTORIAL DE CONVERSACIONES")
    print("=" * 75)
    print(f"\nTotal de conversaciones: {len(historial)}\n")
    
    ultimas = historial[-10:] if len(historial) > 10 else historial
    
    for entrada in reversed(ultimas):
        print(f"[{entrada['id']}] {entrada['timestamp']}")
        print(f"❓ {entrada['pregunta'][:60]}{'...' if len(entrada['pregunta']) > 60 else ''}")
        print(f"🤖 {entrada['respuesta'][:100]}{'...' if len(entrada['respuesta']) > 100 else ''}")
        print("-" * 75)
    
    if len(historial) > 10:
        print(f"\n💡 Mostrando las últimas 10 de {len(historial)} conversaciones")
    print()


def mostrar_estadisticas():
    """Muestra estadísticas de uso"""
    stats = cargar_datos(ESTADISTICAS_FILE, None)
    
    if not stats or stats["total_preguntas"] == 0:
        print("\n📊 No hay estadísticas disponibles aún.\n")
        return
    
    print("\n" + "=" * 75)
    print("📊 ESTADÍSTICAS DE USO")
    print("=" * 75)
    print(f"\n📈 Total de preguntas: {stats['total_preguntas']}")
    print(f"🌐 Consultas con datos SGC: {stats.get('consultas_sgc', 0)}")
    print(f"📅 Primera consulta: {stats['primera_consulta']}")
    print(f"🕐 Última consulta: {stats['ultima_consulta']}")
    
    if stats["temas"]:
        print("\n🏷️ Temas más consultados:")
        temas_ordenados = sorted(stats["temas"].items(), key=lambda x: x[1], reverse=True)
        for tema, cantidad in temas_ordenados:
            print(f"   • {tema.capitalize()}: {cantidad} veces")
    
    print("\n" + "=" * 75 + "\n")


def guardar_favorito(id_conversacion):
    """Guarda una conversación como favorita"""
    historial = cargar_datos(HISTORIAL_FILE, [])
    favoritos = cargar_datos(FAVORITOS_FILE, [])
    
    conversacion = next((c for c in historial if c['id'] == id_conversacion), None)
    
    if not conversacion:
        print(f"\n❌ No se encontró la conversación #{id_conversacion}\n")
        return
    
    if any(f['id'] == id_conversacion for f in favoritos):
        print(f"\n⚠️ La conversación #{id_conversacion} ya está en favoritos\n")
        return
    
    favoritos.append(conversacion)
    if guardar_datos(FAVORITOS_FILE, favoritos):
        print(f"\n⭐ Conversación #{id_conversacion} guardada en favoritos\n")


def mostrar_favoritos():
    """Muestra las conversaciones favoritas"""
    favoritos = cargar_datos(FAVORITOS_FILE, [])
    
    if not favoritos:
        print("\n⭐ No tienes favoritos guardados aún.\n")
        return
    
    print("\n" + "=" * 75)
    print("⭐ CONVERSACIONES FAVORITAS")
    print("=" * 75)
    print(f"\nTotal de favoritos: {len(favoritos)}\n")
    
    for fav in favoritos:
        print(f"[{fav['id']}] {fav['timestamp']}")
        print(f"❓ Pregunta: {fav['pregunta']}")
        print(f"\n🤖 Respuesta:\n{fav['respuesta']}\n")
        print("=" * 75)
    
    print()


def mostrar_ayuda():
    """Muestra la ayuda del sistema"""
    print("\n" + "=" * 75)
    print("📚 GUÍA DE USO DEL AGENTE")
    print("=" * 75)
    
    print("\n🎯 COMANDOS DISPONIBLES:")
    print("   • Tu pregunta normal     - Consultar al agente")
    print("\n   📊 SGC (Servicio Geológico):")
    print("   • sgc sismos            - Ver sismos recientes")
    print("   • sgc volcanes          - Ver volcanes activos")
    print("   • sgc movimientos       - Info movimientos en masa")
    print("\n   🌦️ IDEAM (Clima y Meteorología):")
    print("   • ideam clima [ciudad]  - Pronóstico de una ciudad")
    print("   • ideam alertas         - Alertas meteorológicas")
    print("   • ideam lluvias         - Info sobre lluvias")
    print("\n   🗺️ MAPAS (Visualización Geográfica):")
    print("   • mapa sismos           - Generar mapa de sismos")
    print("   • mapa volcanes         - Generar mapa de volcanes")
    print("   • mapa estaciones       - Generar mapa de estaciones")
    print("   • mapa completo         - Mapa integrado (todo)")
    print("   • estado mapas          - Ver estado del sistema")
    print("\n   📚 Gestión:")
    print("   • historial             - Ver conversaciones anteriores")
    print("   • stats                 - Ver estadísticas de uso")
    print("   • favoritos             - Ver conversaciones guardadas")
    print("   • favorito #N           - Guardar conversación N")
    print("   • ayuda                 - Mostrar esta ayuda")
    print("   • salir                 - Cerrar el programa")
    
    print("\n💡 EJEMPLOS DE PREGUNTAS:")
    print("   🌍 Sismos:")
    print("   • ¿Cuáles fueron los últimos sismos en Colombia?")
    print("   🌋 Volcanes:")
    print("   • ¿Qué volcanes están en alerta naranja?")
    print("   🏔️ Deslizamientos:")
    print("   • ¿Cuál es el riesgo de deslizamiento en Antioquia?")
    print("   🌦️ Clima:")
    print("   • ¿Cómo está el clima en Bogotá?")
    print("   • ¿Cuándo es temporada de lluvias en Colombia?")
    print("   🎒 Emergencias:")
    print("   • ¿Cómo preparar un kit de emergencia?")
    print("   • ¿Qué hacer durante un terremoto?")
    
    print("\n🌐 DATOS EN TIEMPO REAL:")
    print("   El agente consulta automáticamente cuando preguntas sobre:")
    print("   • Sismos y terremotos → SGC")
    print("   • Volcanes y erupciones → SGC")
    print("   • Deslizamientos y movimientos en masa → SGC")
    print("   • Clima y pronósticos → IDEAM")
    print("   • Lluvias y alertas meteorológicas → IDEAM")
    
    print("\n" + "=" * 75 + "\n")


# Función principal
if __name__ == "__main__":
    print("=" * 75)
    print("🤖 AGENTE DE IA - GESTIÓN DE RIESGO COLOMBIA (SGC + IDEAM + MAPAS)")
    print("    Powered by Groq + SGC + IDEAM + GeoVisualization ⚡🌋🌦️🗺️")
    print("=" * 75)
    print("\n✅ Funcionalidades:")
    print("   🌍 Datos del SGC (sismos, volcanes, amenazas geológicas)")
    print("   🌦️ Datos del IDEAM (clima, pronósticos, lluvias, alertas)")
    print("   🗺️ Mapas interactivos (sismos, volcanes, estaciones)")
    print("   📚 Historial de conversaciones")
    print("   📊 Estadísticas de uso")
    print("   ⭐ Guardar favoritos")
    
    # Mostrar estado de mapas
    if MAPAS_DISPONIBLES:
        print("   ✅ Sistema de mapas: ACTIVO")
    else:
        print("   ⚠️ Sistema de mapas: NO DISPONIBLE (instalar geopandas)")
    
    print("\n💡 Escribe 'ayuda' para ver todos los comandos\n")
    
    while True:
        pregunta = input("💬 Tu pregunta o comando: ")
        
        # Comandos especiales
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 ¡Hasta pronto!\n")
            break
        
        if pregunta.lower() in ['ayuda', 'help', '?']:
            mostrar_ayuda()
            continue
        
        if pregunta.lower() == 'historial':
            mostrar_historial()
            continue
        
        if pregunta.lower() in ['stats', 'estadisticas', 'estadísticas']:
            mostrar_estadisticas()
            continue
        
        if pregunta.lower() == 'favoritos':
            mostrar_favoritos()
            continue
        
        if pregunta.lower().startswith('favorito '):
            try:
                id_conv = int(pregunta.split()[1].replace('#', ''))
                guardar_favorito(id_conv)
            except:
                print("\n❌ Uso: favorito #N (ejemplo: favorito #5)\n")
            continue
        
        # Comandos SGC directos
        if pregunta.lower() == 'sgc sismos':
            print("\n🌍 Obteniendo datos de sismos del SGC...\n")
            datos = sgc_client.obtener_sismos_recientes()
            print(formatear_info_sismos(datos))
            print()
            continue
        
        if pregunta.lower() == 'sgc volcanes':
            print("\n🌋 Obteniendo datos de volcanes del SGC...\n")
            datos = sgc_client.obtener_volcanes_activos()
            print(formatear_info_volcanes(datos))
            print()
            continue
        
        if pregunta.lower() == 'sgc movimientos':
            print("\n🏔️ Obteniendo info de movimientos en masa...\n")
            datos = sgc_client.obtener_info_movimientos_masa()
            print(formatear_info_movimientos(datos))
            print()
            continue
        
        # Comandos IDEAM directos
        if pregunta.lower().startswith('ideam clima '):
            ciudad = pregunta[12:].strip()
            print(f"\n🌤️ Obteniendo pronóstico de {ciudad}...\n")
            datos = ideam_client.obtener_pronostico_ciudad(ciudad)
            print(formatear_pronostico(datos))
            print()
            continue
        
        if pregunta.lower() == 'ideam alertas':
            print("\n🚨 Obteniendo alertas meteorológicas del IDEAM...\n")
            datos = ideam_client.obtener_alertas_activas()
            print(formatear_alertas(datos))
            print()
            continue
        
        if pregunta.lower() == 'ideam lluvias':
            print("\n🌧️ Obteniendo información sobre lluvias...\n")
            datos = ideam_client.obtener_info_lluvias()
            print(formatear_info_lluvias(datos))
            print()
            continue
        
        # Comandos de MAPAS
        if pregunta.lower() == 'mapa sismos':
            if MAPAS_DISPONIBLES:
                print("\n🗺️ Generando mapa de sismos...\n")
                resultado = generar_mapa_sismos_sgc()
                print(resultado)
            else:
                print("\n⚠️ Sistema de mapas no disponible")
                print("Instala: pip install geopandas matplotlib matplotlib-scalebar\n")
            continue
        
        if pregunta.lower() == 'mapa volcanes':
            if MAPAS_DISPONIBLES:
                print("\n🗺️ Generando mapa de volcanes...\n")
                resultado = generar_mapa_volcanes_sgc()
                print(resultado)
            else:
                print("\n⚠️ Sistema de mapas no disponible\n")
            continue
        
        if pregunta.lower().startswith('mapa estaciones'):
            if MAPAS_DISPONIBLES:
                partes = pregunta.split()
                depto = partes[2] if len(partes) > 2 else None
                print(f"\n🗺️ Generando mapa de estaciones{' - ' + depto if depto else ''}...\n")
                resultado = generar_mapa_estaciones_ideam(depto)
                print(resultado)
            else:
                print("\n⚠️ Sistema de mapas no disponible\n")
            continue
        
        if pregunta.lower() == 'mapa completo':
            if MAPAS_DISPONIBLES:
                print("\n🗺️ Generando mapa integrado...\n")
                resultado = generar_mapa_integrado()
                print(resultado)
            else:
                print("\n⚠️ Sistema de mapas no disponible\n")
            continue
        
        if pregunta.lower() == 'estado mapas':
            resultado = verificar_sistema_mapas()
            print(resultado)
            continue
        
        if not pregunta.strip():
            continue
        
        try:
            # Detectar si necesita datos del SGC o IDEAM
            requiere_datos, tipo_dato, fuente = detectar_consulta_sgc(pregunta)
            contexto_sgc = None
            
            if requiere_datos:
                print(f"🌐 Consultando datos de {fuente} ({tipo_dato if not isinstance(tipo_dato, tuple) else tipo_dato[0]})...\n")
                contexto_sgc = obtener_datos_sgc(tipo_dato, fuente)
            
            # Obtener respuesta del agente
            respuesta = chat_con_agente(pregunta, contexto_sgc)
            
            # Mostrar respuesta
            print(f"\n🤖 Respuesta:\n")
            print(f"{respuesta}\n")
            print("-" * 75 + "\n")
            
            # Guardar en historial y actualizar stats
            guardar_en_historial(pregunta, respuesta)
            actualizar_estadisticas(pregunta)
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}\n")
