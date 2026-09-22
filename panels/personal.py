"""
panels/personal.py
Panel "Personal": exposición de la ciudadanía.
Usa Plotly porque estos gráficos necesitan interactividad real (hover, zoom)
sobre series temporales -- a diferencia del panel Organizacional, que son
snapshots estáticos sin serie que recorrer.
"""

import re
import streamlit as st
import plotly.express as px

from panels import gap_habitos
from colors import ROJO_AMENAZA


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
        color_discrete_sequence=[ROJO_AMENAZA],
    )
    fig1.update_layout(hovermode="x unified")
    fig1.update_xaxes(tickformat="d", dtick=1)
    st.plotly_chart(fig1, width="stretch")
    st.caption("Fuente: UFECI, informes de gestión anuales. Ver fuente exacta por dato en la tabla de metodología.")

    # --- Callout: salto pre/post-pandemia (periodo fiscal, no calendario) ---
    # Estos dos valores NO pertenecen a la serie de arriba: son período fiscal
    # abr-mar, no año calendario. Se muestran aparte para no falsear la tendencia.
    st.subheader("El salto de la pandemia (período fiscal abr-mar)")
    fiscal_pre = datos[datos["periodo"] == "2019-2020"]["valor"].values
    fiscal_post = datos[datos["periodo"] == "2020-2021"]["valor"].values

    if len(fiscal_pre) and len(fiscal_post):
        variacion = (fiscal_post[0] - fiscal_pre[0]) / fiscal_pre[0] * 100
        valor_pre = f"{int(fiscal_pre[0]):,}".replace(",", ".")
        valor_post = f"{int(fiscal_post[0]):,}".replace(",", ".")

        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; justify-content:center; gap:2.5rem; padding:0.5rem 0; flex-wrap:wrap;">
                    <div style="text-align:center;">
                        <div style="font-size:0.9rem; opacity:0.7;">Abr 2019 - Mar 2020</div>
                        <div style="font-size:2.6rem; font-weight:700; font-family:'Space Grotesk',sans-serif;">{valor_pre}</div>
                        <div style="font-size:0.95rem; visibility:hidden;">placeholder</div>
                    </div>
                    <div style="font-size:2rem; opacity:0.5;">→</div>
                    <div style="text-align:center;">
                        <div style="font-size:0.9rem; opacity:0.7;">Abr 2020 - Mar 2021</div>
                        <div style="font-size:2.6rem; font-weight:700; font-family:'Space Grotesk',sans-serif;">{valor_post}</div>
                        <div style="color:#3dd68c; font-size:0.95rem;">↑ +{variacion:.0f}%</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
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
        color_discrete_sequence=[ROJO_AMENAZA],
    )
    fig2.update_xaxes(type="category")
    st.plotly_chart(fig2, width="stretch")
    st.caption("Fuente: D'Alessio IROL / CertiSur, Encuesta de seguridad digital (series anuales, encuestas independientes entre sí).")

    # --- Sección destacada: el gap de 7 años en encuestas de hábitos ---
    gap_habitos.render(datos)