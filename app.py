import os
import time
import json
import paho.mqtt.client as paho
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# ----------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ----------------------------------------------------------
st.set_page_config(
    page_title="BAE | Control por Voz",
    page_icon="🍼",
    layout="centered"
)

# ----------------------------------------------------------
# ESTILO VISUAL — TEMA BAE 💛
# ----------------------------------------------------------
st.markdown(
    """
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFF8EA;
        color: #3C3C3C;
        font-family: 'Poppins', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        color: #DD8E6B;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #4D797A;
        margin-bottom: 2rem;
    }

    .voice-section {
        background-color: #FFFFFFEE;
        border-radius: 25px;
        border: 1px solid #DD8E6B40;
        padding: 2rem;
        box-shadow: 0px 6px 15px rgba(221, 142, 107, 0.15);
        text-align: center;
    }

    .mic-button {
        background: linear-gradient(135deg, #C6E2E3, #FFF2C3);
        color: #DD8E6B;
        border: none;
        border-radius: 50%;
        width: 130px;
        height: 130px;
        font-size: 3rem;
        margin: 1rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }

    .mic-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(221, 142, 107, 0.3);
    }

    .result-box {
        background: #FFFFFF;
        border: 2px solid #DD8E6B30;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    .status-indicator {
        display: inline-block;
        background: #C6E2E3;
        color: #3C3C3C;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem 0;
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.06); }
        100% { transform: scale(1); }
    }

    .info-text {
        color: #4D797A;
        font-size: 1rem;
        margin: 1rem 0;
    }

    .stButton > button {
        background-color: #C6E2E3;
        color: #3C3C3C;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6em 1.2em;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #DD8E6B;
        color: white;
        transform: scale(1.03);
    }

    [data-testid="stMetricValue"] {
        color: #DD8E6B !important;
        font-weight: 700;
    }
</style>
""",
    unsafe_allow_html=True
)

# ----------------------------------------------------------
# CONFIGURACIÓN MQTT
# ----------------------------------------------------------
broker = "broker.mqttdashboard.com"
port = 1883

def on_publish(client, userdata, result):
    st.toast("Comando enviado exitosamente 💛", icon="✅")

# ----------------------------------------------------------
# INICIALIZAR SESIÓN
# ----------------------------------------------------------
if "last_command" not in st.session_state:
    st.session_state.last_command = ""

# ----------------------------------------------------------
# ENCABEZADO PRINCIPAL
# ----------------------------------------------------------
st.markdown('<div class="main-title"> Control por Voz BAE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Comunica, controla y conecta con suavidad 💛</div>', unsafe_allow_html=True)

# ----------------------------------------------------------
# SECCIÓN DE MICRÓFONO
# ----------------------------------------------------------
st.markdown('<div class="voice-section">', unsafe_allow_html=True)
st.markdown('<div class="mic-button pulse">🎤</div>', unsafe_allow_html=True)
st.markdown('<div class="info-text">Presiona el botón e indica tu comando de voz</div>', unsafe_allow_html=True)

stt_button = Button(label="🎧 Iniciar Reconocimiento", width=300, height=60)
stt_button.js_on_event(
    "button_click",
    CustomJS(
        code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'es-ES';
        recognition.onresult = function (e) {
            var value = e.results[0][0].transcript;
            if (value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.onerror = function(e) {
            document.dispatchEvent(new CustomEvent("RECORDING_ERROR", {detail: e.error}));
        }
        recognition.start();
        """
    ),
)

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=80,
    debounce_time=0,
)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# RESULTADOS Y ENVÍO MQTT
# ----------------------------------------------------------
if result and "GET_TEXT" in result:
    command = result.get("GET_TEXT").strip()
    st.session_state.last_command = command

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown("### 🗣️ Comando Reconocido")
    st.markdown(f'<div style="font-size:1.4rem; color:#DD8E6B; font-weight:600;">“{command}”</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-indicator">✅ Comando procesado</div>', unsafe_allow_html=True)

    try:
        client1 = paho.Client("BAE_Voice")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"BAE_Command": command})
        client1.publish("bae_voice_ctrl", message)
        client1.disconnect()
    except Exception as e:
        st.error(f"Error al enviar comando: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# HISTORIAL DE COMANDOS
# ----------------------------------------------------------
if st.session_state.last_command:
    with st.expander("📝 Historial de Comandos", expanded=True):
        st.metric("Último Comando", st.session_state.last_command)

# ----------------------------------------------------------
# INFORMACIÓN DE CONEXIÓN
# ----------------------------------------------------------
with st.expander("🔧 Información de Conexión"):
    st.write(f"**Broker MQTT:** {broker}")
    st.write(f"**Puerto:** {port}")
    st.write(f"**Tópico:** bae_voice_ctrl")
    st.write("**Comandos sugeridos:** 'encender luz', 'apagar motor', 'abrir puerta', etc.")

st.markdown("---")
st.markdown("✨ Desarrollado con amor por **BAE | IA afectiva para el bienestar** 💛")
