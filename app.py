import streamlit as st
import re
import random

st.set_page_config(page_title="MovieRoute", page_icon="🍿")
st.title("🍿 Movie Picker (Fast Mode)")

# Textové pole - po stisknutí Ctrl+Enter se stránka celá znovu načte a kód se spustí
html_input = st.text_area("Vlož kód z ČSFD a stiskni Ctrl+Enter:", height=150)

if html_input:
    # 1. Najdeme filmy se 4-5 hvězdami
    pattern = r'class="film-title-name">(.+?)<\/a>.*?<span class="info">.*?(\d{4}).*?(?:<span class="info">(.*?)<\/span>)?.*?class="stars stars-([45])"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    # 2. Vyfiltrujeme balast (epizody, pořady atd.)
    clean_movies = []
    for title, year, info, stars in found_data:
        if not any(x in str(info).lower() for x in ['epizoda', 'série', 'pořad', 'záznam', 'seriál']):
            clean_movies.append(title)

    # 3. Pokud máme seznam, hned jeden vybereme
    if clean_movies:
        vybrany_film = random.choice(clean_movies)
        
        st.balloons()
        st.markdown("---")
        st.subheader("🎬 Tvůj film na dnešek:")
        st.code(vybrany_film, language=None) # Zobrazí název ve velkém bloku, co jde snadno kopírovat
        st.markdown("---")
        
        # Pro jistotu vypíšeme i zbytek, abys viděla, z čeho se vybíralo
        with st.expander("Zobrazit všechny nalezené filmy"):
            st.write(", ".join(clean_movies))
    else:
        st.error("Žádné filmy se 4-5* nebyly nalezeny. Zkus zkontrolovat, jestli jsi vložila správný kód.")
