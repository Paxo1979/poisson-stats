import os
import json
import requests
from bs4 import BeautifulSoup

os.makedirs('dati', exist_ok=True)

LEGHE = {
    "serie_a": {"nome": "Serie A", "url": "https://fbref.com/it/scomps/11/Campionato-di-Serie-A-Statistiche"},
    "premier_league": {"nome": "Premier League", "url": "https://fbref.com/it/scomps/9/Premier-League-Statistiche"},
    "la_liga": {"nome": "La Liga", "url": "https://fbref.com/it/scomps/12/La-Liga-Statistiche"},
    "bundesliga": {"nome": "Bundesliga", "url": "https://fbref.com/it/scomps/20/Bundesliga-Statistiche"},
    "ligue_1": {"nome": "Ligue 1", "url": "https://fbref.com/it/scomps/13/Ligue-1-Statistiche"}
}

dati_finali = {}
headers = {'User-Agent': 'Mozilla/5.0'}

for chiave, info in LEGHE.items():
    dati_finali[chiave] = {
        "nome_lega": info["nome"],
        "squadre": {}
    }
    try:
        response = requests.get(info["url"], headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tabella = soup.find('table', id=lambda x: x and 'stats_squads' in x)
            if tabella:
                righe = tabella.find('tbody').find_all('tr')
                for riga in righe:
                    cellula_squadra = riga.find('th', data_stat='team') or riga.find('td', data_stat='team')
                    if cellula_squadra:
                        nome_squadra = cellula_squadra.text.strip()
                        dati_finali[chiave]["squadre"][nome_squadra] = {}
    except Exception as e:
        print(f"Errore per {info['nome']}: {e}")

percorso_file = os.path.join('dati', 'stats.json')
with open(percorso_file, 'w', encoding='utf-8') as f:
    json.dump(dati_finali, f, ensure_ascii=False, indent=4)

print("Scraper completato e dati salvati con successo in dati/stats.json")
