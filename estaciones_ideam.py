"""
Módulo de Estaciones Meteorológicas del IDEAM
Consulta catálogo de estaciones y datos históricos
"""
from datetime import datetime
import json


class EstacionesIDEAM:
    """Cliente para consultar estaciones meteorológicas del IDEAM"""
    
    def __init__(self):
        self.dhime_url = "http://dhime.ideam.gov.co/atencionciudadano/"
        self.datos_abiertos = "https://www.datos.gov.co"
        self.catalogo_url = f"{self.datos_abiertos}/Ambiente-y-Desarrollo-Sostenible/Cat-logo-Nacional-de-Estaciones-del-IDEAM/hp9r-jxuu"
        
        # Base de datos local de estaciones principales
        # (En producción esto vendría de la API o BD)
        self.estaciones_principales = self._cargar_estaciones_principales()
    
    def _cargar_estaciones_principales(self):
        """Carga catálogo de estaciones principales por departamento"""
        return {
            "cundinamarca": [
                {
                    "codigo": "21205790",
                    "nombre": "Aeropuerto El Dorado",
                    "municipio": "Bogotá",
                    "tipo": "Climatológica Principal",
                    "latitud": 4.701594,
                    "longitud": -74.146947,
                    "altitud": 2547,
                    "variables": ["Temperatura", "Precipitación", "Humedad", "Viento", "Presión"]
                },
                {
                    "codigo": "21201200",
                    "nombre": "Guaymaral",
                    "municipio": "Bogotá",
                    "tipo": "Climatológica Ordinaria",
                    "latitud": 4.812778,
                    "longitud": -74.046389,
                    "altitud": 2548,
                    "variables": ["Temperatura", "Precipitación"]
                },
                {
                    "codigo": "21205010",
                    "nombre": "Tibaitatá",
                    "municipio": "Mosquera",
                    "tipo": "Agrometeorológica",
                    "latitud": 4.693611,
                    "longitud": -74.206667,
                    "altitud": 2543,
                    "variables": ["Temperatura", "Precipitación", "Radiación Solar", "Evaporación"]
                }
            ],
            "antioquia": [
                {
                    "codigo": "27015070",
                    "nombre": "Olaya Herrera",
                    "municipio": "Medellín",
                    "tipo": "Climatológica Principal",
                    "latitud": 6.220556,
                    "longitud": -75.590556,
                    "altitud": 1490,
                    "variables": ["Temperatura", "Precipitación", "Humedad", "Viento"]
                }
            ],
            "valle_del_cauca": [
                {
                    "codigo": "26235010",
                    "nombre": "Alfonso Bonilla Aragón",
                    "municipio": "Palmira",
                    "tipo": "Climatológica Principal",
                    "latitud": 3.543056,
                    "longitud": -76.381667,
                    "altitud": 966,
                    "variables": ["Temperatura", "Precipitación", "Humedad", "Viento"]
                }
            ]
        }
    
    def buscar_estaciones_por_departamento(self, departamento):
        """
        Busca estaciones por departamento
        
        Args:
            departamento: Nombre del departamento
            
        Returns:
            Lista de estaciones
        """
        dept_key = departamento.lower().replace(" ", "_")
        estaciones = self.estaciones_principales.get(dept_key, [])
        
        if not estaciones:
            return {
                "departamento": departamento,
                "total_estaciones": 0,
                "estaciones": [],
                "mensaje": f"No hay estaciones cargadas para {departamento} en este momento",
                "nota": f"Consulta el catálogo completo en: {self.catalogo_url}",
                "departamentos_disponibles": list(self.estaciones_principales.keys())
            }
        
        return {
            "departamento": departamento,
            "total_estaciones": len(estaciones),
            "estaciones": estaciones,
            "fuente": "IDEAM - Catálogo Nacional de Estaciones",
            "url_catalogo": self.catalogo_url
        }
    
    def buscar_estacion_por_codigo(self, codigo):
        """
        Busca una estación específica por código
        
        Args:
            codigo: Código de la estación
            
        Returns:
            Información de la estación
        """
        # Buscar en todas las estaciones
        for dept, estaciones in self.estaciones_principales.items():
            for estacion in estaciones:
                if estacion["codigo"] == codigo:
                    return {
                        "encontrada": True,
                        "estacion": estacion,
                        "departamento": dept
                    }
        
        return {
            "encontrada": False,
            "mensaje": f"No se encontró la estación con código {codigo}",
            "nota": "Verifica el código o consulta el catálogo en datos.gov.co"
        }
    
    def buscar_estacion_cercana(self, municipio):
        """
        Busca estación cercana a un municipio
        
        Args:
            municipio: Nombre del municipio
            
        Returns:
            Estación más cercana
        """
        municipio_lower = municipio.lower()
        
        # Buscar coincidencia directa
        for dept, estaciones in self.estaciones_principales.items():
            for estacion in estaciones:
                if municipio_lower in estacion["municipio"].lower():
                    return {
                        "encontrada": True,
                        "estacion": estacion,
                        "departamento": dept,
                        "distancia": "En el municipio"
                    }
        
        return {
            "encontrada": False,
            "mensaje": f"No se encontró estación en {municipio}",
            "recomendacion": "Prueba buscando por departamento o consulta el catálogo completo",
            "url": self.catalogo_url
        }
    
    def obtener_info_datos_historicos(self, codigo_estacion=None):
        """
        Información sobre cómo acceder a datos históricos
        
        Args:
            codigo_estacion: Código de estación específica (opcional)
            
        Returns:
            Guía de acceso a datos históricos
        """
        info = {
            "titulo": "Acceso a Datos Históricos - IDEAM",
            "metodos_acceso": [
                {
                    "nombre": "Portal DHIME (Recomendado)",
                    "url": self.dhime_url,
                    "descripcion": "Sistema web de consulta y descarga",
                    "pasos": [
                        "1. Ingresa a http://dhime.ideam.gov.co/atencionciudadano/",
                        "2. Navega el mapa para seleccionar estación",
                        "3. Selecciona variable (temp, precipitación, etc)",
                        "4. Define rango de fechas",
                        "5. Descarga datos en CSV o Excel"
                    ],
                    "formatos": ["CSV", "Excel", "TXT"],
                    "requiere_registro": False
                },
                {
                    "nombre": "Datos Abiertos Colombia",
                    "url": "https://www.datos.gov.co",
                    "descripcion": "Datasets públicos descargables",
                    "formatos": ["CSV", "JSON", "XML"],
                    "requiere_registro": False
                },
                {
                    "nombre": "Solicitud Formal",
                    "descripcion": "Para datos específicos o personalizados",
                    "contacto": "solicitudes@ideam.gov.co",
                    "nota": "Puede tener costo según volumen de datos"
                }
            ],
            "variables_disponibles": [
                "Precipitación (mm)",
                "Temperatura (°C)",
                "Humedad Relativa (%)",
                "Velocidad del Viento (m/s)",
                "Dirección del Viento",
                "Presión Atmosférica (hPa)",
                "Radiación Solar",
                "Evaporación",
                "Brillo Solar"
            ],
            "periodo_disponible": "Varía por estación (algunas desde 1950s)",
            "frecuencia_datos": ["Horaria", "Diaria", "Mensual", "Anual"],
            "notas_importantes": [
                "Datos sujetos a validación y control de calidad",
                "Algunas estaciones tienen datos incompletos",
                "Verificar disponibilidad por estación y periodo",
                "Citar fuente: IDEAM en publicaciones"
            ]
        }
        
        if codigo_estacion:
            estacion_info = self.buscar_estacion_por_codigo(codigo_estacion)
            if estacion_info.get("encontrada"):
                info["estacion_consultada"] = estacion_info["estacion"]
        
        return info
    
    def obtener_tipos_estaciones(self):
        """
        Información sobre tipos de estaciones
        
        Returns:
            Dict con tipos de estaciones
        """
        return {
            "tipos_estaciones": [
                {
                    "tipo": "Climatológica Principal (CP)",
                    "descripcion": "Medición completa de variables climáticas",
                    "variables": "Todas las meteorológicas",
                    "frecuencia": "Horaria o sub-horaria",
                    "importancia": "Alta - Datos de referencia nacional"
                },
                {
                    "tipo": "Climatológica Ordinaria (CO)",
                    "descripcion": "Medición de variables básicas",
                    "variables": "Temperatura, precipitación, viento",
                    "frecuencia": "Diaria",
                    "importancia": "Media - Complementan la red"
                },
                {
                    "tipo": "Pluviométrica (PM)",
                    "descripcion": "Solo precipitación",
                    "variables": "Precipitación",
                    "frecuencia": "Diaria",
                    "importancia": "Específica - Monitoreo de lluvias"
                },
                {
                    "tipo": "Agrometeorológica (AM)",
                    "descripcion": "Variables para agricultura",
                    "variables": "Temp, lluvia, radiación, evaporación",
                    "frecuencia": "Diaria/horaria",
                    "importancia": "Específica - Sector agrícola"
                },
                {
                    "tipo": "Hidrológica (HG)",
                    "descripcion": "Niveles y caudales de ríos",
                    "variables": "Nivel, caudal, sedimentos",
                    "frecuencia": "Variable",
                    "importancia": "Alta - Gestión del agua"
                }
            ],
            "total_estaciones_ideam": "~3,500 estaciones en todo el país",
            "cobertura": "Todo el territorio nacional",
            "fuente": "IDEAM - Red Hidrometeorológica Nacional"
        }


