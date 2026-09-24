"""
panels/gap_habitos.py
Sección "el gap de 7 años": pieza central del storytelling del panel Personal.
No es una tendencia -- es la ausencia de una. La última encuesta nacional de
hábitos de higiene digital es de 2018-2019 (Avast + Kaspersky); no hay
medición nacional posterior. Esto se muestra como hallazgo metodológico
(falta de transparencia institucional), no como limitación del dataset.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

from etiquetas import etiqueta_legible
from colors import AZUL_DEFENSA, ROJO_AMENAZA

METRICAS_HABITOS = [
    "pct_usuarios_usa_gestor_password",
    "pct_usuarios_password_debil",
    "pct_usuarios_reutiliza_password",
    "pct_usuarios_no_cambia_password_frecuencia",
    "pct_usuarios_solo_3_passwords",
]

ULTIMO_ANIO_CON_DATO = 2019


def _linea_de_tiempo(anio_ultimo_dato, anio_actual):
    """
    Timeline minimalista: un punto marcado en el último año con dato, un
    punto hueco en el año actual (todavía sin dato), y una línea punteada
    entre medio para que el vacío se lea de un vistazo, sin necesidad de
    leer ningún número.
    """
    anios_intermedios = list(range(anio_ultimo_dato + 1, anio_actual))

    fig = go.Figure()

    # Línea punteada -- representa el vacío, no una tendencia
    fig.add_trace(go.Scatter(
        x=[anio_ultimo_dato, anio_actual], y=[0, 0],
        mode="lines",
        line=dict(color=ROJO_AMENAZA, dash="dot", width=2),
        hoverinfo="skip", showlegend=False,
    ))

    # Años intermedios: puntos apagados, cada uno es "un año más sin encuesta"
    if anios_intermedios:
        fig.add_trace(go.Scatter(
            x=anios_intermedios, y=[0] * len(anios_intermedios),
            mode="markers",
            marker=dict(size=9, color="rgba(255,255,255,0.18)"),
            hovertemplate="%{x}: sin encuesta nacional<extra></extra>",
            showlegend=False,
        ))

    # Punto de inicio: la última encuesta real
    fig.add_trace(go.Scatter(
        x=[anio_ultimo_dato], y=[0],
        mode="markers+text",
        marker=dict(size=18, color=AZUL_DEFENSA),
        text=["Última encuesta<br>(2018-2019)"], textposition="top center",
        hovertemplate=f"{anio_ultimo_dato}: última encuesta nacional de hábitos<extra></extra>",
        showlegend=False,
    ))

    # Punto final: hoy, todavía sin dato -- marcador hueco a propósito
    fig.add_trace(go.Scatter(
        x=[anio_actual], y=[0],
        mode="markers+text",
        marker=dict(size=18, color=ROJO_AMENAZA, symbol="circle-open", line=dict(width=3)),
        text=[f"Hoy ({anio_actual})<br>sin nueva medición"], textposition="top center",
        hovertemplate=f"{anio_actual}: todavía sin nueva encuesta<extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        xaxis=dict(
            tickformat="d", dtick=1,
            range=[anio_ultimo_dato - 0.6, anio_actual + 0.6],
            showgrid=False, title="",
        ),
        yaxis=dict(visible=False, range=[-1, 1.6]),
        height=200,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")


def render(datos):
    st.markdown("---")
    st.markdown('<h2 class="titulo-gap">El silencio de 7 años</h2>', unsafe_allow_html=True)

    habitos = datos[datos["metrica"].isin(METRICAS_HABITOS)].sort_values("valor")

    anio_actual = date.today().year
    anios_de_silencio = anio_actual - ULTIMO_ANIO_CON_DATO

    # Callout grande: el número que importa es "años sin nueva medición",
    # no un dato de la encuesta en sí.
    st.markdown(
        f"""
        <div style="background-color:#1a1a2e; padding:1.2rem; border-left:6px solid {ROJO_AMENAZA}; border-radius:4px;">
        <span style="font-size:2.5rem; font-weight:bold; color:{ROJO_AMENAZA};">{anios_de_silencio} años</span><br>
        <span style="color:#eaeaea;">sin una nueva encuesta nacional sobre hábitos de higiene digital en Argentina.
        La última medición disponible es de 2018-2019.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")  # espaciado
    _linea_de_tiempo(ULTIMO_ANIO_CON_DATO, anio_actual)
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
        color_discrete_sequence=[AZUL_DEFENSA],
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Fuente: Avast (2018-2019) y Kaspersky Lab / CORPA (2019). "
        "No se identificó ningún estudio nacional posterior sobre esta misma dimensión."
    )