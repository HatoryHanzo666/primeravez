"""
Módulo de integración con IDEAM (Instituto de Hidrología, Meteorología y Estudios Ambientales)
Obtiene datos de clima, pronósticos, alertas y lluvias
"""
import requests
from datetime import datetime, timedelta
import json


class IDEAMClient:
    """Cliente para obtener datos del IDEAM"""
    
    def __init__(self):
        self.base_url = "http://www.pronosticosyalertas.gov.co"
        self.datos_abiertos_url = f"{self.base_url}/datos-abiertos-ideam"
        self.main_url = "https://www.ideam.gov.co"
        
    def obtener_pronostico_ciudad(self, ciudad):
        """
        Obtiene pronóstico del tiempo para una ciudad
        
        Args:
            ciudad: Nombre de la ciudad
            
        Returns:
            Dict con pronóstico
        """
        # Principales ciudades de Colombia
        ciudades_principales = {
            "bogotá": {"nombre": "Bogotá D.C.", "region": "Andina"},
            "bogota": {"nombre": "Bogotá D.C.", "region": "Andina"},
            "medellín": {"nombre": "Medellín", "region": "Andina"},
            "medellin": {"nombre": "Medellín", "region": "Andina"},
            "cali": {"nombre": "Cali", "region": "Pacífica"},
            "barranquilla": {"nombre": "Barranquilla", "region": "Caribe"},
            "cartagena": {"nombre": "Cartagena", "region": "Caribe"},
            "bucaramanga": {"nombre": "Bucaramanga", "region": "Andina"},
            "manizales": {"nombre": "Manizales", "region": "Andina"},
            "pereira": {"nombre": "Pereira", "region": "Andina"},
            "cúcuta": {"nombre": "Cúcuta", "region": "Andina"},
            "cucuta": {"nombre": "Cúcuta", "region": "Andina"},
            "ibagué": {"nombre": "Ibagué", "region": "Andina"},
            "ibague": {"nombre": "Ibagué", "region": "Andina"},
            "santa marta": {"nombre": "Santa Marta", "region": "Caribe"},
            "villavicencio": {"nombre": "Villavicencio", "region": "Orinoquía"},
            "pasto": {"nombre": "Pasto", "region": "Andina"},
            "neiva": {"nombre": "Neiva", "region": "Andina"},
            "armenia": {"nombre": "Armenia", "region": "Andina"},
            "popayán": {"nombre": "Popayán", "region": "Andina"},
            "popayon": {"nombre": "Popayán", "region": "Andina"},
        }
        
        ciudad_lower = ciudad.lower().strip()
        info_ciudad = ciudades_principales.get(ciudad_lower)
        
        if not info_ciudad:
            return {
                "ciudad": ciudad,
                "error": "Ciudad no encontrada en base de datos",
                "mensaje": f"Consulta el pronóstico oficial en {self.datos_abiertos_url}",
                "ciudades_disponibles": list(ciudades_principales.keys())
            }
        
        # Pronóstico genérico basado en regiones
        pronostico = {
            "ciudad": info_ciudad["nombre"],
            "region": info_ciudad["region"],
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "fuente": "IDEAM - www.ideam.gov.co",
            "mensaje": f"Para pronóstico actualizado en tiempo real, consulta: {self.datos_abiertos_url}",
            "datos_generales": {
                "descripcion": "Datos generales por región",
                "nota": "Esta es información de referencia. Para datos precisos y actualizados, consulta la fuente oficial."
            },
            "pronostico_regional": self._get_pronostico_regional(info_ciudad["region"]),
            "recomendaciones": [
                "Consultar pronóstico oficial del IDEAM",
                "Estar atento a alertas meteorológicas",
                "Seguir redes oficiales @IDEAMColombia"
            ]
        }
        
        return pronostico
    
    def _get_pronostico_regional(self, region):
        """Obtiene características climáticas generales por región"""
        regiones = {
            "Andina": {
                "clima": "Templado de montaña",
                "temperatura_promedio": "14-24°C",
                "epoca_lluvias": "Abril-Mayo y Octubre-Noviembre",
                "caracteristicas": [
                    "Clima variable por altitud",
                    "Lluvias frecuentes en tardes",
                    "Temperatura depende de altura"
                ]
            },
            "Caribe": {
                "clima": "Cálido y húmedo",
                "temperatura_promedio": "27-32°C",
                "epoca_lluvias": "Mayo-Noviembre",
                "caracteristicas": [
                    "Altas temperaturas todo el año",
                    "Temporada de huracanes agosto-noviembre",
                    "Época seca diciembre-abril"
                ]
            },
            "Pacífica": {
                "clima": "Muy húmedo",
                "temperatura_promedio": "25-28°C",
                "epoca_lluvias": "Todo el año (zona más lluviosa)",
                "caracteristicas": [
                    "Alta precipitación anual",
                    "Humedad constante",
                    "Lluvias frecuentes"
                ]
            },
            "Orinoquía": {
                "clima": "Cálido y estacional",
                "temperatura_promedio": "26-30°C",
                "epoca_lluvias": "Abril-Noviembre",
                "caracteristicas": [
                    "Estación seca muy marcada",
                    "Lluvias intensas en invierno",
                    "Calor intenso"
                ]
            },
            "Amazonía": {
                "clima": "Ecuatorial húmedo",
                "temperatura_promedio": "25-27°C",
                "epoca_lluvias": "Todo el año",
                "caracteristicas": [
                    "Humedad muy alta",
                    "Lluvias constantes",
                    "Poca variación térmica"
                ]
            }
        }
        
        return regiones.get(region, {
            "clima": "No disponible",
            "temperatura_promedio": "Consultar IDEAM",
            "epoca_lluvias": "Consultar IDEAM",
            "caracteristicas": ["Información no disponible"]
        })
    
    def obtener_alertas_activas(self):
        """
        Obtiene alertas meteorológicas activas
        
        Returns:
            Dict con alertas
        """
        alertas = {
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "fuente": "IDEAM - Sistema de Alertas",
            "url_oficial": "http://www.pronosticosyalertas.gov.co",
            "mensaje": "Para alertas en tiempo real, consulta la fuente oficial del IDEAM",
            "tipos_alerta": {
                "Roja": "Peligro inminente - Tomar acción inmediata",
                "Naranja": "Posible peligro - Estar preparado",
                "Amarilla": "Posibles afectaciones menores - Estar atento",
                "Verde": "Condiciones normales"
            },
            "alertas_activas": [],
            "nota": "Sistema de consulta en desarrollo. Visita www.ideam.gov.co para alertas oficiales.",
            "fenomenos_monitorear": [
                "Lluvias intensas",
                "Tormentas eléctricas",
                "Vientos fuertes",
                "Oleaje en costas",
                "Temperaturas extremas"
            ]
        }
        
        return alertas
    
    def obtener_info_lluvias(self):
        """
        Información sobre lluvias y precipitaciones
        
        Returns:
            Dict con información de lluvias
        """
        info = {
            "titulo": "Información sobre Lluvias en Colombia",
            "fuente": "IDEAM",
            "epocas_lluvia": {
                "primer_periodo": {
                    "meses": "Abril - Mayo",
                    "regiones_afectadas": ["Andina", "Caribe", "Pacífica"],
                    "intensidad": "Alta"
                },
                "segundo_periodo": {
                    "meses": "Octubre - Noviembre",
                    "regiones_afectadas": ["Andina", "Pacífica"],
                    "intensidad": "Alta"
                }
            },
            "regiones_mas_lluviosas": [
                {
                    "region": "Pacífico Colombiano",
                    "precipitacion_anual": "Hasta 10,000 mm",
                    "nota": "Una de las zonas más lluviosas del mundo"
                },
                {
                    "region": "Amazonía",
                    "precipitacion_anual": "2,500-4,000 mm",
                    "nota": "Lluvia constante todo el año"
                },
                {
                    "region": "Zona Andina",
                    "precipitacion_anual": "1,000-2,000 mm",
                    "nota": "Variación por altitud"
                }
            ],
            "umbrales_alerta": {
                "lluvia_ligera": "< 2 mm/h",
                "lluvia_moderada": "2-10 mm/h",
                "lluvia_fuerte": "10-30 mm/h",
                "lluvia_muy_fuerte": "> 30 mm/h"
            },
            "recomendaciones": [
                "Monitorear boletines del IDEAM",
                "Evitar zonas bajas en lluvias fuertes",
                "No cruzar ríos crecidos",
                "Tener plan de evacuación",
                "Kit de emergencia listo"
            ],
            "fuentes_oficiales": {
                "web": "www.ideam.gov.co",
                "twitter": "@IDEAMColombia",
                "datos_abiertos": "http://www.pronosticosyalertas.gov.co/datos-abiertos-ideam"
            }
        }
        
        return info
    
    def obtener_fenomeno_el_nino_la_nina(self):
        """
        Información sobre El Niño y La Niña
        
        Returns:
            Dict con información de ENOS
        """
        info = {
            "titulo": "Fenómeno El Niño - Oscilación del Sur (ENOS)",
            "descripcion": "Fenómeno climático que afecta el régimen de lluvias en Colombia",
            "el_nino": {
                "caracteristicas": "Calentamiento del Pacífico ecuatorial",
                "efectos_colombia": [
                    "Reducción de lluvias en regiones Andina y Caribe",
                    "Aumento de temperaturas",
                    "Mayor riesgo de incendios forestales",
                    "Disminución caudal de ríos",
                    "Afectación agricultura"
                ],
                "epocas_criticas": "Diciembre-Febrero y Junio-Agosto"
            },
            "la_nina": {
                "caracteristicas": "Enfriamiento del Pacífico ecuatorial",
                "efectos_colombia": [
                    "Aumento de lluvias",
                    "Mayor riesgo de inundaciones",
                    "Deslizamientos más frecuentes",
                    "Crecidas de ríos",
                    "Temperaturas más bajas"
                ],
                "epocas_criticas": "Abril-Mayo y Octubre-Noviembre"
            },
            "monitoreo": "El IDEAM monitorea constantemente estos fenómenos",
            "fuente": "IDEAM - Oficina de Pronósticos y Alertas",
            "url": "https://www.ideam.gov.co"
        }
        
        return info


