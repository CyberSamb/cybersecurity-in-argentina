"""
panels/organizacional.py
Panel "Organizacional": exposición de las empresas.
Usa matplotlib (estático) en vez de Plotly porque cada año de PwC es una
encuesta con preguntas distintas -- no hay serie temporal que justifique
interactividad en el propio gráfico. La interactividad la da el selector
de año de Streamlit, no el chart.
"""

import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from etiquetas import etiqueta_legible
from colors import AZUL_DEFENSA, ROJO_AMENAZA
from panels import punchline


def render(datos):
    st.header("Organizacional — exposición de las empresas")
    st.caption(
        "Cada año corresponde a una encuesta PwC distinta, con preguntas propias. "
        "No son comparables entre sí como serie temporal: se muestran como fotos independientes."
    )

    # Selector de año: puebla las opciones directo desde los datos, así si el
    # día de mañana se agrega un año nuevo al CSV, aparece solo sin tocar código.
    anios_disponibles = sorted(datos["periodo_año"].unique(), reverse=True)
    anio_elegido = st.selectbox("Año del informe", anios_disponibles)

    subset = datos[datos["periodo_año"] == anio_elegido].sort_values("valor")

    etiquetas_legibles = subset["metrica"].apply(etiqueta_legible)

    fig, ax = plt.subplots(figsize=(9, max(3, len(subset) * 0.4)))
    ax.barh(etiquetas_legibles, subset["valor"], color=AZUL_DEFENSA)
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

    # --- La matriz de inconsistencia: qué pregunta existe en qué año ---
    st.subheader("La pregunta que nunca se repite")

    pivot = datos.pivot_table(index="metrica", columns="periodo_año", values="valor", aggfunc="first")
    anios_cols = sorted(pivot.columns)
    total_metricas = len(pivot)
    repetidas = (pivot.notna().sum(axis=1) > 1).sum()

    st.caption(
        f"De las {total_metricas} preguntas distintas que hizo PwC en estos {len(anios_cols)} informes, "
        f"**{repetidas}** se repitieron en más de un año. Pasá el mouse por la matriz para ver el detalle."
    )

    # Orden: metricas ordenadas por año en que aparecen, para que la matriz
    # se lea de arriba a abajo como una línea de tiempo, no al azar.
    pivot_ordenado = pivot.loc[pivot.notna().idxmax(axis=1).sort_values().index]
    etiquetas_fila = [etiqueta_legible(m) for m in pivot_ordenado.index]
    z = pivot_ordenado.notna().astype(int).values
    texto_hover = [
        [
            f"{etiquetas_fila[i]} ({anio}): {pivot_ordenado.iloc[i][anio]:.0f}%"
            if pivot_ordenado.iloc[i][anio] == pivot_ordenado.iloc[i][anio]  # not NaN
            else f"{etiquetas_fila[i]} ({anio}): no se preguntó"
            for anio in anios_cols
        ]
        for i in range(len(pivot_ordenado))
    ]

    fig_matriz = go.Figure(data=go.Heatmap(
        z=z,
        x=[str(a) for a in anios_cols],
        y=etiquetas_fila,
        text=texto_hover,
        hoverinfo="text",
        colorscale=[[0, "rgba(255,255,255,0.04)"], [1, AZUL_DEFENSA]],
        showscale=False,
        xgap=3, ygap=3,
    ))
    fig_matriz.update_layout(
        height=max(300, 24 * len(pivot_ordenado)),
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_matriz, width="stretch")

    # --- Comparador interactivo: el usuario elige qué dos años cruzar ---
    st.subheader("Compará dos años directamente")
    col_a, col_b = st.columns(2)
    with col_a:
        año_a = st.selectbox("Año A", anios_cols, index=0, key="cmp_a")
    with col_b:
        año_b = st.selectbox("Año B", anios_cols, index=len(anios_cols) - 1, key="cmp_b")

    if año_a == año_b:
        st.info("Elegí dos años distintos para comparar.")
    else:
        preguntas_a = set(pivot_ordenado[año_a].dropna().index)
        preguntas_b = set(pivot_ordenado[año_b].dropna().index)
        comunes = preguntas_a & preguntas_b

        st.markdown(f"#### {len(comunes)} pregunta{'s' if len(comunes) != 1 else ''} en común entre {año_a} y {año_b}")
        if comunes:
            for m in sorted(comunes, key=etiqueta_legible):
                st.markdown(f"- {etiqueta_legible(m)}")

        col1, col2 = st.columns(2)
        with col1:
            solo_a = sorted(preguntas_a - preguntas_b, key=etiqueta_legible)
            st.markdown(f"**Solo en {año_a}** ({len(solo_a)})")
            for m in solo_a:
                st.markdown(f"- {etiqueta_legible(m)}")
        with col2:
            solo_b = sorted(preguntas_b - preguntas_a, key=etiqueta_legible)
            st.markdown(f"**Solo en {año_b}** ({len(solo_b)})")
            for m in solo_b:
                st.markdown(f"- {etiqueta_legible(m)}")

    # --- Punchline: el hallazgo central del panel ---
    punchline.render(
        "77%",
        "de las organizaciones argentinas no está preparada para la computación cuántica, "
        "pese a que ya figura entre las cuatro amenazas para las que se sienten menos preparadas "
        "(PwC Argentina, Digital Trust Insights 2026).",
    )
    punchline.render(
        f"{repetidas} de {total_metricas}",
        "preguntas se repitieron entre los tres informes de PwC Argentina (2022, 2025, 2026). "
        "Cada edición mide algo distinto, lo que hace imposible construir una serie temporal real "
        "para el nivel Organizacional.",
        color=ROJO_AMENAZA,
    )