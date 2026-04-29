import streamlit as st
import re
import pandas as pd
import random

st.set_page_config(page_title="MovieRoute AI 🧠", page_icon="🎬")
st.title("🧠 MovieRoute: Podle tvého hodnocení")

st.info("Tento nástroj najde tvoje 5* pecky i bez ručního přepisování!")

with st.expander("Návod: Jak sem dostat svoje hodnocení?"):
    st.write("1. Otevři svůj profil na ČSFD (sekce Hodnocení).")
    st.write("2. Zmáčkni **Ctrl+U** (otevře se kód stránky).")
    st.write("3. Zmáčkni **Ctrl+A** a pak **Ctrl+C**.")
    st.write("4. Vlož to do pole níže.")

# Okno pro vložení zdrojového kódu
html_input = st.text_area("Vlož zdrojový kód z ČSFD sem:", height=200)

if html_input:
    # REGEX MAGIE: Hledáme názvy filmů a k nim přiřazené hvězdičky v kódu ČSFD
    # ČSFD v kódu používá třídy jako "stars-5" nebo "rating-5"
    pattern = r'class="film-title-name">(.+?)<\/a>.*?class="stars-(\d)"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    if found_data:
        df = pd.DataFrame(found_data, columns=['Film', 'Hvězdy'])
        df['Hvězdy'] = df['Hvězdy'].astype(int)
        
        # Filtrujeme jen tvoje srdcovky (4 a 5 hvězd)
        top_movies = df[df['Hvězdy'] >= 4].copy()
        
        st.success(f"Načteno! Vidím {len(df)} ohodnocených filmů. Z toho {len(top_movies)} jsou tvoje TOP kousky (4-5*).")
        
        if st.button("🎲 Doporuč mi něco na základě mých TOP filmů"):
            seed_movie = random.choice(top_movies['Film'].tolist())
            st.divider()
            st.write(f"Vycházím z tvého oblíbeného filmu: **{seed_movie}**")
            
            # Tady propojíme s vyhledáváním podobných věcí
            st.subheader("Zkus se mrknout na tyhle podobné kousky:")
            
            # Vygenerujeme odkazy na Google/YouTube pro doporučení
            col1, col2 = st.columns(2)
            with col1:
                st.link_button(f"Podobné jako {seed_movie} (Google)", f"https://www.google.com/search?q=filmy+podobné+jako+{seed_movie.replace(' ', '+')}")
            with col2:
                st.link_button("Hledat na ČSFD", f"https://www.csfd.cz/hledat/?q={seed_movie.replace(' ', '+')}")
    else:
        st.warning("V tomhle textu jsem žádná hodnocení nenašel. Ujisti se, že kopíruješ kód (Ctrl+U) ze stránky s hodnocením.")

else:
    st.info("Čekám na tvůj vložený kód ze stránky Hodnocení...")
