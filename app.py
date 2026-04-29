import streamlit as st
import re
import random

st.set_page_config(page_title="Movie Picker")
st.title("🎬 Movie Picker")

# Jednoduchý vstup
text_vstup = st.text_area("Vlož kód z ČSFD:")

if text_vstup:
    # Najde názvy u 4* a 5* hodnocení
    filmy = re.findall(r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-[45]"', text_vstup, re.DOTALL)
    
    # Odfiltruje balast
    ciste_filmy = [f.strip() for f in filmy if not any(x in f.lower() for x in ["epizoda", "pořad", "série"])]

    if ciste_filmy:
        st.divider()
        st.header(f"🍿 Zkus: {random.choice(ciste_filmy)}")
        st.divider()
    else:
        st.warning("Žádné filmy nenalezeny.")
