import streamlit as st
import re
import random

st.set_page_config(page_title="MovieRoute", page_icon="🍿")
st.title("🍿 Movie Picker")

html_input = st.text_area("Vlož kód z ČSFD:", height=150)

if html_input:
    # Najde filmy, které mají 4 nebo 5 hvězdiček
    # Ignoruje epizody a pořady, aby tam neskákal Jirka nebo Bridgertonovi
    pattern = r'class="film-title-name">(.+?)<\/a>.*?<span class="info">.*?(\d{4}).*?(?:<span class="info">(.*?)<\/span>)?.*?class="stars stars-([45])"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    # Vyfiltrujeme jen ty, co v doplňujícím info nemají "epizoda", "pořad" atd.
    top_movies = []
    for title, year, info, stars in found_data:
        if not any(x in str(info).lower() for x in ['epizoda', 'pořad', 'série', 'záznam']):
            top_movies.append(title)

    if top_movies:
        st.write(f"Vybírám z tvých {len(top_movies)} nejlepších filmů...")
        
        if st.button("CO SI MÁM PUSTIT?"):
            vybrany_film = random.choice(top_movies)
            
            # Velký, jasný výsledek bez zbytečných řečí
            st.markdown(f"""
            ---
            ### 🎬 Dneska koukej na:
            # **{vybrany_film}**
            ---
            """)
    else:
        st.warning("V tomhle textu jsem nenašel žádné FILMY se 4-5 hvězdami. Zkus zkopírovat větší kus stránky.")
