from scrapper import fetch_all_offers
from groq import Groq    
from dotenv import load_dotenv
import os
from datetime import datetime
from io_interface import parse_txt, format_angebote, format_kategorien

# def aus_txt_laden(datei_pfad: str = "zutaten.txt") -> dict:
#     zutaten = {}
#     aktuelle_kategorie = "Sonstiges"
    
#     with open(datei_pfad, "r", encoding="utf-8") as f:
#         for zeile in f:
#             zeile = zeile.strip()
#             if not zeile:
#                 continue
#             if zeile.startswith("[") and zeile.endswith("]"):
#                 aktuelle_kategorie = zeile[1:-1]
#                 zutaten[aktuelle_kategorie] = []
#             else:
#                 zutaten[aktuelle_kategorie].append(zeile)
#     return zutaten

# def parse_txt(dateipfad: str) -> dict:
#     result = {}
#     kategorie = None
#     with open(dateipfad, "r", encoding="utf-8") as f:
#         for zeile in f:
#             zeile = zeile.strip()
#             if not zeile:
#                 continue
#             if zeile.startswith("[") and zeile.endswith("]"):
#                 kategorie = zeile[1:-1]
#                 result[kategorie] = []
#             elif kategorie:
#                 result[kategorie].append(zeile)
#     return result

def call_ai(prompt: str) -> str:
    load_dotenv()
    client = Groq(
        api_key=os.getenv('GROQ_API_KEY')
    )

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=8000
    )
    content = response.choices[0].message.content
    return content #type: ignore

def build_filter_prompt(angebote: dict) -> str:
    return f"""
    Du bekommst eine Liste von Supermarktangeboten.
    Extrahiere NUR Produkte die zum Kochen geeignet sind.

    **Ignoriere:**
    - Alkohol (Bier, Wein, Spirituosen)
    - Süßigkeiten & Snacks (Chips, Schokolade, Kekse, Eis)
    - Non-Food Artikel (Holzkohle, Pfannen, etc.)
    - Fertiggerichte & Fast Food
    - Softdrinks & Energy Drinks

    **Behalte:**
    - Fleisch, Fisch, Meeresfrüchte
    - Gemüse & Obst
    - Milchprodukte & Käse
    - Nudeln, Reis, Getreide
    - Saucen, Gewürze, Öle
    - Brot & Backwaren (zum Frühstück)
    - Säfte & Wasser

    **Angebote:**
    {format_angebote(angebote, True)}

    **Ausgabe als JSON:**
    {{
    "Lidl": [
        {{"name": "Produktname", "price_eur": 1.99}}
    ],
    "EDEKA": [...]
    }}

    Keine Erklärungen, nur JSON.
    """

def build_recepie_prompt(angebote: dict, zutaten: dict, gerichte: dict): 
    #     Lieblingsgerichte (erstelle ähnliche Gerichte):
    # {format_kategorien(gerichte)}
    return f"""
    Du bist ein professioneller Küchenchef. Erstelle ein Speiseplan für eine Woche mit folgenden Vorgaben:

    Zutaten die vorhanden sind:
    {format_kategorien(zutaten)}

    Angebote dieser Woche
    {format_angebote(angebote, False)}

    Rahmenbedingungen:
    - Kreative Gerichte
    - Portionen: 2 Personen
    - Küche: Westlich und Östlich
    - Kocherfahrung: Fortgeschrittener Hobbykoch
    - Ernährungsweise: Kein Schweinefleisch, laktosearm, zuckerarm, kaloriearm, proteinreich
    - STRIKT VERBOTEN: Paprika(Gemüse) , Mais, rohe Karroten, rohe Tomaten, gekochtes Lachs

**Deine Antwort MUSS enthalten:**
1. Wochenübersicht (Tabelle: Tag | Frühstück | Mittagessen | Abendessen)
2. Pro Rezept:
    - Zubereitungszeit & Kochzeit
    - Zutaten mit genauen Mengenangaben
    - Schritt-für-Schritt Anleitung (nummeriert)
    - Tipps & Variationen
    - Mögliche Ersatzzutaten
3. Gesamte Einkaufsliste (sortiert nach Supermarkt)

    Schreibe auf Deutsch in Markdown. Halte die Sprache einfach und verständlich.
    """

if __name__ == "__main__":
    offers = fetch_all_offers()
    zutaten = parse_txt("zutaten.txt")
    gerichte = parse_txt("gerichte.txt")
    print(call_ai("das ist ein test, sag 'HelloWorld!'"))
    print(build_filter_prompt(offers))
    print(build_recepie_prompt(offers, zutaten, gerichte))