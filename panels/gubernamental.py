"""
panels/gubernamental.py
Panel "Gubernamental": exposición del Estado.
Plotly para la serie principal (hay continuidad real 2020-2024, a diferencia
de Organizacional). El desglose por sector usa selector de año porque CERT.ar
no reporta las mismas categorías todos los años. A tener en cuenta :)
"""

import streamlit as st
import plotly.express as px

from etiquetas import etiqueta_legible


def render(datos):
    st.header("Gubernamental — exposición del Estado")

    # --- Gráfico 1: serie principal, incidentes totales 2020-2024 ---
    serie = datos[
        datos["metrica"] == "incidentes_totales_estado"
    ].sort_values("periodo_año")

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
    st.caption("Fuente: CERT.ar, informes de gestión anuales.")

    # --- Gráfico 2: desglose por sector ---
    # Solo existe desglose para los años en que CERT.ar lo publicó con esa
    # granularidad (2022 y 2024, con categorías distintas entre sí).
    desglose = datos[datos["metrica"] != "incidentes_totales_estado"]
    anios_con_desglose = sorted(desglose["periodo_año"].unique(), reverse=True)

    if len(anios_con_desglose) == 0:
        return  # nada más que mostrar si no hay desglose cargado

    st.subheader("Desglose por sector")
    st.caption(
        "CERT.ar no publica las mismas categorías todos los años, "
        "por eso el desglose se muestra año por año en vez de como serie."
    )
    anio_elegido = st.selectbox("Año del desglose", anios_con_desglose)
    subset = desglose[desglose["periodo_año"] == anio_elegido].sort_values("valor")

    fig2 = px.bar(
        subset,
        x="valor",
        y=subset["metrica"].apply(etiqueta_legible),
        orientation="h",
        title=f"Desglose de incidentes — {anio_elegido}",
        labels={"x": "Cantidad / %", "y": ""},
    )
    st.plotly_chart(fig2, width="stretch")

    fuente = subset["fuente"].iloc[0] if len(subset) else ""
    st.caption(f"Fuente: {fuente}")