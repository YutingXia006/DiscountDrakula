from scrapper import fetch_all_offers
from groq import Groq    
from dotenv import load_dotenv
import os
from datetime import datetime
from io_interface import parse_txt, format_angebote, format_kategorien

def call_ai(prompt: str) -> str:
    load_dotenv()
    client = Groq(
        api_key=os.getenv('API_KEY')
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=8000,
        temperature=0.7
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
    Du bist ein professioneller Küchenchef und Ernährungsberater. Erstelle einen Speiseplan für eine Woche.

    Zutaten die vorhanden sind:
    {format_kategorien(zutaten)}

    Angebote dieser Woche:
    {format_angebote(angebote, False)}

    MAKRO-ZIELE PRO TAG (pro Person, Ziel: Abnehmen):
    - Kalorien: Person 1 → 1150-1200 kcal | Person 2 → 1400-1500 kcal
    - Protein: mindestens 100-120g (Muskelerhalt beim Abnehmen)
    - Kohlenhydrate: 100-130g
    - Fett: 40-55g
    - Ballaststoffe: mindestens 30g (Sättigung!)

    HINWEIS: Rezepte für 2 Personen berechnen.
    Person 1 reduziert Kohlenhydrat-Beilage um 30%.
    Proteinquellen bleiben gleich für beide.

    MAKRO-VERTEILUNG PRO MAHLZEIT:
    - Frühstück: 25% der Tageskalorien
    - Mittagessen: 40% der Tageskalorien
    - Abendessen: 35% der Tageskalorien

    WICHTIGE ANWEISUNGEN:
    - Schreibe den Plan VOLLSTÄNDIG und KOMPLETT
    - Überspringe KEINE Tage
    - Kürze KEINE Rezepte ab

    RAHMENBEDINGUNGEN:
    - Portionen: 2 Personen
    - Küche: Westlich und Östlich gemischt
    - Kocherfahrung: Fortgeschrittener Hobbykoch
    - Ernährungsweise: Kein Schweinefleisch, laktosearm, zuckerarm, kaloriearm, proteinreich, glutenfrei
    - Jedes Gericht braucht einen kreativen konkreten Namen

    STRIKT VERBOTEN:
    - Zutaten: Paprika, Mais, rohe Karotten, rohe Tomaten, gekochter Lachs
    - Vage Begriffe: "Gemüse", "Fleisch", "Gewürze", "Kräuter", "Öl" → IMMER spezifisch!
    - Wiederholung: kein Gericht darf zweimal vorkommen

    PFLICHTREGELN:
    - Jede Zutat MIT Menge (g/ml/Stück/TL/EL)
    - Jedes Gericht = Protein + Kohlenhydrat + spezifisches Gemüse
    - Neue Zutaten erlaubt die nicht auf der Liste stehen
    - Makros MÜSSEN realistisch berechnet sein

    DEINE ANTWORT MUSS ENTHALTEN:
    1. Wochenübersicht (Tabelle: Tag | Frühstück | Mittagessen | Abendessen)
    2. Pro Rezept:
    - Zubereitungszeit & Kochzeit
    - Zutaten mit genauen Mengenangaben
    - Makros pro Portion (Kalorien | Protein | Kohlenhydrate | Fett | Ballaststoffe)
    - Schritt-für-Schritt Anleitung (nummeriert)
    - Tipps & Variationen
    - Mögliche Ersatzzutaten
    3. Tages-Makro Zusammenfassung (Tabelle pro Tag)
    4. Einkaufsliste mit fehlenden Zutaten (sortiert nach Kategorie)

    Schreibe auf Deutsch in Markdown.
    """


if __name__ == "__main__":
    offers = fetch_all_offers()
    zutaten = parse_txt("zutaten.txt")
    gerichte = parse_txt("gerichte.txt")
    print(call_ai("das ist ein test, sag 'HelloWorld!'"))
    print(build_filter_prompt(offers))
    print(build_recepie_prompt(offers, zutaten, gerichte))