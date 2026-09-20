"""
streamlit_app.py
Punto de entrada de la app. Maneja solo la navegación entre los 3 niveles
(Personal / Organizacional / Gubernamental) y delega el contenido de cada
panel a su propia función. 
"""

import streamlit as st
from data_loader import cargar_datos, filtrar_por_nivel

# Configuración general de la página
st.set_page_config(
    page_title="La ciberseguridad invisible",
    layout="wide",
)

# carga de datos: se realiza una sola vez por sesión, no en cada interacción del usuario.
# st.cache_data evita releer el CSV cada vez que alguien toca un filtro.
@st.cache_data
def obtener_dataframe():
    return cargar_datos()

df = obtener_dataframe()


# --- Header ---
st.title("La ciberseguridad invisible")
st.caption("La exposición de la que nadie habla")


# --- Navegación entre niveles ---
# Un radio en la barra lateral decide qué panel se muestra.
nivel_seleccionado = st.sidebar.radio(
    "Nivel de exposición",
    options=["Personal", "Organizacional", "Gubernamental"],
)


# --- Cada nivel tiene su propia función de panel ---
def panel_personal(datos):
    st.header("Personal — exposición de la ciudadanía")
    st.dataframe(datos, width='stretch')


def panel_organizacional(datos):
    st.header("Organizacional — exposición de las empresas")
    st.dataframe(datos, width='stretch')


def panel_gubernamental(datos):
    st.header("Gubernamental — exposición del Estado")
    st.dataframe(datos, width='stretch')


# Despacho: según lo elegido en el sidebar, filtra y llama al panel correspondiente
if nivel_seleccionado == "Personal":
    panel_personal(filtrar_por_nivel(df, "personal"))
elif nivel_seleccionado == "Organizacional":
    panel_organizacional(filtrar_por_nivel(df, "organizacional"))
else:
    panel_gubernamental(filtrar_por_nivel(df, "gubernamental"))