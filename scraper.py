import os
import json
import requests
from bs4 import BeautifulSoup

# URL di esempio per FBref dei Top 5 campionati (stagione attuale)
# Lo script estrae tabelle, pulisce e calcola le medie casa/trasferta
LEAGUES = {
    "serie_a": {"name": "Serie A", "url": "https://fbref.com/it/comp/11/11/Serie-A-Statistiche"},
    "premier_league": {"name": "Premier League", "url": "https://fbref.com/it/comp/9/9/Premier-League-Statistiche"},
    "la_liga": {"name": "La Liga", "url": "https://fbref.com/it/comp/12/12/La-Liga-Statistiche"},
    "bundesliga": {"name": "Bundesliga", "url": "https://fbref.com/it/comp/20/20/Bundesliga-Statistiche"},
    "ligue_1": {"name": "Ligue 1", "url": "https://fbref.com/it/comp/13/13/Ligue-1-Statistiche"}
}

print("Inizializzazione dello script di estrazione dati...")
# Per ora creiamo la struttura base che espanderemo per popolare il file JSON ufficiale
data_output = {}

for key, info in LEAGUES.items():
    data_output[key] = {
        "league_name": info["name"],
        "teams": {}
    }

# Salviamo un file JSON di test/struttura iniziale
os.makedirs("data", exist_ok=True)
with open("data/stats.json", "w", encoding="utf-8") as f:
    json.dump(data_output, f, ensure_ascii=False, indent=4)

print("Struttura dati inizializzata con successo.")
