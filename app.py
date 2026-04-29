import streamlit as st
import re
import random
import urllib.parse

# Nastavení vzhledu stránky
st.set_page_config(page_title="Movie Picker", page_icon="🎬")

st.title("🎬 Movie Picker")

# Vstupní pole pro kód
html_input = st.text_area("Sem vlož kód (Ctrl+U):", height=200)

if html_input:
    # Regex hledá název filmu a informaci o hvězdách (4 nebo 5)
    pattern = r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    # Filtrace: Chceme jen čisté názvy filmů
    final_movies = []
    for title, stars in found_data:
        clean_title = title.strip()
        # Odfiltruje seriály a Jirku
        if not any(word in clean_title.lower() for word in ["epizoda", "pořad", "série", "seriál", "vysvětluje věci"]):
            final_movies.append(clean_title)

    if final_movies:
        selected_movie = random.choice(final_movies)
        
        st.divider()
        st.subheader("🎯 Tvůj tip na film:")
        st.title(f"🍿 {selected_movie}")
        
        # Odkaz na vyhledávání na ČSFD
        search_url = f"https://www.csfd.cz/vyhledavani/?q={urllib.parse.quote(selected_movie)}"
        
        st.link_button(f"🔍 Najít {selected_movie} na ČSFD", search_url)
        st.divider()
    else:
        st.error("V tomto kódu jsem nenašel žádné filmy se 4 nebo 5 hvězdami.")
else:
    st.info("Jdi na CSFD na svá hodnocení, dej Ctrl+U, vše označ, zkopíruj a vlož sem.")
