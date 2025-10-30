import os
import time
import json
import paho.mqtt.client as paho
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image

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
st.markdown("""
<style>
    /* Fondo general */
    [data-testid="stAppViewContainer"] {
        background-color: #FFF8EA;
        color: #3C3C3C;
        font-family: 'Poppins', sans-serif;
    }

    /* Encabezados */
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

    /* Contenedor principal */
    .voice-section {
        background-color: #FFFFFFEE;
        border-radius: 25px;
        border: 1px solid #DD8E6B40;
        padding: 2rem;
        box-shadow: 0px 6px 15px rgba(221, 142, 107, 0.15);
        text-align: center;
    }

    /* Botón micrófono */
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

    /* Caja de resultados */
    .result-box {
        background: #FFFFFF;
        border: 2px solid #DD8E6B30;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    /* Indicador de estado */
    .status-indicator {
        display: inline-block;
        background: #C6E2E3;
        color: #3C3C3C;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem 0;
    }

    /* Animación suave */
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.06); }
        100% { transform: scale(1); }
    }

    /* Texto informativo */
    .info-text {
        color: #4D797A;
        font-size: 1rem;

