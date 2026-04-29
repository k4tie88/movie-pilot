import streamlit as st
import re
import random

st.title("🎬 Movie Picker")

# Vstupní pole bez zbytečností
html_input = st.text_area("Vlož kód a stiskni Ctrl+Enter:", height=200)

if html_input:
    # Hledáme názvy u 4* a 5* (včetně ošetření speciálních znaků)
    data = re.findall(r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"', html_input, re.DOTALL)
    
    # Filtrace: pouze filmy (vynecháme balast)
    filmy = []
    for t, s in data:
        t_clean = t.strip()
        if not any(x in t_clean.lower() for x in ["epizoda", "pořad", "série", "seriál"]):
            filmy.append(t_clean)

    if filmy:
        vysledek = random.choice(filmy)
        st.write("---")
        st.subheader("Tvůj tip na film:")
        # Obří text, aby nešel přehlédnout
        st.title(f"🍿 {vysledek}")
        st.write("---")
        st.write(f"Vybíral jsem z celkem {len(filmy)} tvých oblíbených filmů.")
    else:
        st.warning("V tomhle textu jsem nenašel žádné filmy se 4 nebo 5 hvězdami.")
else:
    st.info("Aplikace je připravena. Vlož kód z ČSFD a potvrď ho.")
