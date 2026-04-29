import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random

st.set_page_config(page_title="MovieRoute 🎬", page_icon="🍿")
st.title("🎬 MovieRoute")

# ID tvého profilu z odkazu
USER_ID = "889226"

def get_watchlist(user_id):
    # Tohle je adresa tvého seznamu "Chci vidět"
    url = f"https://www.csfd.cz/uzivatel/{user_id}/chci-videt/"
    
    # ČSFD vyžaduje "User-Agent", aby si nemyslelo, že jsme zlý robot
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Najdeme všechny filmy v seznamu
    movies = []
    # ČSFD používá pro názvy filmů třídu 'film-title-name'
    for link in soup.select('.film-title-name'):
        title = link.text.strip()
        path = link.get('href')
        movies.append({
            'title': title,
            'url': f"https://www.csfd.cz{path}"
        })
    return movies

st.write(f"Načítám tvůj 'Chci vidět' seznam pro uživatele: **katie88**")

if st.button("🎲 Vyber mi film na večer"):
    with st.spinner("Slídím na ČSFD..."):
        watchlist = get_watchlist(USER_ID)
        
    if watchlist:
        film = random.choice(watchlist)
        st.balloons()
        st.divider()
        st.subheader(f"🍿 {film['title']}")
        st.link_button("Kouknout na ČSFD ↗", film['url'])
    else:
        st.error("Nepodařilo se načíst tvůj seznam. ČSFD nás možná na chvíli zablokovalo, zkus to za moment.")

st.info("Poznámka: Tento scraper zatím bere jen první stránku tvého seznamu. Pokud jich chceš víc, museli bychom to nechat 'prolézat' déle.")