# Funciones auxiliares para formatear
def formatear_pronostico(pronostico):
    """Formatea pronóstico para el agente"""
    if "error" in pronostico:
        return f"⚠️ {pronostico['mensaje']}"
    
    msg = f"🌤️ **Pronóstico para {pronostico['ciudad']}**\n\n"
    msg += f"📍 Región: {pronostico['region']}\n"
    msg += f"🕐 Consulta: {pronostico['fecha_consulta']}\n\n"
    
    regional = pronostico['pronostico_regional']
    msg += f"**Características climáticas regionales:**\n"
    msg += f"🌡️ Temperatura promedio: {regional['temperatura_promedio']}\n"
    msg += f"🌧️ Época de lluvias: {regional['epoca_lluvias']}\n\n"
    
    msg += "**Características:**\n"
    for caract in regional['caracteristicas']:
        msg += f"• {caract}\n"
    
    msg += f"\n💡 {pronostico['mensaje']}"
    
    return msg


def formatear_alertas(alertas):
    """Formatea alertas para el agente"""
    msg = f"🚨 **Alertas Meteorológicas - IDEAM**\n\n"
    msg += f"🕐 Consulta: {alertas['fecha_consulta']}\n\n"
    
    msg += "**Niveles de alerta:**\n"
    for nivel, desc in alertas['tipos_alerta'].items():
        emoji = {"Roja": "🔴", "Naranja": "🟠", "Amarilla": "🟡", "Verde": "🟢"}
        msg += f"{emoji.get(nivel, '•')} **{nivel}**: {desc}\n"
    
    msg += f"\n💡 {alertas['mensaje']}\n"
    msg += f"🌐 Fuente oficial: {alertas['url_oficial']}"
    
    return msg


def formatear_info_lluvias(info):
    """Formatea información de lluvias"""
    msg = f"🌧️ **{info['titulo']}**\n\n"
    
    msg += "**Épocas de lluvia:**\n"
    for periodo, datos in info['epocas_lluvia'].items():
        msg += f"• {datos['meses']}: {', '.join(datos['regiones_afectadas'])}\n"
    
    msg += "\n**Regiones más lluviosas:**\n"
    for region in info['regiones_mas_lluviosas'][:2]:
        msg += f"• **{region['region']}**: {region['precipitacion_anual']}\n"
    
    msg += "\n**Recomendaciones:**\n"
    for rec in info['recomendaciones'][:3]:
        msg += f"✓ {rec}\n"
    
    msg += f"\n🌐 Fuentes oficiales:\n"
    msg += f"• Web: {info['fuentes_oficiales']['web']}\n"
    msg += f"• Twitter: {info['fuentes_oficiales']['twitter']}"
    
    return msg


# Instancia global
ideam_client = IDEAMClient()
