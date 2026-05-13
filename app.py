import streamlit as st
import re
import random
import urllib.parse

st.set_page_config(page_title="Hidden Gems Finder", page_icon="💎")

# --- DATABÁZE SKRYTÝCH KLENOTŮ A KVALITNÍCH MÉNĚ ZNÁMÝCH FILMŮ ---
# Tento seznam můžeš dál rozšiřovat. Jsou tu věci, co mají úroveň, ale nejsou to "Avengers".
HIDDEN_GEMS = [
    "Pozemský muž", "Díra", "Co děláme v temnotách", "Sama v noci domů kráčím",
    "Humr", "Zabití posvátného jelena", "První reformovaná", "Věčný svit neposkvrněné mysli",
    "Ex Machina", "Pí", "Nepřítel", "Noční zvířata", "Trestanec", "Wind River",
    "Sicario: Nájemný vrah", "Příchozí", "Slunovrat", "Čarodějnice", "Maják",
    "Dobrý časy", "Uncut Gems", "Florida Project", "Kapitán Fantastický",
    "Whiplash", "Vykolejená", "Sing Street", "Frank", "Musíme si promluvit o Kevinovi",
    "Svědek", "Zmizení", "Úkryt", "Pevnost", "Pouto", "V kůži Johna Malkoviche",
    "Adaptace", "Magnolia", "Synekdocha, New York", "Oldboy", "Viděl jsem ďábla",
    "Zátah: Vykoupení", "Kluk od vedle", "Nikdy jsi tu nebyl", "Drive", 
    "Neon Demon", "Pod kůží", "Anihilace", "Stoker", "Sněhurka", "Victoria",
    "Oni", "Vstup do prázdna", "Climax", "Zvrácený", "Holy Motors", "Svišti",
    "Incendies", "Královna", "Kód Enigmy", "Teorie všeho", "Loni v Marienbadu",
    "Persona", "U konce s dechem", "Sedm samurajů", "Hrob světlušek", "Hon",
    "Rozchod Nadera a Simin", "Zloději krámů", "Zlaté časy na Ridgemont High"
]

if 'shlednuto' not in st.session_state:
    st.session_state.shlednuto = set()

st.title("💎 Hledač skrytých klenotů")
st.write("Doporučím ti kvalitní, méně známé filmy, které **nemáš v seznamu**.")

# --- TVŮJ SEZNAM (Z ČSFD) ---
with st.expander("📥 Nahrát moje viděné filmy (Ctrl+U)"):
    html_input = st.text_area("Vlož kód z ČSFD:", height=150)
    if st.button("Aktualizovat moji databázi"):
        if html_input:
            titles = re.findall(r'class="film-title-name">(.+?)<\/a>', html_input)
            for t in titles:
                st.session_state.shlednuto.add(t.strip())
            st.success(f"Vím o {len(st.session_state.shlednuto)} filmech, co jsi viděla.")

# --- LOGIKA DOPORUČENÍ ---
st.divider()

if st.button("🔍 NAJDI SKRYTÝ KLENOT", use_container_width=True):
    # Najdeme ty, co v seznamu NEJSOU
    nove_kousky = [f for f in HIDDEN_GEMS if f not in st.session_state.shlednuto]
    
    if nove_kousky:
        vysledek = random.choice(nove_kousky)
        st.balloons()
        st.markdown(f"### Tohle by tě mohlo bavit: \n# 🎥 {vysledek}")
        
        q = urllib.parse.quote(f"{vysledek} csfd")
        st.link_button(f"🔎 Podívat se, o čem to je (Google)", f"https://www.google.com/search?q={q}")
        
        st.info("Tento film je v mém seznamu doporučených, ale ve tvém seznamu viděných chybí.")
    else:
        st.warning("Vypadá to, že jsi viděla všechny klenoty z mého aktuálního výběru! Musím jich přidat víc.")

# Statistiky v panelu
st.sidebar.write(f"V tvém blacklistu je: **{len(st.session_state.shlednuto)}** filmů.")