def formatear_estaciones_departamento(resultado):
    """Formatea resultado de búsqueda por departamento"""
    if resultado["total_estaciones"] == 0:
        return f"⚠️ {resultado['mensaje']}\n\n💡 {resultado['nota']}"
    
    msg = f"📊 **Estaciones en {resultado['departamento'].title()}**\n\n"
    msg += f"Total de estaciones: {resultado['total_estaciones']}\n\n"
    
    for estacion in resultado['estaciones']:
        msg += f"🔹 **{estacion['nombre']}** (Código: {estacion['codigo']})\n"
        msg += f"   📍 Municipio: {estacion['municipio']}\n"
        msg += f"   📏 Altitud: {estacion['altitud']} msnm\n"
        msg += f"   🎯 Tipo: {estacion['tipo']}\n"
        msg += f"   📈 Variables: {', '.join(estacion['variables'][:3])}\n\n"
    
    msg += f"🌐 Catálogo completo: {resultado['url_catalogo']}"
    
    return msg


def formatear_info_datos_historicos(info):
    """Formatea guía de datos históricos"""
    msg = f"📚 **{info['titulo']}**\n\n"
    
    msg += "**Métodos de acceso:**\n\n"
    for metodo in info['metodos_acceso'][:2]:
        msg += f"🔸 **{metodo['nombre']}**\n"
        msg += f"   {metodo['descripcion']}\n"
        msg += f"   🌐 {metodo['url']}\n"
        if 'pasos' in metodo:
            msg += f"   📝 Pasos básicos:\n"
            for paso in metodo['pasos'][:3]:
                msg += f"      {paso}\n"
        msg += "\n"
    
    msg += f"**Variables disponibles:**\n"
    msg += f"{', '.join(info['variables_disponibles'][:5])}, y más.\n\n"
    
    msg += "**Notas importantes:**\n"
    for nota in info['notas_importantes'][:3]:
        msg += f"• {nota}\n"
    
    return msg


def formatear_tipos_estaciones(info):
    """Formatea información de tipos de estaciones"""
    msg = f"🏢 **Tipos de Estaciones Meteorológicas - IDEAM**\n\n"
    
    for tipo in info['tipos_estaciones'][:4]:
        msg += f"📍 **{tipo['tipo']}**\n"
        msg += f"   {tipo['descripcion']}\n"
        msg += f"   Variables: {tipo['variables']}\n\n"
    
    msg += f"📊 **Total**: {info['total_estaciones_ideam']}\n"
    msg += f"🗺️ **Cobertura**: {info['cobertura']}"
    
    return msg


# Instancia global
estaciones_ideam = EstacionesIDEAM()
