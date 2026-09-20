"""
panels/gap_habitos.py
Sección "el gap de 7 años": pieza central del storytelling del panel Personal.
No es una tendencia -- es precisamente la ausencia de una. La última encuesta nacional de
hábitos de higiene digital es de 2018-2019 (Avast + Kaspersky); no hay
medición nacional posterior. Esto, por desgracia, demuestra falta de transparencia institucional
y compromiso con la ciberseguridad ciudanana.
"""

import streamlit as st
import plotly.express as px
from datetime import date

from etiquetas import etiqueta_legible

METRICAS_HABITOS = [
    "pct_usuarios_usa_gestor_password",
    "pct_usuarios_password_debil",
    "pct_usuarios_reutiliza_password",
    "pct_usuarios_no_cambia_password_frecuencia",
    "pct_usuarios_solo_3_passwords",
]


def render(datos):
    st.markdown("---")
    st.subheader("El silencio de 7 años")

    habitos = datos[datos["metrica"].isin(METRICAS_HABITOS)].sort_values("valor")

    anio_actual = date.today().year
    anios_de_silencio = anio_actual - 2019

    # Callout grande: el número que importa es "años sin nueva medición",
    # no un dato de la encuesta en sí.
    st.markdown(
        f"""
        <div style="background-color:#1a1a2e; padding:1.2rem; border-left:6px solid #d94f4f; border-radius:4px;">
        <span style="font-size:2.5rem; font-weight:bold; color:#d94f4f;">{anios_de_silencio} años</span><br>
        <span style="color:#eaeaea;">sin una nueva encuesta nacional sobre hábitos de higiene digital en Argentina.
        La última medición disponible es de 2018-2019.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")  # espaciado

    # La única foto que existe -- se muestra completa, sin compararla con nada
    # posterior porque no hay nada posterior con qué compararla.
    fig = px.bar(
        habitos,
        x="valor",
        y=habitos["metrica"].apply(etiqueta_legible),
        orientation="h",
        title="Última fotografía disponible de hábitos de higiene digital (2018-2019)",
        labels={"x": "% de usuarios", "y": ""},
        color_discrete_sequence=["#3a86ff"],
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Fuente: Avast (2018-2019) y Kaspersky Lab / CORPA (2019). "
        "No se identificó ningún estudio nacional posterior sobre esta misma dimensión."
    )