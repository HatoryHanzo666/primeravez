"""
Interfaz Web para Agente de Gestión de Riesgo Colombia
Usando Gradio para chat interactivo + visualización de mapas
"""
import gradio as gr
import os
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

# Importar módulos del agente
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
        MAPAS_DISPONIBLES
    )
except:
    MAPAS_DISPONIBLES = False

# Configuración
import requests
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def chat_con_groq(mensaje, historial):
    """
    Función principal del chat con Groq
    
    Args:
        mensaje: Mensaje del usuario
        historial: Lista de mensajes anteriores
        
    Returns:
        Respuesta del agente
    """
    
    # Verificar comandos especiales
    if mensaje.lower() in ['sgc sismos', 'sismos']:
        datos = sgc_client.obtener_sismos_recientes()
        return formatear_info_sismos(datos)
    
    elif mensaje.lower() in ['sgc volcanes', 'volcanes']:
        datos = sgc_client.obtener_volcanes_activos()
        return formatear_info_volcanes(datos)
    
    elif mensaje.lower() in ['sgc movimientos', 'deslizamientos']:
        datos = sgc_client.obtener_info_movimientos_masa()
        return formatear_info_movimientos(datos)
    
    elif mensaje.lower().startswith('ideam clima'):
        ciudad = mensaje.replace('ideam clima', '').strip() or 'Bogotá'
        datos = ideam_client.obtener_pronostico_ciudad(ciudad)
        return formatear_pronostico(datos)
    
    elif mensaje.lower() in ['ideam alertas', 'alertas']:
        datos = ideam_client.obtener_alertas_activas()
        return formatear_alertas(datos)
    
    elif mensaje.lower() in ['ideam lluvias', 'lluvias']:
        datos = ideam_client.obtener_info_lluvias()
        return formatear_info_lluvias(datos)
    
    # Chat normal con Groq
    system_prompt = """Eres un asistente experto en gestión de riesgo de desastres en Colombia.

Tienes acceso a datos REALES de:
- **SGC (Servicio Geológico Colombiano)**: Sismos, volcanes, movimientos en masa
- **IDEAM**: Clima, pronósticos, alertas meteorológicas, lluvias

Ayudas con:
- Fenómenos meteorológicos y pronósticos
- Sismos, volcanes y actividad geológica  
- Riesgos de deslizamientos
- Alertas y preparación para emergencias

Responde de forma clara, concisa y práctica en español."""

    messages = [{"role": "system", "content": system_prompt}]
    
    # Agregar historial
    for h in historial:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    
    messages.append({"role": "user", "content": mensaje})
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500,
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Error {response.status_code}: No se pudo obtener respuesta"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def generar_mapa_ui(tipo_mapa, departamento=""):
    """
    Genera mapas y los devuelve para la UI
    
    Args:
        tipo_mapa: Tipo de mapa a generar
        departamento: Departamento para estaciones (opcional)
        
    Returns:
        Ruta del archivo de imagen generado
    """
    if not MAPAS_DISPONIBLES:
        return None
    
    try:
        if tipo_mapa == "Sismos":
            resultado = generar_mapa_sismos_sgc()
            # Extraer ruta del resultado
            if "mapas_generados" in resultado:
                ruta = resultado.split(": ")[1]
                return ruta
        
        elif tipo_mapa == "Volcanes":
            resultado = generar_mapa_volcanes_sgc()
            if "mapas_generados" in resultado:
                ruta = resultado.split(": ")[1]
                return ruta
        
        elif tipo_mapa == "Estaciones":
            resultado = generar_mapa_estaciones_ideam(departamento if departamento else None)
            if "mapas_generados" in resultado:
                ruta = resultado.split(": ")[1]
                return ruta
        
        elif tipo_mapa == "Integrado":
            resultado = generar_mapa_integrado()
            if "mapas_generados" in resultado:
                ruta = resultado.split(": ")[1]
                return ruta
        
        return None
    
    except Exception as e:
        print(f"Error generando mapa: {e}")
        return None


