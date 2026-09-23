"""
panels/punchline.py
Callout de "número grande + una frase" -- el hallazgo central de un panel.
"""

import streamlit as st

from colors import ROJO_AMENAZA


def render(valor_grande: str, texto: str, color: str = ROJO_AMENAZA):
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="text-align:center; padding:0.6rem 1rem;">
                <div style="font-size:3rem; font-weight:700; font-family:'Space Grotesk',sans-serif; color:{color};">
                    {valor_grande}
                </div>
                <div style="font-size:1.05rem; opacity:0.85; max-width:34rem; margin:0.2rem auto 0;">
                    {texto}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )