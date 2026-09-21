"""
panels/gubernamental.py
Panel "Gubernamental": exposición del Estado.
Plotly para la serie principal (hay continuidad real 2020-2025). Los
desgloses (sector y severidad) son dimensiones DISTINTAS entre sí -- se
separan en secciones propias para no graficarlas juntas como si fueran
categorías comparables.
"""

import streamlit as st
import plotly.express as px

from etiquetas import etiqueta_legible

METRICAS_SECTOR = [
    "incidentes_criticos_sector_estado",
    "incidentes_sector_finanzas",
    "incidentes_sector_estado_gob",
]

METRICAS_SEVERIDAD = [
    "incidentes_severidad_alta",
    "incidentes_severidad_critica",
    "incidentes_severidad_media",
    "incidentes_severidad_baja",
]


def _selector_y_barras(datos, metricas, titulo_base, key):
    """Reutilizada por sector y por severidad: mismo patrón, distinta lista de métricas."""
    subset_metricas = datos[datos["metrica"].isin(metricas)]
    anios = sorted(subset_metricas["periodo_año"].unique(), reverse=True)
    if len(anios) == 0:
        return

    anio_elegido = st.selectbox("Año", anios, key=key)
    subset = subset_metricas[subset_metricas["periodo_año"] == anio_elegido].sort_values("valor")

    fig = px.bar(
        subset,
        x="valor",
        y=subset["metrica"].apply(etiqueta_legible),
        orientation="h",
        title=f"{titulo_base} — {anio_elegido}",
        labels={"x": "Cantidad", "y": ""},
    )
    st.plotly_chart(fig, width="stretch")
    fuente = subset["fuente"].iloc[0] if len(subset) else ""
    st.caption(f"Fuente: {fuente}")


def render(datos):
    st.header("Gubernamental — exposición del Estado")

    # --- Gráfico 1: serie principal ---
    serie = datos[datos["metrica"] == "incidentes_totales_estado"].sort_values("periodo_año")
    fig1 = px.line(
        serie,
        x="periodo_año",
        y="valor",
        markers=True,
        title="Incidentes de ciberseguridad reportados al Estado argentino",
        labels={"periodo_año": "Año", "valor": "Incidentes reportados"},
    )
    fig1.update_layout(hovermode="x unified")
    st.plotly_chart(fig1, width="stretch")
    st.caption("Fuente: CERT.ar, informes anuales de gestión de incidentes.")

    # --- Gráfico 2: desglose por sector (dimensión propia) ---
    st.subheader("Desglose por sector")
    st.caption("CERT.ar no publica las mismas categorías sectoriales todos los años.")
    _selector_y_barras(datos, METRICAS_SECTOR, "Incidentes por sector", key="sector")

    # --- Gráfico 3: desglose por severidad (dimensión distinta, no comparable con sector) ---
    st.subheader("Desglose por severidad")
    st.caption("Disponible solo para los años en que CERT.ar publicó esta clasificación (2023-2025).")
    _selector_y_barras(datos, METRICAS_SEVERIDAD, "Incidentes por nivel de severidad", key="severidad")