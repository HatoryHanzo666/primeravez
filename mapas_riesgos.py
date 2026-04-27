"""
Módulo de Mapas para Agente de Gestión de Riesgo
VERSIÓN OFICIAL - Usa datos del DANE (Gobierno de Colombia)
Fuente: https://geoportal.dane.gov.co/
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_scalebar.scalebar import ScaleBar
import numpy as np
from matplotlib import colors
import pandas as pd
from shapely.geometry import Point
from datetime import datetime
import os


class MapaRiesgosColombia:
    """Sistema de mapas georeferenciados para gestión de riesgo"""
    
    def __init__(self):
        """Inicializar sistema de mapas"""
        print("🗺️ Inicializando sistema de mapas...")
        
        # URLs OFICIALES - Datos Abiertos Colombia (Gobierno Nacional)
        # Estos datos son mantenidos por el DANE y son los oficiales del país
        self.url_deptos = "https://www.datos.gov.co/resource/xdk5-pm3f.geojson"
        
        # Alternativa si la primera falla (GitHub respaldo)
        self.url_backup = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
        
        # Cargar datos
        try:
            print("📥 Descargando mapa oficial desde datos.gov.co...")
            self.gdf_deptos = gpd.read_file(self.url_deptos)
            self.gdf_municipios = self.gdf_deptos.copy()
            print(f"✅ Datos oficiales DANE cargados ({len(self.gdf_deptos)} departamentos)")
            self.fuente = "DANE - datos.gov.co"
        except Exception as e:
            print(f"⚠️ Error con datos.gov.co: {e}")
            print("📥 Intentando con fuente de respaldo (GitHub)...")
            try:
                self.gdf_deptos = gpd.read_file(self.url_backup)
                self.gdf_municipios = self.gdf_deptos.copy()
                print(f"✅ Datos de respaldo cargados ({len(self.gdf_deptos)} regiones)")
                self.fuente = "GitHub (respaldo)"
            except Exception as e2:
                print(f"❌ ERROR: No se pudieron cargar datos geográficos")
                print(f"   Error 1 (datos.gov.co): {e}")
                print(f"   Error 2 (GitHub): {e2}")
                print("\n💡 Soluciones:")
                print("   1. Verifica tu conexión a internet")
                print("   2. Intenta de nuevo en unos minutos")
                print("   3. Ejecuta: pip install --upgrade geopandas requests")
                self.gdf_deptos = None
                self.gdf_municipios = None
                self.fuente = "No disponible"
                return
        
        # Sistemas de coordenadas
        self.crs_wgs84 = 'EPSG:4326'  # WGS84 (lat/lon)
        self.crs_magna = 'EPSG:3116'  # MAGNA SIRGAS Colombia
        
        self.setup_coordenadas()
        
        # Directorio para guardar mapas
        self.output_dir = "mapas_generados"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup_coordenadas(self):
        """Configurar sistemas de coordenadas"""
        if self.gdf_deptos is None:
            return
        try:
            self.gdf_deptos_magna = self.gdf_deptos.to_crs(self.crs_magna)
            self.gdf_municipios_magna = self.gdf_municipios.to_crs(self.crs_magna)
            print("✅ MAGNA SIRGAS EPSG:3116 configurado")
        except Exception as e:
            print(f"⚠️ Usando WGS84 (lat/lon) como respaldo")
            self.gdf_deptos_magna = self.gdf_deptos
            self.gdf_municipios_magna = self.gdf_municipios
    
    def mapa_sismos(self, sismos_data, archivo_salida=None):
        """
        Mapa de sismos recientes
        
        Args:
            sismos_data: Lista de dict con {lat, lon, magnitud, profundidad, ubicacion}
            archivo_salida: Nombre del archivo (opcional)
        """
        if self.gdf_deptos is None:
            print("❌ No se puede generar mapa - datos geográficos no disponibles")
            return None
            
        if not sismos_data:
            print("⚠️ No hay datos de sismos para visualizar")
            return None
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 16))
        
        # Mapa base Colombia
        self.gdf_deptos.plot(ax=ax, color='#f0f8ff', 
                            edgecolor='#95a5a6', linewidth=0.8, alpha=0.7)
        
        # Plotear sismos
        for sismo in sismos_data:
            lat, lon = sismo.get('lat', 0), sismo.get('lon', 0)
            mag = sismo.get('magnitud', 3.0)
            
            # Tamaño proporcional a magnitud
            size = (mag ** 2) * 10
            color = self._color_magnitud(mag)
            
            ax.plot(lon, lat, 'o', markersize=size, color=color,
                   alpha=0.6, markeredgecolor='darkred', 
                   markeredgewidth=1, transform=ax.transData)
        
        # Título y elementos
        ax.set_title(f"Sismos Recientes en Colombia\n{len(sismos_data)} eventos\nFuente mapa: {self.fuente}",
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_axis_off()
        
        # Leyenda de magnitudes
        self._agregar_leyenda_sismos(ax)
        
        # Guardar
        if archivo_salida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"mapa_sismos_{timestamp}.png"
        
        ruta_completa = os.path.join(self.output_dir, archivo_salida)
        plt.savefig(ruta_completa, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        print(f"✅ Mapa guardado: {ruta_completa}")
        
        return fig, ax, ruta_completa
    
    def mapa_volcanes(self, volcanes_data, archivo_salida=None):
        """
        Mapa de volcanes activos
        
        Args:
            volcanes_data: Lista de dict con {nombre, lat, lon, alerta}
        """
        if self.gdf_deptos is None:
            print("❌ No se puede generar mapa - datos geográficos no disponibles")
            return None
            
        if not volcanes_data:
            print("⚠️ No hay datos de volcanes para visualizar")
            return None
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 16))
        
        # Mapa base
        self.gdf_deptos.plot(ax=ax, color='#f0f8ff',
                            edgecolor='#95a5a6', linewidth=0.8, alpha=0.7)
        
        # Plotear volcanes
        for volcan in volcanes_data:
            lat, lon = volcan.get('lat', 0), volcan.get('lon', 0)
            nombre = volcan.get('nombre', 'Desconocido')
            alerta = volcan.get('alerta', 'verde')
            
            color = self._color_alerta_volcan(alerta)
            
            ax.plot(lon, lat, '^', markersize=20, color=color,
                   markeredgecolor='black', markeredgewidth=2,
                   transform=ax.transData, zorder=5)
            
            # Etiqueta
            ax.text(lon, lat + 0.15, nombre, fontsize=9,
                   ha='center', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(f"Volcanes Activos en Colombia\n{len(volcanes_data)} monitoreados\nFuente mapa: {self.fuente}",
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_axis_off()
        
        # Leyenda
        self._agregar_leyenda_volcanes(ax)
        
        # Guardar
        if archivo_salida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"mapa_volcanes_{timestamp}.png"
        
        ruta_completa = os.path.join(self.output_dir, archivo_salida)
        plt.savefig(ruta_completa, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        print(f"✅ Mapa guardado: {ruta_completa}")
        
        return fig, ax, ruta_completa
    
    def mapa_estaciones(self, estaciones_data, departamento=None, archivo_salida=None):
        """
        Mapa de estaciones meteorológicas
        
        Args:
            estaciones_data: Lista de dict con {nombre, lat, lon, tipo}
            departamento: Filtrar por departamento (opcional)
        """
        if self.gdf_deptos is None:
            print("❌ No se puede generar mapa - datos geográficos no disponibles")
            return None
            
        if not estaciones_data:
            print("⚠️ No hay datos de estaciones para visualizar")
            return None
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 16))
        
        # Mapa base
        self.gdf_deptos.plot(ax=ax, color='#f0f8ff',
                            edgecolor='#95a5a6', linewidth=0.8, alpha=0.7)
        
        # Plotear estaciones
        for estacion in estaciones_data:
            lat, lon = estacion.get('latitud', 0), estacion.get('longitud', 0)
            nombre = estacion.get('nombre', 'Est')
            tipo = estacion.get('tipo', 'Climatológica')
            
            marker = 's'  # Cuadrado
            color = '#3498db'  # Azul
            
            ax.plot(lon, lat, marker, markersize=8, color=color,
                   markeredgecolor='navy', markeredgewidth=1,
                   transform=ax.transData, alpha=0.7)
        
        titulo = f"Estaciones Meteorológicas - {departamento if departamento else 'Colombia'}"
        ax.set_title(f"{titulo}\n{len(estaciones_data)} estaciones\nFuente mapa: {self.fuente}",
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_axis_off()
        
        # Guardar
        if archivo_salida is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"mapa_estaciones_{timestamp}.png"
        
        ruta_completa = os.path.join(self.output_dir, archivo_salida)
        plt.savefig(ruta_completa, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        print(f"✅ Mapa guardado: {ruta_completa}")
        
        return fig, ax, ruta_completa
    
    def mapa_completo_riesgos(self, sismos=None, volcanes=None, estaciones=None):
        """
        Mapa integrado con múltiples capas de riesgo
        """
        if self.gdf_deptos is None:
            print("❌ No se puede generar mapa - datos geográficos no disponibles")
            return None
            
        fig, ax = plt.subplots(1, 1, figsize=(16, 18))
        
        # Mapa base
        self.gdf_deptos.plot(ax=ax, color='#ecf0f1',
                            edgecolor='#7f8c8d', linewidth=1, alpha=0.8)
        
        # Capa de sismos
        if sismos:
            for sismo in sismos:
                lat, lon = sismo.get('lat', 0), sismo.get('lon', 0)
                mag = sismo.get('magnitud', 3.0)
                size = (mag ** 2) * 8
                ax.plot(lon, lat, 'o', markersize=size, color='orange',
                       alpha=0.5, markeredgecolor='red', markeredgewidth=1)
        
        # Capa de volcanes
        if volcanes:
            for volcan in volcanes:
                lat, lon = volcan.get('lat', 0), volcan.get('lon', 0)
                ax.plot(lon, lat, '^', markersize=15, color='red',
                       markeredgecolor='darkred', markeredgewidth=2, zorder=5)
        
        # Capa de estaciones
        if estaciones:
            for estacion in estaciones:
                lat, lon = estacion.get('latitud', 0), estacion.get('longitud', 0)
                ax.plot(lon, lat, 's', markersize=6, color='blue',
                       markeredgecolor='navy', markeredgewidth=1, alpha=0.6)
        
        ax.set_title(f"Mapa Integrado de Riesgos - Colombia\nFuente: {self.fuente}",
                    fontsize=18, fontweight='bold', pad=20)
        ax.set_axis_off()
        
        # Leyenda combinada
        handles = []
        if sismos:
            handles.append(mpatches.Patch(color='orange', label=f'Sismos ({len(sismos)})'))
        if volcanes:
            handles.append(mpatches.Patch(color='red', label=f'Volcanes ({len(volcanes)})'))
        if estaciones:
            handles.append(mpatches.Patch(color='blue', label=f'Estaciones ({len(estaciones)})'))
        
        ax.legend(handles=handles, loc='lower right', fontsize=12)
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = f"mapa_integrado_{timestamp}.png"
        ruta_completa = os.path.join(self.output_dir, archivo_salida)
        
        plt.savefig(ruta_completa, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        print(f"✅ Mapa integrado guardado: {ruta_completa}")
        
        return fig, ax, ruta_completa
    
    def _color_magnitud(self, magnitud):
        """Color según magnitud del sismo"""
        if magnitud < 3.0:
            return '#95a5a6'
        elif magnitud < 4.0:
            return '#f39c12'
        elif magnitud < 5.0:
            return '#e67e22'
        elif magnitud < 6.0:
            return '#e74c3c'
        else:
            return '#c0392b'
    
    def _color_alerta_volcan(self, nivel):
        """Color según nivel de alerta volcánica"""
        colores = {
            'verde': '#27ae60',
            'amarillo': '#f1c40f',
            'amarilla': '#f1c40f',
            'naranja': '#e67e22',
            'rojo': '#c0392b',
            'roja': '#c0392b'
        }
        return colores.get(nivel.lower(), '#95a5a6')
    
    def _agregar_leyenda_sismos(self, ax):
        """Leyenda de magnitudes"""
        handles = [
            mpatches.Patch(color='#95a5a6', label='M < 3.0'),
            mpatches.Patch(color='#f39c12', label='M 3.0-4.0'),
            mpatches.Patch(color='#e67e22', label='M 4.0-5.0'),
            mpatches.Patch(color='#e74c3c', label='M 5.0-6.0'),
            mpatches.Patch(color='#c0392b', label='M > 6.0'),
        ]
        ax.legend(handles=handles, loc='lower right', fontsize=11,
                 title='Magnitud', framealpha=0.9)
    
    def _agregar_leyenda_volcanes(self, ax):
        """Leyenda de niveles de alerta"""
        handles = [
            mpatches.Patch(color='#27ae60', label='🟢 Verde (Normal)'),
            mpatches.Patch(color='#f1c40f', label='🟡 Amarillo (Cambios)'),
            mpatches.Patch(color='#e67e22', label='🟠 Naranja (Probable)'),
            mpatches.Patch(color='#c0392b', label='🔴 Rojo (Inminente)'),
        ]
        ax.legend(handles=handles, loc='lower right', fontsize=11,
                 title='Nivel de Alerta', framealpha=0.9)


# Instancia global
try:
    sistema_mapas = MapaRiesgosColombia()
    MAPAS_DISPONIBLES = True
except Exception as e:
    print(f"⚠️ Sistema de mapas no disponible: {e}")
    sistema_mapas = None
    MAPAS_DISPONIBLES = False