# Crear interfaz Gradio
with gr.Blocks(title="Agente de Gestión de Riesgo - Colombia") as demo:
    
    gr.Markdown(
        """
        # 🇨🇴 Agente de IA - Gestión de Riesgo Colombia
        ### Datos en tiempo real del SGC e IDEAM
        
        **Consulta información sobre:**
        - 🌍 Sismos y actividad sísmica
        - 🌋 Volcanes activos
        - 🏔️ Deslizamientos y movimientos en masa
        - 🌦️ Clima y pronósticos
        - 🌧️ Lluvias y alertas meteorológicas
        """
    )
    
    with gr.Tabs():
        
        # TAB 1: CHAT
        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(
                label="Asistente de Riesgo",
                height=500
            )
            
            msg = gr.Textbox(
                label="Tu pregunta",
                placeholder="Ejemplo: ¿Cuáles fueron los últimos sismos en Colombia?",
                lines=2
            )
            
            with gr.Row():
                submit_btn = gr.Button("Enviar", variant="primary")
                clear_btn = gr.Button("Limpiar chat")
            
            gr.Markdown(
                """
                **💡 Comandos rápidos:**
                - `sismos` o `sgc sismos` - Ver sismos recientes
                - `volcanes` o `sgc volcanes` - Ver volcanes activos
                - `deslizamientos` - Info sobre movimientos en masa
                - `ideam clima [ciudad]` - Pronóstico de una ciudad
                - `alertas` - Alertas meteorológicas
                - `lluvias` - Información sobre lluvias
                """
            )
            
            def responder(mensaje, historial):
                respuesta = chat_con_groq(mensaje, historial)
                historial.append((mensaje, respuesta))
                return "", historial
            
            submit_btn.click(responder, [msg, chatbot], [msg, chatbot])
            msg.submit(responder, [msg, chatbot], [msg, chatbot])
            clear_btn.click(lambda: None, None, chatbot, queue=False)
        
        # TAB 2: MAPAS
        with gr.Tab("🗺️ Mapas"):
            gr.Markdown("### Genera mapas de riesgo georeferenciados")
            
            with gr.Row():
                tipo_mapa = gr.Dropdown(
                    choices=["Sismos", "Volcanes", "Estaciones", "Integrado"],
                    value="Sismos",
                    label="Tipo de mapa"
                )
                
                departamento = gr.Textbox(
                    label="Departamento (solo para estaciones)",
                    placeholder="Ej: Cundinamarca",
                    value=""
                )
            
            generar_btn = gr.Button("Generar Mapa", variant="primary")
            
            mapa_output = gr.Image(
                label="Mapa Generado",
                type="filepath"
            )
            
            if not MAPAS_DISPONIBLES:
                gr.Markdown("⚠️ **Sistema de mapas no disponible.** Instala: `pip install geopandas matplotlib matplotlib-scalebar`")
            
            generar_btn.click(
                generar_mapa_ui,
                inputs=[tipo_mapa, departamento],
                outputs=mapa_output
            )
        
        # TAB 3: DATOS SGC
        with gr.Tab("📊 Datos SGC"):
            gr.Markdown("### Datos del Servicio Geológico Colombiano")
            
            with gr.Row():
                btn_sismos = gr.Button("🌍 Ver Sismos Recientes")
                btn_volcanes = gr.Button("🌋 Ver Volcanes Activos")
                btn_movimientos = gr.Button("🏔️ Info Movimientos en Masa")
            
            output_sgc = gr.Textbox(
                label="Información",
                lines=15,
                max_lines=20
            )
            
            btn_sismos.click(
                lambda: formatear_info_sismos(sgc_client.obtener_sismos_recientes()),
                outputs=output_sgc
            )
            
            btn_volcanes.click(
                lambda: formatear_info_volcanes(sgc_client.obtener_volcanes_activos()),
                outputs=output_sgc
            )
            
            btn_movimientos.click(
                lambda: formatear_info_movimientos(sgc_client.obtener_info_movimientos_masa()),
                outputs=output_sgc
            )
        
        # TAB 4: DATOS IDEAM
        with gr.Tab("🌦️ Datos IDEAM"):
            gr.Markdown("### Datos del IDEAM (Clima y Meteorología)")
            
            ciudad_input = gr.Textbox(
                label="Ciudad",
                placeholder="Bogotá",
                value="Bogotá"
            )
            
            with gr.Row():
                btn_clima = gr.Button("🌤️ Ver Pronóstico")
                btn_alertas = gr.Button("🚨 Ver Alertas")
                btn_lluvias = gr.Button("🌧️ Info Lluvias")
            
            output_ideam = gr.Textbox(
                label="Información",
                lines=15,
                max_lines=20
            )
            
            btn_clima.click(
                lambda c: formatear_pronostico(ideam_client.obtener_pronostico_ciudad(c)),
                inputs=ciudad_input,
                outputs=output_ideam
            )
            
            btn_alertas.click(
                lambda: formatear_alertas(ideam_client.obtener_alertas_activas()),
                outputs=output_ideam
            )
            
            btn_lluvias.click(
                lambda: formatear_info_lluvias(ideam_client.obtener_info_lluvias()),
                outputs=output_ideam
            )
        
        # TAB 5: ACERCA DE
        with gr.Tab("ℹ️ Acerca de"):
            gr.Markdown(
                """
                ## 🤖 Agente de IA - Gestión de Riesgo Colombia
                
                **Versión:** 1.0
                
                **Tecnologías:**
                - 🧠 IA: Groq (Llama 3.3 70B)
                - 🌍 Datos SGC: Sismos, volcanes, amenazas
                - 🌦️ Datos IDEAM: Clima, pronósticos, lluvias
                - 🗺️ Mapas: GeoPandas + MAGNA SIRGAS
                - 🌐 Interfaz: Gradio
                
                **Fuentes de datos:**
                - Servicio Geológico Colombiano (SGC)
                - Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM)
                - DANE - Datos Abiertos Colombia
                
                **Desarrollado para:** Gestión de riesgo de desastres en Colombia
                
                ---
                
                💡 **Sugerencias y mejoras:** Contáctanos para agregar nuevas funcionalidades
                """
            )
    
    gr.Markdown(
        """
        ---
        **Nota:** Los datos son de fuentes oficiales pero pueden tener retrasos. Para emergencias, contacta autoridades locales.
        """
    )


# Lanzar la aplicación
if __name__ == "__main__":
    print("=" * 75)
    print("🌐 LANZANDO INTERFAZ WEB DEL AGENTE")
    print("=" * 75)
    print("\n✅ La interfaz web se abrirá automáticamente en tu navegador")
    print("📍 URL local: http://127.0.0.1:7860")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,  # Cambiar a True para URL pública
        inbrowser=True  # Abre automáticamente en navegador
    )
