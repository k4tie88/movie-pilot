import streamlit as st
import re
import random

st.title("🎬 Movie Picker")

# Jednoduché pole bez zbytečných funkcí
html_input = st.text_area("Vlož kód a dej Ctrl+Enter:")

if html_input:
    # Hledáme jen názvy u 4* a 5* hodnocení
    pattern = r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"'
    found = re.findall(pattern, html_input, re.DOTALL)
    
    # Seznam jen pro filmy (vyhazujeme epizody a pořady)
    filmy = [t for t, s in found if "epizoda" not in t.lower() and "pořad" not in t.lower()]

    if filmy:
        tip = random.choice(filmy)
        st.write("---")
        st.header(f"Dneska koukej na: {tip}")
        st.write("---")
    else:
        st.error("Žádné 4-5* filmy nenalezeny.")
