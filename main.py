from dotenv import load_dotenv
load_dotenv()
import re
import os
from src.ai_interface import build_recepie_prompt, build_filter_prompt, call_filter_ai, call_recepie_ai
from src.io_interface import parse_txt
from src.scrapper import fetch_all_offers
from datetime import datetime
import json


def parse_json_response(response: str) -> dict:
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if not match:
        raise ValueError("Kein JSON gefunden!")
    return json.loads(match.group())

def main():
    os.makedirs("json", exist_ok=True)
    file_path = os.path.join("json", f"KW{datetime.now().isocalendar().week}_angebote_gefiltert.json")
    if os.path.exists(file_path):
        #json von "KW_{datetime.now().isocalendar().week}_angebote_gefiltert.json" laden
        with open(file_path, encoding="utf-8") as f:
            filtered_offers=json.load(f)
    else:
        offers = fetch_all_offers()
        prompt1 = build_filter_prompt(offers)
        response1 = call_filter_ai(prompt1)
        filtered_offers = parse_json_response(response1)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(filtered_offers, f, ensure_ascii=False, indent=2)

    os.makedirs("data", exist_ok=True)
    zutaten = parse_txt("data\\vorhandene_zutaten.txt")
    speiseplan_prompt = build_recepie_prompt(filtered_offers, zutaten)
    
    speiseplan = call_recepie_ai(speiseplan_prompt)

    dateiname = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    #datei speichern
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write(speiseplan)

if __name__ == '__main__':
    main()