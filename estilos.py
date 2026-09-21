"""
estilos.py
Tipografía y espaciado del proyecto. Dos familias, un rol cada una:
Space Grotesk para títulos (carácter técnico), IBM Plex Sans para todo lo
demás (texto de cuerpo, captions, tablas). Se inyecta una sola vez desde
streamlit_app.py, apenas arranca la página.
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500&display=swap');

/* Cuerpo del texto: IBM Plex Sans en todo por default */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Títulos y headers: Space Grotesk, con más peso y letter-spacing ajustado
   para que se lea técnico sin caer en todo-mayúsculas */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

h1 {
    font-size: 2.4rem !important;
    margin-bottom: 0.2rem !important;
}

h2 {
    font-size: 1.6rem !important;
    margin-top: 2rem !important;
    margin-bottom: 0.8rem !important;
}

h3 {
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    margin-top: 1.5rem !important;
}

/* El caption bajo el título principal: un poco más de aire, tono más suave */
[data-testid="stCaptionContainer"] {
    font-family: 'IBM Plex Sans', sans-serif;
    opacity: 0.75;
}

/* Menos padding superior por default de Streamlit -- el título queda pegado arriba */
.block-container {
    padding-top: 2.5rem;
}
</style>
"""


def aplicar():
    """Inyecta el CSS una sola vez. Llamar apenas arranca streamlit_app.py."""
    st.markdown(CSS, unsafe_allow_html=True)