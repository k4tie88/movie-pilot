import streamlit as st
import re
import pandas as pd
import random

st.set_page_config(page_title="MovieRoute AI 🧠", page_icon="🎬")
st.title("🎬 MovieRoute: Katie88 Edition")

st.markdown("""
Vlož do pole níže ten text, co jsi mi poslala (celý ten blok začínající `table class...`).
""")

html_input = st.text_area("Vlož zdrojový kód sem:", height=300)

if html_input:
    # Upravený regulární výraz přímo pro ČSFD tabulku
    # Hledá název filmu a počet hvězdiček nebo "odpad!"
    pattern = r'class="film-title-name">(.+?)<\/a>.*?class="stars (?:stars-(\d)|(trash))"'
    found_data = re.findall(pattern, html_input, re.DOTALL)
    
    parsed_movies = []
    for title, stars, trash in found_data:
        rating = 0 if trash else int(stars)
        parsed_movies.append({"Film": title, "Hvězdy": rating})

    if parsed_movies:
        df = pd.DataFrame(parsed_movies)
        st.success(f"✅ Úspěch! Načetl jsem {len(df)} tvých hodnocení.")
        
        # Zobrazení statistik
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Průměrné hodnocení", f"{df['Hvězdy'].mean():.1f} / 5")
        with col2:
            top_count = len(df[df['Hvězdy'] >= 4])
            st.metric("Srdcovky (4-5*)", top_count)

        st.dataframe(df, use_container_width=True)
        
        # Doporučovací algoritmus "Katie-Logic"
        st.divider()
        st.subheader("🤖 AI doporučení na večer")
        
        if st.button("Vygenerovat tip podle mého vkusu"):
            favorites = df[df['Hvězdy'] >= 4]['Film'].tolist()
            if favorites:
                tip = random.choice(favorites)
                st.balloons()
                st.info(f"Dneska bys mohla dát něco v podobném duchu jako: **{tip}**")
    else:
        st.error("Chyba: V tomhle textu jsem nenašel žádné filmy. Zkus zkopírovat ten velký blok znovu.")
