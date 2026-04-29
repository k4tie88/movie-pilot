import streamlit as st
import re
import random

# Jednoduché nastavení
st.title("🎬 Movie Picker")

# Vstupní pole
html_input = st.text_area("Vlož kód a dej Ctrl+Enter:")

if html_input:
    # Extrakce názvů filmů (hledáme cokoli s 4* nebo 5*)
    data = re.findall(r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"', html_input, re.DOTALL)
    
    # Filtrujeme jen čisté názvy, vynecháme seriálové věci
    filmy = []
    for t, s in data:
        if "epizoda" not in t.lower() and "pořad" not in t.lower() and "série" not in t.lower():
            filmy.append(t)

    if filmy:
        vysledek = random.choice(filmy)
        st.write("---")
        # Tohle vypíše pouze čistý název filmu
        st.success(f"## {vysledek}")
        st.write("---")
    else:
        st.error("V tomto kódu jsem žádné 4* nebo 5* filmy nenašel.")
else:
    st.info("Čekám na vložení textu...")
