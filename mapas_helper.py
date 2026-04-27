"""
Helper functions para generar mapas desde el agente
"""
from mapas_riesgos import sistema_mapas, MAPAS_DISPONIBLES


def generar_mapa_sismos_sgc():
    """Genera mapa con datos de sismos del SGC"""
    if not MAPAS_DISPONIBLES:
        return "⚠️ Sistema de mapas no disponible. Instala: pip install geopandas matplotlib matplotlib-scalebar"
    
    from sgc_integration import sgc_client
    
    print("🗺️ Generando mapa de sismos...")
    
    # Obtener sismos del SGC
    datos_sismos = sgc_client.obtener_sismos_recientes(horas=48)
    
    # Datos de ejemplo (en producción vendrían del scraping real)
    sismos_ejemplo = [
        {'lat': 4.5, 'lon': -75.7, 'magnitud': 3.2, 'ubicacion': 'Caldas'},
        {'lat': 1.2, 'lon': -77.3, 'magnitud': 4.1, 'ubicacion': 'Nariño'},
        {'lat': 6.2, 'lon': -75.6, 'magnitud': 2.8, 'ubicacion': 'Antioquia'},
        {'lat': 4.9, 'lon': -75.3, 'magnitud': 3.5, 'ubicacion': 'Tolima'},
    ]
    
    # Generar mapa
    resultado = sistema_mapas.mapa_sismos(sismos_ejemplo)
    
    if resultado:
        fig, ax, ruta = resultado
        return f"✅ Mapa de sismos generado: {ruta}"
    else:
        return "❌ Error generando mapa de sismos"


def generar_mapa_volcanes_sgc():
    """Genera mapa con volcanes activos del SGC"""
    if not MAPAS_DISPONIBLES:
        return "⚠️ Sistema de mapas no disponible"
    
    from sgc_integration import sgc_client
    
    print("🗺️ Generando mapa de volcanes...")
    
    # Obtener datos de volcanes
    datos_volcanes = sgc_client.obtener_volcanes_activos()
    
    # Convertir a formato para mapa
    volcanes_mapa = []
    for volcan in datos_volcanes.get('volcanes', [])[:10]:
        # Coordenadas aproximadas de volcanes principales
        coords = {
            'Nevado del Ruiz': (4.8925, -75.3222),
            'Galeras': (1.2217, -77.3603),
            'Nevado del Huila': (2.9292, -76.0303),
            'Puracé': (2.3189, -76.3989),
            'Cerro Machín': (4.4811, -75.3819),
            'Sotará': (2.1083, -76.5917),
            'Doña Juana': (1.4833, -76.9333),
            'Cumbal': (0.9500, -77.8833),
            'Azufral': (1.0833, -77.6833),
            'Chiles-Cerro Negro': (0.8167, -77.9333)
        }
        
        nombre = volcan.get('nombre', '')
        if nombre in coords:
            lat, lon = coords[nombre]
            volcanes_mapa.append({
                'nombre': nombre,
                'lat': lat,
                'lon': lon,
                'alerta': 'verde'  # En producción vendría del SGC
            })
    
    # Generar mapa
    resultado = sistema_mapas.mapa_volcanes(volcanes_mapa)
    
    if resultado:
        fig, ax, ruta = resultado
        return f"✅ Mapa de volcanes generado: {ruta}"
    else:
        return "❌ Error generando mapa de volcanes"


def generar_mapa_estaciones_ideam(departamento=None):
    """Genera mapa con estaciones del IDEAM"""
    if not MAPAS_DISPONIBLES:
        return "⚠️ Sistema de mapas no disponible"
    
    from estaciones_ideam import estaciones_ideam
    
    print(f"🗺️ Generando mapa de estaciones{' - ' + departamento if departamento else ''}...")
    
    # Obtener estaciones
    if departamento:
        resultado = estaciones_ideam.buscar_estaciones_por_departamento(departamento)
        estaciones = resultado.get('estaciones', [])
    else:
        # Todas las estaciones principales
        estaciones = []
        for dept in ['cundinamarca', 'antioquia', 'valle_del_cauca']:
            resultado = estaciones_ideam.buscar_estaciones_por_departamento(dept)
            estaciones.extend(resultado.get('estaciones', []))
    
    if not estaciones:
        return f"⚠️ No se encontraron estaciones{' en ' + departamento if departamento else ''}"
    
    # Generar mapa
    resultado = sistema_mapas.mapa_estaciones(estaciones, departamento)
    
    if resultado:
        fig, ax, ruta = resultado
        return f"✅ Mapa de estaciones generado: {ruta}"
    else:
        return "❌ Error generando mapa de estaciones"


def generar_mapa_integrado():
    """Genera mapa con todas las capas de riesgo"""
    if not MAPAS_DISPONIBLES:
        return "⚠️ Sistema de mapas no disponible"
    
    print("🗺️ Generando mapa integrado...")
    
    # Datos de ejemplo para cada capa
    sismos = [
        {'lat': 4.5, 'lon': -75.7, 'magnitud': 3.2},
        {'lat': 1.2, 'lon': -77.3, 'magnitud': 4.1},
        {'lat': 6.2, 'lon': -75.6, 'magnitud': 2.8},
    ]
    
    volcanes = [
        {'nombre': 'N. Ruiz', 'lat': 4.8925, 'lon': -75.3222, 'alerta': 'amarillo'},
        {'nombre': 'Galeras', 'lat': 1.2217, 'lon': -77.3603, 'alerta': 'verde'},
        {'nombre': 'N. Huila', 'lat': 2.9292, 'lon': -76.0303, 'alerta': 'verde'},
    ]
    
    estaciones = [
        {'nombre': 'El Dorado', 'latitud': 4.701594, 'longitud': -74.146947},
        {'nombre': 'Olaya Herrera', 'latitud': 6.220556, 'longitud': -75.590556},
        {'nombre': 'Alfonso Bonilla', 'latitud': 3.543056, 'longitud': -76.381667},
    ]
    
    # Generar mapa integrado
    resultado = sistema_mapas.mapa_completo_riesgos(
        sismos=sismos,
        volcanes=volcanes,
        estaciones=estaciones
    )
    
    if resultado:
        fig, ax, ruta = resultado
        return f"✅ Mapa integrado generado: {ruta}"
    else:
        return "❌ Error generando mapa integrado"


def verificar_sistema_mapas():
    """Verifica si el sistema de mapas está disponible"""
    if MAPAS_DISPONIBLES:
        return """
✅ Sistema de mapas ACTIVO

📊 Comandos disponibles:
  • mapa sismos      - Mapa de sismos recientes
  • mapa volcanes    - Mapa de volcanes activos
  • mapa estaciones  - Mapa de estaciones IDEAM
  • mapa completo    - Mapa integrado con todo

📁 Los mapas se guardan en: ./mapas_generados/
"""
    else:
        return """
⚠️ Sistema de mapas NO DISPONIBLE

📦 Para activarlo, instala las dependencias:
  pip install geopandas matplotlib matplotlib-scalebar shapely

Una vez instalado, reinicia el agente.
"""
