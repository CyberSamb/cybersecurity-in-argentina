"""
panels/footer.py
Footer metodológico: fuentes, limitaciones y declaración de uso de IA.
Se muestra siempre, en los tres niveles, al final de la página.
Las fuentes se extraen directo del CSV (no se tipean a mano) para que el
footer nunca quede desincronizado si el dataset cambia.
"""

import streamlit as st


def render(datos):
    st.markdown("---")

    with st.expander("Fuentes de datos"):
        fuentes = (
            datos[["nivel", "fuente", "url"]]
            .drop_duplicates()
            .sort_values(["nivel", "fuente"])
        )
        for nivel in ["personal", "organizacional", "gubernamental"]:
            st.markdown(f"**{nivel.capitalize()}**")
            subset = fuentes[fuentes["nivel"] == nivel]
            for _, fila in subset.iterrows():
                st.markdown(f"- [{fila['fuente']}]({fila['url']})")

    with st.expander("Limitaciones metodológicas"):
        st.markdown(
            """
            - **UFECI (Personal):** el criterio de conteo cambió de año fiscal (abril-marzo) a año
              calendario entre informes. La serie principal usa solo años calendario (2021-2024);
              el salto 2019/20→2020/21 se muestra aparte porque corresponde al período fiscal antiguo.
            - **PwC (Organizacional):** cada año (2022, 2025, 2026) es una encuesta distinta, con
              preguntas propias y alcance geográfico que cambia. Se tratan como fotos independientes,
              nunca como tendencia. En 2026, solo se usan las cifras que el propio informe confirma
              como específicas de Argentina (el resto del informe es a nivel LATAM).
            - **CERT.ar (Gubernamental):** la taxonomía de tipos de incidente se amplió a partir de
              2023; el desglose sectorial no se publicó con los mismos criterios todos los años.
            - **Hábitos de higiene digital (Personal):** no se identificó ninguna encuesta nacional
              posterior a 2018-2019 sobre esta dimensión específica — es la base del panel "El
              silencio de 7 años".
            """
        )

    with st.expander("Declaración de uso de Inteligencia Artificial"):
        st.markdown(
            """
            Se utilizó Claude (Anthropic) como herramienta de asistencia bajo supervisión directa
            del autor, en las siguientes etapas:

            - **Recolección y validación de fuentes:** verificación de cifras contra los PDFs
              originales (PwC Argentina, UFECI, CERT.ar) y detección de datos con alcance
              geográfico mal etiquetado en los informes PwC 2025/2026.
            - **Construcción y limpieza del dataset:** estructuración en formato tabular,
              normalización de formatos de fecha, documentación de limitaciones metodológicas.
            - **Desarrollo de la aplicación:** asistencia en la generación de código Python/Streamlit
              (carga de datos, navegación, visualizaciones), revisado y probado en cada paso.

            No se utilizó IA generativa para crear las visualizaciones finales de forma automatizada:
            cada gráfico fue definido, revisado y ajustado por el autor. No se generaron ni
            manipularon imágenes con IA generativa.
            """
        )

    st.caption("La ciberseguridad invisible — Concurso Nacional de Visualización de Datos 2026, Contar con Datos ⎯ por CyberSamb")