"""
panels/organizacional.py
Panel "Organizacional": exposición de las empresas.
Usa matplotlib (estático) en vez de Plotly porque cada año de PwC es una
encuesta con preguntas distintas. No hay serie temporal que justifique 
interactividad en el propio gráfico.
"""

import streamlit as st
import matplotlib.pyplot as plt


def render(datos):
    st.header("Organizacional — exposición de las empresas")
    st.caption(
        "Cada año corresponde a una encuesta PwC distinta, con preguntas propias. "
        "No son comparables entre sí como serie temporal: se muestran como fotos independientes."
    )

    # Selector de año: puebla las opciones directo desde los datos.
    # Importante: "anios" se utiliza intencionalmente para evitar futuros errores con otras herramientas
    anios_disponibles = sorted(datos["periodo_año"].unique(), reverse=True)
    anio_elegido = st.selectbox("Año del informe", anios_disponibles)

    subset = datos[datos["periodo_año"] == anio_elegido].sort_values("valor")

    fig, ax = plt.subplots(figsize=(9, max(3, len(subset) * 0.4)))
    ax.barh(subset["metrica"], subset["valor"], color="#d94f4f")
    ax.set_xlabel("% de organizaciones")
    ax.set_title(f"Organizaciones en Argentina — PwC Digital Trust Insights {anio_elegido}")
    ax.set_xlim(0, 100)

    # Etiqueta con el valor al final de cada barra, para no obligar al lector
    # a leer contra el eje.
    for i, valor in enumerate(subset["valor"]):
        ax.text(valor + 1, i, f"{valor}%", va="center", fontsize=8)

    fig.tight_layout()
    st.pyplot(fig)

    fuente = subset["fuente"].iloc[0] if len(subset) else ""
    st.caption(f"Fuente: {fuente}")