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

    /* Contenedor glass */
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
        bor

