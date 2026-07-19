import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

st.set_page_config(page_title="MovieRoute 🎬", page_icon="🍿")
st.title("🎬 MovieRoute")

USER_ID = "889226"

@st.cache_data(ttl=3600)  # Seznam si zapamatuje na hodinu, aby neprovokoval ČSFD
def get_watchlist(user_id):
    url = f"https://www.csfd.cz/uzivatel/{user_id}/chci-videt/"
    
    # Rozšířené hlavičky, které věrně simulují prohlížeč
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "cs-CZ,cs;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = []
        
        # Nový selektor pro názvy filmů na ČSFD
        for link in soup.select('a.film-title-name'):
            title = link.text.strip()
            path = link.get('href')
            movies.append({
                'title': title,
                'url': f"https://www.csfd.cz{path}"
            })
        return movies
    except:
        return None

st.write(f"Načítám tvůj 'Chci vidět' seznam pro uživatele: **katie88**")

if st.button("🎲 Vyber mi film na večer"):
    with st.spinner("Zkouším se nenápadně podívat na ČSFD..."):
        watchlist = get_watchlist(USER_ID)
        
    if watchlist and len(watchlist) > 0:
        film = random.choice(watchlist)
        st.balloons()
        st.divider()
        st.subheader(f"🍿 {film['title']}")
        st.link_button("Otevřít film na ČSFD ↗", film['url'])
    else:
        st.error("ČSFD nás stále blokuje. 🛑")
        st.info("Zkus aplikaci restartovat (vpravo nahoře v menu 'Clear cache' nebo 'Rerun'). Pokud to nepomůže, ČSFD dočasně zablokovalo adresu, na které běží Streamlit.")
