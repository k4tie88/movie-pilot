import streamlit as st
import re
import random
import urllib.parse

# 1. Nastavení stránky a inicializace "Paměti"
st.set_page_config(page_title="Movie Picker s Pamětí", page_icon="🎬")

if 'seznam_filmu' not in st.session_state:
    st.session_state.seznam_filmu = []

st.title("🎬 Movie Picker s Pamětí")
st.markdown("""
Tato verze umí posbírat filmy z více stránek ČSFD najednou. 
Postupně vkládej kód z různých stránek svých hodnocení.
""")

# 2. Postranní panel s informacemi
with st.sidebar:
    st.header("📊 Moje paměť")
    st.write(f"Aktuálně uloženo filmů: **{len(st.session_state.seznam_filmu)}**")
    if st.button("🗑️ Vymazat celou paměť"):
        st.session_state.seznam_filmu = []
        st.rerun()

# 3. Vstup pro kód
html_input = st.text_area("Sem vlož kód z jedné stránky (Ctrl+U):", height=200)

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Přidat tyto filmy do paměti"):
        if html_input:
            # Hledáme bloky v tabulce, abychom se vyhnuli odpadu a reklamám
            bloky = re.findall(r'<tr.*?>.*?<\/tr>', html_input, re.DOTALL)
            nove_filmy = 0
            
            for blok in bloky:
                # Chceme jen 4* a 5*
                hvezdy = re.search(r'class="stars stars-([45])"', blok)
                if hvezdy:
                    nazev_match = re.search(r'class="film-title-name">(.+?)<\/a>', blok)
                    if nazev_match:
                        t = nazev_match.group(1).strip()
                        # Filtr na seriály
                        if not any(x in t.lower() for x in ["epizoda", "pořad", "série", "seriál"]):
                            if t not in st.session_state.seznam_filmu:
                                st.session_state.seznam_filmu.append(t)
                                nove_filmy += 1
            
            if nove_filmy > 0:
                st.success(f"Přidáno {nove_filmy} nových filmů!")
            else:
                st.warning("Na této stránce jsem nenašel žádné nové 4-5* filmy.")
        else:
            st.error("Nejdřív sem něco vlož!")

with col2:
    if st.button("🎲 VYBRAT NÁHODNÝ FILM"):
        if st.session_state.seznam_filmu:
            tip = random.choice(st.session_state.seznam_filmu)
            st.balloons()
            st.session_state.posledni_tip = tip
        else:
            st.error("Paměť je prázdná! Nejdřív přidej nějaké filmy.")

# 4. Zobrazení výsledku
if 'posledni_tip' in st.session_state:
    st.divider()
    st.subheader("🎯 Tvůj tip na večer:")
    st.title(f"🍿 {st.session_state.posledni_tip}")
    
    query = urllib.parse.quote(f"{st.session_state.posledni_tip} csfd")
    st.link_button(f"🔍 Najít '{st.session_state.posledni_tip}' na Google/ČSFD", f"https://www.google.com/search?q={query}")
    st.divider()

# Bonus: Seznam uložených filmů (pro kontrolu)
if st.checkbox("Ukázat seznam všech uložených filmů"):
    st.write(st.session_state.seznam_filmu)
