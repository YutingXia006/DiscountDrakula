import requests
import re
import json

RELEVANT_SUPERMARKTS = ['Lidl', 'REWE', 'EDEKA']
LAT = 48.774465
LNG = 9.185967

def fetch_brochure_ids():
    html = requests.get(
        "https://www.kaufda.de/shelf",
        params={"lat": LAT, "lng": LNG}
    ).text

    # Händlername + ID zusammen extrahieren
    matches = re.findall(
        r'font-bold[^>]*>([^<]+)</div>.*?bonial\.biz/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
        html
    )

    brochure_ids = {} 

    for name, id in matches:
        if name in RELEVANT_SUPERMARKTS and name not in brochure_ids:
            brochure_ids[name] = id
    return brochure_ids

def main():
    BROCHURE_IDS = fetch_brochure_ids()
    print(BROCHURE_IDS)

# def fetch_ids():
#     html = requests.get(
#         "https://www.kaufda.de/shelf",
#         params={"lat": LAT, "lng": LNG}
#     ).text

#     # Händlername + ID zusammen extrahieren
#     matches = re.findall(
#         r'font-bold[^>]*>([^<]+)</div>.*?bonial\.biz/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
#         html
#     )
#     brochure_id = {}
#     for name, id in matches:
#         # print(f"{name} → {id}")
#         if name in RELEVANT_SUPERMARKTS and name not in brochure_id:
#             brochure_id[name] = id
#     print(brochure_id)
#     return brochure_id

if __name__ == '__main__':
    main()