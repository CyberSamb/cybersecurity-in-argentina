"""
streamlit_app.py
Punto de entrada de la app. Maneja solo la navegación entre los 3 niveles
(Personal / Organizacional / Gubernamental) y delega el contenido de cada
panel a su propia función. Los gráficos reales se agregan en la etapa 4.
"""

import streamlit as st
from data_loader import cargar_datos, filtrar_por_nivel
from panels import personal as panel_personal_modulo
from panels import organizacional as panel_organizacional_modulo
from panels import gubernamental as panel_gubernamental_modulo
from panels import footer

# Configuración general de la página (una sola vez, al principio)
st.set_page_config(
    page_title="La ciberseguridad invisible",
    layout="wide",
)

# Carga de datos: una sola vez por sesión, no en cada interacción del usuario.
# st.cache_data evita releer el CSV cada vez que alguien toca un filtro.
@st.cache_data
def obtener_dataframe():
    return cargar_datos()

df = obtener_dataframe()


# --- Header del proyecto ---
st.title("La ciberseguridad invisible")
st.caption("La exposición de la que nadie habla")


# --- Navegación entre niveles ---
# Un radio en la barra lateral decide qué panel se muestra.
nivel_seleccionado = st.sidebar.radio(
    "Nivel de exposición",
    options=["Personal", "Organizacional", "Gubernamental"],
)


# --- Cada nivel tiene su propia función de panel ---
# Por ahora cada una solo muestra los datos filtrados como tabla, para
# confirmar que la navegación y el filtrado funcionan de punta a punta.
# En la etapa 4 esto se reemplaza por los gráficos reales.

def panel_personal(datos):
    panel_personal_modulo.render(datos)


def panel_organizacional(datos):
    panel_organizacional_modulo.render(datos)


def panel_gubernamental(datos):
    panel_gubernamental_modulo.render(datos)


# Despacho: según lo elegido en el sidebar, filtra y llama al panel correspondiente
if nivel_seleccionado == "Personal":
    panel_personal(filtrar_por_nivel(df, "personal"))
elif nivel_seleccionado == "Organizacional":
    panel_organizacional(filtrar_por_nivel(df, "organizacional"))
else:
    panel_gubernamental(filtrar_por_nivel(df, "gubernamental"))


# --- Footer: siempre visible, no depende del panel seleccionado ---
footer.render(df)