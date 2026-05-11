import streamlit as st
import re
import random
import urllib.parse
import pandas as pd

st.set_page_config(page_title="Movie Picker PRO", page_icon="🎬")

# Inicializace paměti
if 'seznam_filmu' not in st.session_state:
    st.session_state.seznam_filmu = []

st.title("🎬 Movie Picker s Pamětí")

# --- POSTRANNÍ PANEL ---
with st.sidebar:
    st.header("📊 Statistiky")
    st.write(f"V paměti uloženo: **{len(st.session_state.seznam_filmu)}** filmů")
    
    if st.button("🗑️ Vymazat vše"):
        st.session_state.seznam_filmu = []
        if 'posledni_tip' in st.session_state:
            del st.session_state.posledni_tip
        st.rerun()

# --- VKLÁDÁNÍ KÓDU ---
html_input = st.text_area("Sem vlož kód (Ctrl+U):", height=150, help="Vlož zdrojový kód z ČSFD a klikni na tlačítko níže.")

if st.button("📥 Přidat do paměti"):
    if html_input:
        bloky = re.findall(r'<tr.*?>.*?<\/tr>', html_input, re.DOTALL)
        nove_filmy_pocet = 0
        
        for blok in bloky:
            hvezdy = re.search(r'class="stars stars-([45])"', blok)
            if hvezdy:
                nazev_match = re.search(r'class="film-title-name">(.+?)<\/a>', blok)
                if nazev_match:
                    t = nazev_match.group(1).strip()
                    if not any(x in t.lower() for x in ["epizoda", "pořad", "série", "seriál"]):
                        if t not in st.session_state.seznam_filmu:
                            st.session_state.seznam_filmu.append(t)
                            nove_filmy_pocet += 1
        
        if nove_filmy_pocet > 0:
            st.success(f"Hotovo! Přidáno **{nove_filmy_pocet}** nových kousků.")
        else:
            st.warning("Žádné nové 4-5* filmy k přidání.")
    else:
        st.error("Textové pole je prázdné!")

# --- VÝBĚR FILMU ---
st.divider()
if st.button("🎲 VYBRAT NÁHODNÝ TIP", use_container_width=True):
    if st.session_state.seznam_filmu:
        st.session_state.posledni_tip = random.choice(st.session_state.seznam_filmu)
        st.balloons()
    else:
        st.error("Paměť je prázdná, není z čeho vybírat.")

if 'posledni_tip' in st.session_state:
    st.markdown(f"### 🎯 Tvůj tip: \n# 🍿 {st.session_state.posledni_tip}")
    q = urllib.parse.quote(f"{st.session_state.posledni_tip} csfd")
    st.link_button(f"🔍 Otevřít na Google", f"https://www.google.com/search?q={q}")

# --- KONTROLA SEZNAMU (Opravená verze) ---
st.divider()
with st.expander("📂 Prohlédnout uložené filmy"):
    if st.session_state.seznam_filmu:
        # Seřadíme abecedně
        serazene = sorted(st.session_state.seznam_filmu)
        
        # Přidáme vyhledávač v seznamu
        search_list = st.text_input("Hledat v mém seznamu:", placeholder="Zadej název...")
        
        if search_list:
            zobrazeno = [f for f in serazene if search_list.lower() in f.lower()]
        else:
            zobrazeno = serazene
            
        # Zobrazení pomocí tabulky (je to stabilnější než text)
        df = pd.DataFrame(zobrazeno, columns=["Název filmu"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("V paměti zatím nic není.")
