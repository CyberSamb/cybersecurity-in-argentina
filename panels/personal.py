"""
panels/personal.py
Panel "Personal": exposición de la ciudadanía.
Se utiliza Plotly para crear interactividad con las información
"""

import re
import streamlit as st
import plotly.express as px


def _es_anio_calendario_puro(periodo: str) -> bool:
    """True solo para '2021', '2022', etc. -- False para '2019-2020' (fiscal) o '~2021' (aprox)."""
    return bool(re.fullmatch(r"\d{4}", str(periodo)))


def render(datos):
    st.header("Personal — exposición de la ciudadanía")

    # --- Gráfico 1: serie principal de reportes a UFECI, años calendario ---
    # Se filtra explícitamente a periodos "puros" (ej. "2021") para no mezclar
    # con los periodos fiscales (ej. "2020-2021"), que usan un criterio de
    # corte distinto (abril-marzo) y no son comparables punto a punto.
    serie = datos[
        (datos["metrica"] == "reportes_delitos_informaticos")
        & (datos["periodo"].apply(_es_anio_calendario_puro))
    ].sort_values("periodo_año")

    fig1 = px.line(
        serie,
        x="periodo_año",
        y="valor",
        markers=True,
        title="Reportes de delitos informáticos recibidos por UFECI (año calendario)",
        labels={"periodo_año": "Año", "valor": "Reportes recibidos"},
    )
    fig1.update_layout(hovermode="x unified")
    st.plotly_chart(fig1, width="stretch")
    st.caption("Fuente: UFECI, informes de gestión anuales. Ver fuente exacta por dato en la tabla de metodología.")

    # --- Callout: salto pre/post-pandemia (periodo fiscal, no calendario) ---
    # Estos dos valores NO pertenecen a la serie de arriba: son período fiscal
    # abr-mar, no año calendario. Se muestran aparte para no falsear la tendencia.
    st.subheader("El salto de la pandemia (período fiscal abr-mar)")
    fiscal_pre = datos[datos["periodo"] == "2019-2020"]["valor"].values
    fiscal_post = datos[datos["periodo"] == "2020-2021"]["valor"].values

    if len(fiscal_pre) and len(fiscal_post):
        col1, col2 = st.columns(2)
        col1.metric("Abr 2019 - Mar 2020", f"{int(fiscal_pre[0]):,}".replace(",", "."))
        variacion = (fiscal_post[0] - fiscal_pre[0]) / fiscal_pre[0] * 100
        col2.metric(
            "Abr 2020 - Mar 2021",
            f"{int(fiscal_post[0]):,}".replace(",", "."),
            delta=f"+{variacion:.0f}%",
        )
        st.caption("Período fiscal (abril a marzo), distinto del año calendario del gráfico anterior. Fuente: UFECI, Informe de gestión 2020 (ed. 2021).")

    # --- Gráfico 2: tasa de victimización autopercibida ---
    victimas = datos[
        datos["metrica"] == "pct_usuarios_victimas_hackeo_fraude"
    ].sort_values("periodo_año")

    fig2 = px.bar(
        victimas,
        x="periodo",
        y="valor",
        title="% de usuarios que dice haber sido víctima de hackeo o fraude",
        labels={"periodo": "Período", "valor": "% de encuestados"},
    )
    st.plotly_chart(fig2, width="stretch")
    st.caption("Fuente: D'Alessio IROL / CertiSur, Encuesta de seguridad digital (series anuales, encuestas independientes entre sí).")