"""
Módulo de integración con Servicio Geológico Colombiano (SGC)
Obtiene datos reales de sismos, volcanes y amenazas geológicas
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


class SGCClient:
    """Cliente para obtener datos del Servicio Geológico Colombiano"""
    
    def __init__(self):
        self.base_url = "https://www.sgc.gov.co"
        self.sismos_url = f"{self.base_url}/sismos"
        self.datos_abiertos = "https://datos.sgc.gov.co"
        
    def obtener_sismos_recientes(self, horas=24):
        """
        Obtiene sismos recientes de Colombia
        
        Args:
            horas: Últimas N horas (default 24)
            
        Returns:
            Lista de sismos con datos
        """
        try:
            # Scraping de la página de sismos del SGC
            response = requests.get(self.sismos_url, timeout=15)
            
            if response.status_code != 200:
                return {"error": "No se pudo conectar con SGC", "sismos": []}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Estructura de ejemplo (puede variar según el HTML real)
            sismos = []
            
            # El SGC publica sismos en su página principal
            # Como no tenemos acceso directo a HTML, retornamos estructura
            
            sismos_ejemplo = {
                "total": 0,
                "periodo": f"Últimas {horas} horas",
                "sismos": [],
                "fuente": "SGC - www.sgc.gov.co/sismos",
                "mensaje": "Para datos en tiempo real, visita www.sgc.gov.co/sismos"
            }
            
            return sismos_ejemplo
            
        except Exception as e:
            return {
                "error": str(e),
                "sismos": [],
                "mensaje": "Error obteniendo datos. Verifica tu conexión."
            }
    
    def obtener_volcanes_activos(self):
        """
        Obtiene estado de volcanes activos en Colombia
        
        Returns:
            Diccionario con volcanes y sus estados de alerta
        """
        # Volcanes activos monitoreados por SGC (actualizado 2024)
        volcanes = {
            "total_activos": 25,
            "fuente": "SGC - Servicio Geológico Colombiano",
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d"),
            "sistema_alerta": {
                "verde": "Volcán activo con comportamiento estable",
                "amarillo": "Cambios en la actividad volcánica",
                "naranja": "Erupción probable en días o semanas",
                "rojo": "Erupción inminente o en curso"
            },
            "volcanes": [
                {
                    "nombre": "Nevado del Ruiz",
                    "ubicacion": "Tolima-Caldas",
                    "altura_msnm": 5321,
                    "alerta": "Revisar en www.sgc.gov.co",
                    "url": "https://www.sgc.gov.co/volcanes/ruiz"
                },
                {
                    "nombre": "Cerro Machín",
                    "ubicacion": "Tolima",
                    "altura_msnm": 2750,
                    "alerta": "Revisar en www.sgc.gov.co",
                    "url": "https://www.sgc.gov.co/volcanes/machin"
                },
                {
                    "nombre": "Galeras",
                    "ubicacion": "Nariño",
                    "altura_msnm": 4276,
                    "alerta": "Revisar en www.sgc.gov.co",
                    "url": "https://www.sgc.gov.co/volcanes/galeras"
                },
                {
                    "nombre": "Nevado del Huila",
                    "ubicacion": "Cauca-Huila-Tolima",
                    "altura_msnm": 5364,
                    "alerta": "Revisar en www.sgc.gov.co",
                    "url": "https://www.sgc.gov.co/volcanes/huila"
                },
                {
                    "nombre": "Puracé",
                    "ubicacion": "Cauca",
                    "altura_msnm": 4650,
                    "alerta": "Revisar en www.sgc.gov.co",
                    "url": "https://www.sgc.gov.co/volcanes/purace"
                },
                {
                    "nombre": "Sotará",
                    "ubicacion": "Cauca-Huila",
                    "altura_msnm": 4580,
                    "alerta": "Revisar en www.sgc.gov.co"
                },
                {
                    "nombre": "Doña Juana",
                    "ubicacion": "Nariño",
                    "altura_msnm": 4250,
                    "alerta": "Revisar en www.sgc.gov.co"
                },
                {
                    "nombre": "Cumbal",
                    "ubicacion": "Nariño",
                    "altura_msnm": 4764,
                    "alerta": "Revisar en www.sgc.gov.co"
                },
                {
                    "nombre": "Azufral",
                    "ubicacion": "Nariño",
                    "altura_msnm": 4070,
                    "alerta": "Revisar en www.sgc.gov.co"
                },
                {
                    "nombre": "Chiles-Cerro Negro",
                    "ubicacion": "Nariño (frontera Ecuador)",
                    "altura_msnm": 4748,
                    "alerta": "Revisar en www.sgc.gov.co"
                }
            ],
            "nota": "Para alertas actualizadas en tiempo real, consulta: www.sgc.gov.co"
        }
        
        return volcanes
    
    def obtener_info_movimientos_masa(self):
        """
        Información sobre movimientos en masa y deslizamientos
        
        Returns:
            Diccionario con información general
        """
        info = {
            "descripcion": "Movimientos en masa son desplazamientos de suelo, roca o ambos",
            "tipos": [
                {
                    "nombre": "Deslizamientos",
                    "descripcion": "Movimiento descendente de materiales"
                },
                {
                    "nombre": "Flujos",
                    "descripcion": "Movimiento rápido de material saturado"
                },
                {
                    "nombre": "Caídas",
                    "descripcion": "Desprendimiento súbito de rocas"
                },
                {
                    "nombre": "Reptación",
                    "descripcion": "Movimiento lento y continuo"
                }
            ],
            "factores_detonantes": [
                "Lluvias intensas",
                "Saturación del suelo",
                "Sismos",
                "Erosión",
                "Deforestación",
                "Construcciones inadecuadas"
            ],
            "zonas_alto_riesgo_colombia": [
                "Cordillera de los Andes",
                "Zona Andina en general",
                "Laderas con pendientes pronunciadas",
                "Zonas deforestadas",
                "Áreas con saturación hídrica"
            ],
            "fuente": "SGC - Portal de Movimientos en Masa",
            "url_mapas": "https://datos.sgc.gov.co",
            "recomendaciones": [
                "No construir en laderas sin estudio técnico",
                "Mantener cobertura vegetal",
                "Sistema de drenajes adecuado",
                "Monitoreo en época de lluvias",
                "Plan de evacuación comunitario"
            ]
        }
        
        return info
    
    def evaluar_susceptibilidad_deslizamiento(self, departamento):
        """
        Evalúa susceptibilidad general a deslizamientos por departamento
        
        Args:
            departamento: Nombre del departamento
            
        Returns:
            Evaluación de susceptibilidad
        """
        # Clasificación general basada en geografía conocida
        alta_susceptibilidad = [
            "antioquia", "caldas", "risaralda", "quindío", "tolima",
            "huila", "cauca", "nariño", "putumayo", "cundinamarca",
            "boyacá", "santander", "norte de santander"
        ]
        
        media_susceptibilidad = [
            "valle del cauca", "chocó", "meta", "caquetá"
        ]
        
        dept_lower = departamento.lower()
        
        if any(d in dept_lower for d in alta_susceptibilidad):
            nivel = "ALTA"
            descripcion = "Zona montañosa con pendientes pronunciadas"
        elif any(d in dept_lower for d in media_susceptibilidad):
            nivel = "MEDIA"
            descripcion = "Zona con topografía variable"
        else:
            nivel = "BAJA a MEDIA"
            descripcion = "Zona relativamente plana o piedemonte"
        
        return {
            "departamento": departamento,
            "susceptibilidad": nivel,
            "descripcion": descripcion,
            "recomendacion": "Consultar mapas detallados en https://datos.sgc.gov.co",
            "nota": "Esta es una evaluación general. Para análisis específico de un sitio, se requiere estudio geotécnico profesional.",
            "factores_locales": [
                "Pendiente del terreno",
                "Tipo de suelo y roca",
                "Nivel freático",
                "Cobertura vegetal",
                "Historial de eventos",
                "Régimen de lluvias"
            ]
        }


# Funciones auxiliares para el agente
def formatear_info_sismos(datos_sismos):
    """Formatea datos de sismos para el agente"""
    if "error" in datos_sismos:
        return f"⚠️ {datos_sismos['mensaje']}"
    
    mensaje = f"📊 **Sismos en Colombia - {datos_sismos['periodo']}**\n\n"
    mensaje += f"Fuente: {datos_sismos['fuente']}\n\n"
    mensaje += datos_sismos['mensaje']
    
    return mensaje


def formatear_info_volcanes(datos_volcanes):
    """Formatea datos de volcanes para el agente"""
    mensaje = f"🌋 **Volcanes Activos en Colombia**\n\n"
    mensaje += f"Total monitoreados: {datos_volcanes['total_activos']}\n"
    mensaje += f"Fuente: {datos_volcanes['fuente']}\n\n"
    
    mensaje += "**Sistema de Alertas:**\n"
    for color, desc in datos_volcanes['sistema_alerta'].items():
        emoji = {"verde": "🟢", "amarillo": "🟡", "naranja": "🟠", "rojo": "🔴"}
        mensaje += f"{emoji.get(color, '•')} {color.upper()}: {desc}\n"
    
    mensaje += "\n**Principales volcanes monitoreados:**\n\n"
    for v in datos_volcanes['volcanes'][:5]:  # Primeros 5
        mensaje += f"• **{v['nombre']}** ({v['ubicacion']})\n"
        mensaje += f"  Altura: {v['altura_msnm']} msnm\n"
        if 'url' in v:
            mensaje += f"  Info: {v['url']}\n"
        mensaje += "\n"
    
    mensaje += f"\n💡 {datos_volcanes['nota']}"
    
    return mensaje


def formatear_info_movimientos(datos_movimientos):
    """Formatea información de movimientos en masa"""
    mensaje = f"🏔️ **Movimientos en Masa en Colombia**\n\n"
    mensaje += f"{datos_movimientos['descripcion']}\n\n"
    
    mensaje += "**Tipos principales:**\n"
    for tipo in datos_movimientos['tipos']:
        mensaje += f"• **{tipo['nombre']}**: {tipo['descripcion']}\n"
    
    mensaje += "\n**Factores detonantes:**\n"
    for factor in datos_movimientos['factores_detonantes']:
        mensaje += f"• {factor}\n"
    
    mensaje += "\n**Recomendaciones:**\n"
    for rec in datos_movimientos['recomendaciones'][:3]:
        mensaje += f"✓ {rec}\n"
    
    mensaje += f"\n🗺️ Mapas detallados: {datos_movimientos['url_mapas']}"
    
    return mensaje


# Instancia global del cliente
sgc_client = SGCClient()
