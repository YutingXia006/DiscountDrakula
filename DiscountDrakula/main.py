import re
import os
from ai_interface import build_recepie_prompt, build_filter_prompt, call_ai
from io_interface import parse_txt, format_angebote
from scrapper import fetch_all_offers
from datetime import datetime
import json

def parse_json_response(response: str) -> dict:
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if not match:
        raise ValueError("Kein JSON gefunden!")
    return json.loads(match.group())

def main():
    file_path = os.path.join("json", f"KW{datetime.now().isocalendar().week}_angebote_gefiltert.json")
    if os.path.exists(file_path):
        #json von "KW_{datetime.now().isocalendar().week}_angebote_gefiltert.json" laden
        with open(file_path, encoding="utf-8") as f:
            filtered_offers=json.load(f)
    else:
        offers = fetch_all_offers()
        prompt1 = build_filter_prompt(offers)
        response1 = call_ai(prompt1)
        filtered_offers = parse_json_response(response1)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(filtered_offers, f, ensure_ascii=False, indent=2)

    zutaten = parse_txt("zutaten.txt")
    gerichte = parse_txt("gerichte.txt")
    speiseplan_prompt = build_recepie_prompt(filtered_offers, zutaten, gerichte)
    
    speiseplan = call_ai(speiseplan_prompt)

    dateiname = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    #datei speichern
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write(speiseplan)

if __name__ == '__main__':
    main()