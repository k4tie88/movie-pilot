import streamlit as st
import re
import random

st.set_page_config(page_title="MovieRoute", page_icon="🎬")
st.title("🎬 Movie Picker")

# Vstupní pole
html_input = st.text_area("Vlož kód a stiskni Ctrl+Enter:", height=150)

if html_input:
    # Najde názvy u 4* a 5* hodnocení
    pattern = r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"'
    found = re.findall(pattern, html_input, re.DOTALL)
    
    # Vyfiltruje pryč epizody a pořady, aby zbyl jen čistý název filmu
    filmy = [t for t, s in found if not any(x in t.lower() for x in ["epizoda", "pořad", "série"])]

    if filmy:
        vyber = random.choice(filmy)
        st.markdown("---")
        st.subheader("Dneska koukej na:")
        # Tohle vypíše jen čistý název filmu velkým písmem
        st.info(f"### {vyber}")
        st.markdown("---")
    else:
        st.warning("V tomhle textu jsem nenašel žádné 4* nebo 5* filmy.")
else:
    st.write("Vlož kód z ČSFD a potvrď ho pomocí Ctrl+Enter.")
