import streamlit as st
import re
import random
import urllib.parse

st.set_page_config(page_title="Movie Picker", page_icon="🎬")
st.title("🎬 Movie Picker")

text = st.text_area("Vlož zdrojový kód (Ctrl+U) a stiskni Ctrl+Enter:", height=200)

if text:
    # Hledáme název filmu a ID filmu pro vytvoření odkazu
    # Pattern: najde odkaz (href) a název filmu u 4-5 hvězdiček
    pattern = r'href="(/film/.+?/)".+?class="film-title-name">(.+?)<\/a>.*?class="stars stars-([45])"'
    data = re.findall(pattern, text, re.DOTALL)
    
    filmy = []
    for link, title, stars in data:
        t_clean = title.strip()
        # Odfiltrujeme seriálový balast
        if not any(x in t_clean.lower() for x in ["epizoda", "pořad", "série", "seriál"]):
            filmy.append((t_clean, link))

    if filmy:
        vysledek_nazev, vysledek_cesta = random.choice(filmy)
        full_link = f"https://www.csfd.cz{vysledek_cesta}"
        
        st.write("---")
        st.subheader("Dneska si dej opáčko nebo hledej podobné u:")
        
        # Velký nadpis, který je zároveň odkazem
        st.markdown(f"## 🍿 [{vysledek_nazev}]({full_link})")
        
        st.info("💡 Klikni na název výše – otevře se ti profil filmu na ČSFD.")
        st.write("---")
        
        # Bonus: Tlačítko pro rychlé hledání podobných filmů na Google
        google_search = urllib.parse.quote(f"filmy podobné filmu {vysledek_nazev}")
        st.write(f"🔍 [Najít podobné filmy na Google](https://www.google.com/search?q={google_search})")
    else:
        st.warning("V tomto kódu jsem nenašel žádné 4-5* filmy. Jsi si jistá, že jsi zkopírovala Ctrl+U?")
else:
    st.info("Vlož kód a uvidíš tip i s odkazem.")
