import streamlit as st
import re
import random
import urllib.parse

# Nastavení vzhledu stránky
st.set_page_config(page_title="Movie Picker", page_icon="🎬")

st.title("🎬 Movie Picker")
st.markdown("Vlož zdrojový kód tvých hodnocení z ČSFD a já ti vyberu film na večer.")

# Vstupní pole pro kód (Ctrl+U -> Ctrl+A -> Ctrl+C)
html_input = st.text_area("Sem vlož kód (Ctrl+U):", height=200, placeholder="Pravým na ČSFD -> Zobrazit zdrojový kód stránky...")

if html_input:
    # Regex hledá název filmu a informaci o tom, zda má 4 nebo 5 hvězd
    # Hvězdičky na ČSFD jsou v kódu jako 'stars-4' nebo 'stars-5'
    pattern = r'class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    # Filtrace: Chceme jen čisté názvy filmů a vyhazujeme balast (epizody, pořady)
    final_movies = []
    for title, stars in found_data:
        clean_title = title.strip()
        # Seznam slov, která nechceme v názvu (odfiltruje seriály a Jirku)
        if not any(word in clean_title.lower() for word in ["epizoda", "pořad", "série", "seriál", "vysvětluje věci"]):
            final_movies.append(clean_title)

    if final_movies:
        # Náhodný výběr jednoho filmu
        selected_movie = random.choice(final_movies)
        
        st.divider()
        st.subheader("🎯 Můj tip pro tebe:")
        st.title(f"🍿 {selected_movie}")
        
        # Vytvoření bezpečného odkazu na vyhledávání na ČSFD
        # Tím se vyhneme chybě 404 (Upsy-daisy)
        search_url = f"https://www.csfd.cz/vyhledavani/?q={urllib.parse.quote(selected_movie)}"
        
        st.link_button(f"🔍 Najít '{selected_movie}' na ČSFD", search_url)
        
        st.caption(f"Vybíral jsem z {len(final_movies)} tvých oblíbených filmů na této stránce.")
        st.divider()
    else:
        st.error("V tomto kódu jsem nenašel žádné FILMY se 4 nebo 5 hvězdami. Ujisti se, že kopíruješ zdrojový kód (Ctrl+U).")
else:
    st.info("💡 **Nápověda:** Jdi na ČSFD na svá hodnocení, dej **Ctrl+U**, pak všechno označ (**Ctrl+A**
