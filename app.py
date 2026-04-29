import streamlit as st
import re
import random

# Základní konfigurace stránky
st.set_page_config(page_title="MovieRoute", page_icon="🎬")

st.title("🎬 Movie Picker")

# 1. Vstupní pole
html_input = st.text_area("Vlož kód a stiskni Ctrl+Enter:", height=150, placeholder="Sem vlož ten zkopírovaný text...")

# 2. Logika zpracování (běží automaticky po Ctrl+Enter)
if html_input:
    # Regex hledá název filmu a hvězdičky 4 nebo 5
    # Bere v úvahu tvou tabulku z ČSFD
    pattern = r'class="film-title-name">(.+?)<\/a>.*?<span class="info">.*?(\d{4}).*?(?:<span class="info">(.*?)<\/span>)?.*?class="stars stars-([45])"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    # Filtrace balastu
    filmy = []
    for t, y, info, s in found_data:
        infostr = str(info).lower()
        if "epizoda" not in infostr and "pořad" not in infostr and "série" not in infostr:
            filmy.append(t)

    # 3. Okamžitý výsledek
    if filmy:
        vyber = random.choice(filmy)
        
        st.markdown("---")
        st.success("Filmy načteny! Tvůj tip na večer:")
        
        # Obří nápis bez zbytečných řečí
        st.write(f"## 🏆 {vyber}")
        
        st.markdown("---")
        
        # Malá pojistka - seznam všech nalezených pro kontrolu
        with st.expander("Seznam všech tvých 4-5* filmů"):
            st.write(", ".join(filmy))
    else:
        st.warning("Vložený text neobsahuje žádné FILMY se 4-5 hvězdami. Zkus to znovu.")
else:
    st.info("Čekám na vložení kódu...")
