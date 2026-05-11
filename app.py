import streamlit as st
import re
import random
import urllib.parse
import pandas as pd

st.set_page_config(page_title="Movie Picker - Full DB", page_icon="🎬")

# Inicializace paměti jako slovníku (název: počet hvězd)
if 'databaze_filmu' not in st.session_state:
    st.session_state.databaze_filmu = {}

st.title("🎬 Movie Picker: Kompletní Databáze")

# --- POSTRANNÍ PANEL ---
with st.sidebar:
    st.header("📊 Statistiky")
    vsechny = len(st.session_state.databaze_filmu)
    # Spočítáme, kolik je v paměti těch kvalitních (4-5*)
    kvalitni = [n for n, h in st.session_state.databaze_filmu.items() if h in ['4', '5']]
    
    st.write(f"Celkem v databázi: **{vsechny}**")
    st.write(f"Z toho s hodnocením 4-5*: **{len(kvalitni)}**")
    
    if st.button("🗑️ Vymazat vše"):
        st.session_state.databaze_filmu = {}
        if 'posledni_tip' in st.session_state:
            del st.session_state.posledni_tip
        st.rerun()

# --- VKLÁDÁNÍ KÓDU ---
html_input = st.text_area("Sem vlož kód (Ctrl+U):", height=150)

if st.button("📥 Přidat/Aktualizovat databázi"):
    if html_input:
        # Najdeme všechny řádky tabulky
        bloky = re.findall(r'<tr.*?>.*?<\/tr>', html_input, re.DOTALL)
        nove_zaznamy = 0
        
        for blok in bloky:
            # Najdeme název filmu
            nazev_match = re.search(r'class="film-title-name">(.+?)<\/a>', blok)
            # Najdeme hodnocení (0-5 nebo odpad)
            hvezdy_match = re.search(r'class="stars stars-([0-5])"', blok)
            odpad_match = re.search(r'class="stars stars-0"', blok) or "odpad" in blok.lower()
            
            if nazev_match:
                t = nazev_match.group(1).strip()
                # Určíme hodnotu (0-5), pokud je to odpad, dáme 0
                h = hvezdy_match.group(1) if hvezdy_match else ("0" if "stars-0" in blok else "N/A")
                
                # Odfiltrujeme seriálový balast
                if not any(x in t.lower() for x in ["epizoda", "pořad", "série", "seriál"]):
                    # Uložíme do slovníku (přepíše staré, pokud tam bylo)
                    if t not in st.session_state.databaze_filmu:
                        nove_zaznamy += 1
                    st.session_state.databaze_filmu[t] = h
        
        st.success(f"Aktualizováno! Celkem máš v paměti už {len(st.session_state.databaze_filmu)} záznamů.")
    else:
        st.error("Pole je prázdné!")

# --- VÝBĚR FILMU ---
st.divider()
if st.button("🎲 CHCI DOPORUČIT NĚCO DOBRÉHO (4-5*)", use_container_width=True):
    # Vybereme jen ty, co mají 4 nebo 5 hvězd
    adepti = [n for n, h in st.session_state.databaze_filmu.items() if h in ['4', '5']]
    
    if adepti:
        st.session_state.posledni_tip = random.choice(adepti)
        st.balloons()
    else:
        st.error("V databázi nemáš žádné filmy se 4 nebo 5 hvězdičkami!")

if 'posledni_tip' in st.session_state:
    st.markdown(f"### 🎯 Tip pro tebe: \n# 🍿 {st.session_state.posledni_tip}")
    q = urllib.parse.quote(f"{st.session_state.posledni_tip} csfd")
    st.link_button(f"🔍 Otevřít na Google", f"https://www.google.com/search?q={q}")

# --- PROHLÍŽENÍ ---
st.divider()
with st.expander("📂 Kompletní seznam tvé databáze"):
    if st.session_state.databaze_filmu:
        # Převedeme slovník na tabulku
        seznam = [{"Film": n, "Hvězdy": h} for n, h in st.session_state.databaze_filmu.items()]
        df = pd.DataFrame(seznam).sort_values(by="Film")
        
        search = st.text_input("Hledat konkrétní film:")
        if search:
            df = df[df['Film'].str.contains(search, case=False)]
            
        st.dataframe(df, use_container_width=True, hide_index=True)
