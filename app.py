import streamlit as st
import re
import random
import urllib.parse

st.set_page_config(page_title="Movie Explorer", page_icon="🕵️‍♀️")
st.title("🕵️‍♀️ Movie Explorer: Najdi něco nového")

text = st.text_area("Vlož zdrojový kód (Ctrl+U):", height=150)

if text:
    # Hledáme název a ID filmu (např. /film/10134-rivalove/)
    pattern = r'href="(/film/(.+?)/)".+?class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"'
    data = re.findall(pattern, text, re.DOTALL)
    
    filmy = []
    for link, slug, title, stars in data:
        t_clean = title.strip()
        if not any(x in t_clean.lower() for x in ["epizoda", "pořad", "série", "seriál"]):
            filmy.append((t_clean, link, slug))

    if filmy:
        vysledek_nazev, vysledek_cesta, slug = random.choice(filmy)
        
        st.write("---")
        st.subheader(f"Protože se ti líbilo: **{vysledek_nazev}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Odkaz přímo na podobné filmy na ČSFD (sekce Podobné)
            sim_link = f"https://www.csfd.cz{vysledek_cesta}podobne/"
            st.link_button("✨ Ukázat PODOBNÉ na ČSFD", sim_link, width='stretch')
            
        with col2:
            # Odkaz na Google vyhledávání tipů
            google_search = urllib.parse.quote(f"movies similar to {vysledek_nazev} reddit")
            st.link_button("🔍 Hledat tipy na Redditu/Google", f"https://www.google.com/search?q={google_search}", width='stretch')
            
        st.write("---")
        st.info("💡 **Tip:** Na ČSFD stránce 'Podobné' uvidíš filmy, které systém doporučuje k tvému oblíbenci. Tam najdeš ty novinky!")

    else:
        st.warning("V kódu nejsou žádné filmy se 4-5*. Zkus jinou stránku tvých hodnocení.")
else:
    st.write("Vlož kód a já ti pomůžu najít něco, co jsi ještě neviděla.")
